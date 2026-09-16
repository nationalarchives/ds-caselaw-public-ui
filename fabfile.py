import os
import signal
import subprocess
from contextlib import contextmanager

from invoke import run as local
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
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
    result = subprocess.run(["docker", "compose", "exec", "-T", container_name, "bash", "-c", cmd], check=False)
    if check_returncode:
        result.check_returncode()
    return result


@contextmanager
def background_exec(cmd, logfile):
    "Run a child process for the duration of a task, capturing its logs."
    with open(f"{logfile}.log", "w") as output:
        process = subprocess.Popen(cmd, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)

        def terminate(signum, frame):
            raise SystemExit(128 + signum)

        previous_handlers = {sig: signal.signal(sig, terminate) for sig in (signal.SIGTERM, signal.SIGHUP)}
        try:
            yield process
        finally:
            try:
                # npm spawns Node, so stop the whole group rather than just npm.
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                finally:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait()
            finally:
                for sig, handler in previous_handlers.items():
                    signal.signal(sig, handler)


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
    try:
        django_exec("pip install -r requirements/local.txt -U")
        django_exec("python manage.py migrate")
    finally:
        stop(c)


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
    try:
        start(c, "django")
        with background_exec(["npm", "run", "dev"], "assets"):
            collectstatic(c)
            django_exec("VITE_DEV_SERVER_ENABLED=true python manage.py runserver 0.0.0.0:3000")
    except KeyboardInterrupt:
        pass
    finally:
        stop(c)


@task(pip, npm_install, runquick)
def run(c): ...


@task
def memray(c):
    """Launch the server with memray tracking for live connections with `live`"""
    try:
        start(c, "django")
        with background_exec(["npm", "run", "dev"], "assets"):
            collectstatic(c)
            django_exec(
                "VITE_DEV_SERVER_ENABLED=true memray run --live-remote --live-port 8002 manage.py runserver 0.0.0.0:3000"
            )
    except KeyboardInterrupt:
        pass
    finally:
        stop(c)


@task
def live(c):
    """Display a running memray instance"""
    try:
        django_exec("memray live 8002")
    except KeyboardInterrupt:
        pass


@task
def flamegraph(c):
    """Take a memray log whilst running the server, then generate a flamegraph from it and show that flamegraph in the browser"""
    try:
        start(c, "django")
        with background_exec(["npm", "run", "dev"], "assets"):
            collectstatic(c)
            try:
                os.remove("memray.out")
            except FileNotFoundError:
                pass

            try:
                django_exec("VITE_DEV_SERVER_ENABLED=true memray run -o memray.out manage.py runserver 0.0.0.0:3000")
            except KeyboardInterrupt:
                pass

            try:
                os.remove("memray-flamegraph-memray.html")
            except FileNotFoundError:
                pass

            try:
                django_exec("memray flamegraph memray.out")
            except KeyboardInterrupt:
                pass

            subprocess.run(["open", "memray-flamegraph-memray.html"], check=False)
    finally:
        stop(c)


@task
def stop(c, container_name=None):
    """
    Stop the local development environment.
    """
    cmd = ["docker", "compose", "stop", "--timeout", "10"]
    if container_name:
        cmd.append(container_name)
    # Allow shutdown to finish even if the terminal sends another interrupt.
    previous_handlers = {
        sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
    }
    try:
        subprocess.run(cmd, check=True, start_new_session=True)
    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)


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
    subprocess.run(["docker", "compose", "exec", "django", "bash"], check=False)


@task
def checktypes(c):
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
        check=False,
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
            check=False,
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
            check=False,
        )
    else:
        subprocess.run(["docker", "compose", "exec", "django", "pytest", test], check=False)


@task(optional=["baseUrl", "regenerateSnapshots", "testPath"])
def e2etest(c, baseUrl="http://django:3000", regenerateSnapshots="false", testPath=None):
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
        check=False,
    )

    pytest_cmd = [
        "pytest",
        "--base-url",
        baseUrl,
    ]

    if testPath:
        pytest_cmd.append(testPath)

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-e",
            f"E2E_REGENERATE_SNAPSHOTS={regenerateSnapshots}",
            "e2e_tests",
            *pytest_cmd,
        ],
        check=False,
    )


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
        check=False,
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
        check=False,
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

    subprocess.run(cmd_list, check=False)


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
