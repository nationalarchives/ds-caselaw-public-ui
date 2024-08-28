import os
import subprocess

from invoke import run as local
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f.readlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)


LOCAL_DATABASE_NAME = os.getenv("POSTGRES_DB")
LOCAL_DATABASE_USERNAME = os.getenv("POSTGRES_USER")
LOCAL_DB_DUMP_DIR = "database_dumps"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def container_exec(cmd, container_name="django", check_returncode=False):
    result = subprocess.run(["docker", "compose", "exec", "-T", container_name, "bash", "-c", cmd])
    if check_returncode:
        result.check_returncode()
    return result


def background_exec(cmd, logfile):
    "Run a command in the background and capture logs."
    if os.name == "posix":
        local(f"nohup {cmd} &> {logfile}.log &")


def postgres_exec(cmd, check_returncode=False):
    "Execute something in the 'postgres' Docker container."
    return container_exec(cmd, "postgres", check_returncode)


def django_exec(cmd, check_returncode=False):
    "Execute something in the 'django' Docker container."
    return container_exec(cmd, "django", check_returncode)


# -----------------------------------------------------------------------------
# Container management
# -----------------------------------------------------------------------------


@task
def build(c):
    """
    Build (or rebuild) local development containers.
    """
    local("docker compose build")


@task
def start(c, container_name=None):
    """
    Start the local development environment.
    """
    cmd = "docker compose up -d"
    if container_name:
        cmd += f" {container_name}"
    local(cmd)


@task
def pip(c):
    start(c, "django")
    django_exec("pip install -r requirements/local.txt -U")
    django_exec("DJANGO_SETTINGS_MODULE= django-admin compilemessages")
    django_exec("python manage.py migrate")
    stop(c, "django")


@task
def npm_install(c):
    """
    Install NPM packages
    """
    local("npm install")


@task
def collectstatic(c):
    """
    Update static assets
    """
    django_exec("rm -rf /app/staticfiles")
    django_exec("python manage.py collectstatic")


@task
def runquick(c):
    start(c, "django")
    background_exec("npm run watch", "assets")
    collectstatic(c)
    try:
        django_exec("python manage.py runserver 0.0.0.0:3000")
    except KeyboardInterrupt:
        pass
    stop(c, "django")


@task(pip, npm_install, runquick)
def run(c): ...


@task
def stop(c, container_name=None):
    """
    Stop the local development environment.
    """
    cmd = "docker compose stop"
    if container_name:
        cmd += f" {container_name}"
    local(cmd)


@task
def restart(c):
    """
    Restart the local development environment.
    """
    stop(c)
    start(c)


@task
def sh(c):
    """
    Run bash in a local container (with access to dependencies)
    """
    subprocess.run(["docker", "compose", "exec", "django", "bash"])


@task
def translate(c):
    """
    Make messages for translations
    """
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "django",
            "bash",
            "-c",
            "python manage.py makemessages --no-obsolete --add-location file -l en_GB "
            + "&& python manage.py compilemessages",
        ],
    )


@task(optional=["test"])
def test(c, test=None):
    """
    Run python tests in the web container
    """
    if test is None:
        # Static analysis
        subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "django",
                "mypy",
                "ds_judgements_public_ui",
                "judgments",
            ],
        )
        # Pytest
        subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "django",
                "pytest",
            ],
        )
    else:
        subprocess.run(["docker", "compose", "exec", "django", "pytest", test])


@task(optional=["baseUrl"])
def e2etest(c, baseUrl="http://django:3000"):
    """
    Run end-to-end playwright tests against the given base url -
    the default is the running local django web container.
    """
    subprocess.run(
        [
            "docker",
            "compose",
            "build",
            "e2e_tests",
        ],
    )
    subprocess.run(["docker", "compose", "run", "e2e_tests", "pytest", "--base-url", baseUrl])


@task
def coverage(c):
    # Run pytest with coverage
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "django",
            "coverage",
            "run",
            "-m",
            "pytest",
        ],
    )
    # Generate html report
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "django",
            "coverage",
            "html",
        ],
    )


# -----------------------------------------------------------------------------
# Database operations
# -----------------------------------------------------------------------------


@task
def psql(c, command=None):
    """
    Connect to the local postgres DB using psql
    """
    cmd_list = [
        "docker",
        "compose",
        "exec",
        "postgres",
        "psql",
        *["-d", LOCAL_DATABASE_NAME],
        *["-U", LOCAL_DATABASE_USERNAME],
    ]
    if command:
        cmd_list.extend(["-c", command])

    subprocess.run(cmd_list)


def delete_db(c):
    postgres_exec(f"dropdb --if-exists --host db --username={LOCAL_DATABASE_USERNAME} {LOCAL_DATABASE_NAME}")
    postgres_exec(f"createdb --host db --username={LOCAL_DATABASE_USERNAME} {LOCAL_DATABASE_NAME}")


@task
def dump_db(c, filename):
    """Snapshot the database, files will be stored in the db container"""
    if not filename.endswith(".dmp"):
        filename += ".dmp"
    postgres_exec(f"pg_dump -d {LOCAL_DATABASE_NAME} -U {LOCAL_DATABASE_USERNAME} > {filename}")
    print(f"Database dumped to: {filename}")


@task
def restore_db(c, filename, delete_dump_on_success=False, delete_dump_on_error=False):
    """Restore the database from a snapshot in the db container"""
    print("Stopping 'web' to sever DB connection")
    stop(c, "django")
    if not filename.endswith(".dmp"):
        filename += ".dmp"
    delete_db(c)

    try:
        print(f"Restoring datbase from: {filename}")
        postgres_exec(
            f"psql -d {LOCAL_DATABASE_NAME} -U {LOCAL_DATABASE_USERNAME} < {filename}",
            check_returncode=True,
        )
    except subprocess.CalledProcessError:
        if delete_dump_on_error:
            postgres_exec(f"rm {filename}")
        raise

    if delete_dump_on_success:
        print(f"Deleting dump file: {filename}")
        postgres_exec(f"rm {filename}")

    start(c, "django")
