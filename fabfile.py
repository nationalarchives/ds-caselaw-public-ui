import os
import subprocess

from invoke import run as local
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def container_exec(cmd, container_name="django", check_returncode=False):
    result = subprocess.run(
        ["docker-compose", "exec", "-T", container_name, "bash", "-c", cmd]
    )
    if check_returncode:
        result.check_returncode()
    return result


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
    local("docker-compose build")


@task
def start(c, container_name=None):
    """
    Start the local development environment.
    """
    cmd = "docker-compose up -d"
    if container_name:
        cmd += f" {container_name}"
    local(cmd)


@task
def run(c):
    start(c, "django")
    django_exec("pip install -r requirements/local.txt -U")
    django_exec("DJANGO_SETTINGS_MODULE= django-admin compilemessages")
    django_exec("python manage.py migrate")
    django_exec("rm -rf /app/staticfiles")
    django_exec("python manage.py collectstatic")
    return django_exec("python manage.py runserver 0.0.0.0:3000")


@task
def stop(c, container_name=None):
    """
    Stop the local development environment.
    """
    cmd = "docker-compose stop"
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
    subprocess.run(["docker-compose", "exec", "django", "bash"])


@task
def test(c):
    """
    Run python tests in the web container
    """
    # Static analysis
    subprocess.run(
        [
            "docker-compose",
            "exec",
            "django",
            "mypy",
            "ds_judgements_public_ui",
        ]
    )
    # Pytest
    subprocess.run(
        [
            "docker-compose",
            "exec",
            "django",
            "pytest",
        ]
    )
