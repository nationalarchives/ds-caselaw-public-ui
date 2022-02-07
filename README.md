# ds-judgements-public-ui

See [cookiecutter-README](doc/cookiecutter-README.md) for information related to the Cookiecutter install of Django.

## Environment

Copy `.env.example` to `env` to set your local environment variables

## Judgments data

After running `script/bootstrap` you will need to create a database named `Judgments` in Marklogic. You can do this via
the Marklogic console. Run `docker-compose -f docker-marklogic.yml up` to bring up Marklogic in its own container.

Once this is up you can create and restore the database from an s3 bucket containing test Judgments data:

1. First, navigate to http://localhost:8001/, which will ask for basic auth. Username and password are both `admin`. 
2. Then add AWS credentials to MarkLogic (under Security > Credentials), so it can pull the backup from a shared S3 bucket.
   The credentials (AWS access ID & secret key) should be for your `dxwbilling` account. You will need to create them in AWS
   if you haven't already.
2. Then create a database named `Judgments`in the Marklogic interface.
3. In the Backup/Restore tab in Marklogic for your new Judgments database, initiate a restore, using the following as the
   `"directory": s3://tna-judgments-marklogic-backup/`

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

## Local development

### Pre-push hook

Copy `pre-push.sample` to `.git/hooks/pre-push` to set up the pre-push hook. This will run Python linting and
style checks when you push to the repo and alert you to any linting issues that will cause CI to fail.
