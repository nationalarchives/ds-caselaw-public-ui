# ds-judgements-public-ui

Public UI

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy ds_judgements_public_ui

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

## Deployment

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## Environment

Copy `.env.example` to `env` to set your local environment variables

## Judgments data

Before running `script/bootstrap` you will need to create a database named `Judgments` in Marklogic. You can do this via
the Marklogic console. Run `docker-compose -f docker-marklogic.yml` to bring up Marklogic in its own container.

Once this is up you can create and restore the database from an s3 bucket containing test Judgments data:

1. First, add AWS credentials to MarkLogic (under Security > Credentials), so it can pull the backup from a shared S3 bucket.
   The credentials (AWS access ID & secret key) should be for your `dxwbilling` account. You will need to create them in AWS
   if you haven't already.
2. Then navigate to http://localhost:8001/ and create a database named `Judgments`.
3. In the Backup/Restore tab in Marklogic for your new Judgments database, initiate a restore, using the following as the
   "directory": s3://tna-judgments-marklogic-backup/

Assuming you have entered the S3 credentials correctly, this will kick off a restore from s3. Once you have the data locally,
you can then back it up locally using the path `/var/opt/backup` in the management console. It will be backed up to your local
machine in `docker/db/backup`

## Scripts

This application uses the "Scripts to rule them all" pattern.

### Bootstrap

Run `script/bootstrap` to set required environment variables for the application

### Test

Run `script/test` to run pytest and the linters

### Server

Run `script/server` to run the server

Marklogic will be run in its own Docker container, and its logs will be piped to `marklogic.log`
