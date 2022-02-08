# ds-judgements-public-ui

See [cookiecutter-README](doc/cookiecutter-README.md) for information related to the Cookiecutter install of Django.

## Environment

Copy `.env.example` to `env` to set your local environment variables

## Using Marklogic

To use Marklogic in development, edit `.env` and set `USE_MARKLOGIC` to true. You will then need to follow the instructions
in Judgements Data to create and populate your Marklogic database. 

### Judgments data

After running `script/bootstrap` you will need to create a database named `Judgments` in Marklogic. You can do this via
the Marklogic console. Run `docker-compose -f docker-marklogic.yml up` to bring up Marklogic in its own container.

Once this is up you can create and restore the database from an s3 bucket containing test Judgments data:

1. First, navigate to http://localhost:8001/, which will ask for basic auth. Username and password are both `admin`.
2. Then add AWS credentials to MarkLogic (under Security > Credentials), so it can pull the backup from a shared S3 bucket.
   The credentials (AWS access ID & secret key) should be for your `dxwbilling` account. You will need to create them in AWS
   if you haven't already.
3. Then create a database named `Judgments`in the Marklogic interface.
4. After creating the database, attach a `Forest` named `Judgments1`. The interface should tell you that the database does not have any Forests attached. To create this Forest click on the link provided within the interface, or click in the Forest folder and follow the instructions.
5. In the Backup/Restore tab in Marklogic for your new Judgments database, initiate a restore, using the following as the
   `"directory": s3://tna-judgments-marklogic-backup/`

Assuming you have entered the S3 credentials correctly, this will kick off a restore from s3. Once you have the data locally,
you can then back it up locally using the path `/var/opt/backup` in the management console. It will be backed up to your local
machine in `docker/db/backup`

#### Marklogic URL Guide

- http://localhost:8000/ this is the query interface where you can browse documents in the `Judgments` database.
- http://localhost:8001/ this is the management console where you can administer your database.
- http://localhost:8002/ this is the monitoring dashboard.
- http://localhost:8011/ this is the application server for the Marklogic REST interface
All four URLs use basic auth, username and password are both `admin`.

## Without using Marklogic

If you wish to run the application without Marklogic, set `USE_MARKLOGIC` to false in `.env`. You will then have 4 
judgments available to use in the UI:

- http://localhost:3000/judgments/ewca/civ/2004/811
- http://localhost:3000/judgments/ewca/civ/2004/632
- http://localhost:3000/judgments/ewca/civ/2006/392
- http://localhost:3000/judgments/ewca/civ/2007/214

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
