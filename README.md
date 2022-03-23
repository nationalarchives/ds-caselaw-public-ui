Spuruious change
# ds-judgements-public-ui

## Local development

This project uses Docker to create a consistent environment for local development.

On macOS and Windows, Docker requires [Docker
Desktop](https://www.docker.com/products/docker-desktop) to be installed. Linux
users should install the Docker engine using their distribution's package
manager or [download a `.deb` or
`.rpm`](https://docs.docker.com/engine/install/)

Once installed, we need to build our containers. We use
[`docker-compose`](https://docs.docker.com/compose/) to orchestrate the
building of the project's containers, one for each each service:

### `django`

Our custom container responsible for running the application. Built from the
official [python 3.9](https://hub.docker.com/_/python/) base image

### `postgres`

The database service built from the official [postgres](https://hub.docker.com/_/postgres/) image

### `marklogic`

A database server built from the official [marklogic](https://hub.docker.com/_/marklogic) image.


## Getting started

**NOTE**: For any of the following commands to work, you must first [install Fabric](https://www.fabfile.org/installing.html). Once installed, you can type `fab -l` to see a list of available commands.

### 1. Gain access to the Marklogic image

Access to the Marklogic Docker image is restricted to those who have 'purchased' it on Docker Hub. It's actually FREE to
purchase, but you need to fill out [a short form](https://hub.docker.com/_/marklogic/purchase).

### 2. Create `.env`

```console
$ cp .env.example .env
```

### 3. Compile frontend assets

With the dependencies installed as described in [Front end development](#front-end-development)

```bash
npm run build
```

### 4. Build Docker containers

```console
$ fab build
```

### 5. Start Docker containers

```console
$ fab start
```

### 6. Start a shell session with the 'django' container

```console
$ fab sh
```

### 7. Apply database migrations

```console
$ python manage.py migrate
```

### 8. Run a 'development' web server

```console
$ python manage.py runserver_plus 0.0.0.0:3000
```

### 9. Access the site

<http://127.0.0.1:3000>

**NOTE**: Compiled CSS is not included and therefore needs to be built initially, and after each git pull.

## Additional development tips

### Quick start with `fab run`

While it's handy to be able to access the django container via a shell and interact with it directly, sometimes all you
want is to view the site in a web browser. In these cases, you can use:

```console
$ fab run
```

This command takes care of the following:

1. Starting all of the necessary Docker containers
2. Installing any new python dependencies
3. Applying any new database migrations
4. Starting the Django development server

You can then access the site in your browser as usual:

<http://127.0.0.1:3000>

### Available Judgments

- <http://127.0.0.1:3000/ewca/civ/2004/632>
- <http://127.0.0.1:3000/ewca/civ/2004/811>
- <http://127.0.0.1:3000/ewca/civ/2006/392>
- <http://127.0.0.1:3000/ewca/civ/2007/214>

### Running tests

```console
$ fab test
```

## Using Marklogic

If you wish to use Marklogic in development, you will need to run it in a Docker container of its own and populate
it with data.

### Bootstrap

Run `script/bootstrap-marklogic` to create local storage directories and the REST Application server in Marklogic.
You should only need to do this once.

### Importing Judgments data

Create a database in Marklogic and restore the data from an S3 bucket containing test Judgments data. Note that this
bucket is currently only available to dxw developers.

1. First, navigate to http://localhost:8001/, which will ask for basic auth. Username and password are both `admin`.
2. Then add AWS credentials to MarkLogic (under Security > Credentials), so it can pull the backup from a shared S3 bucket.
   The credentials (AWS access ID & secret key) should be for your `dxwbilling` account. You will need to create them in AWS
   if you haven't already.
3. Then create a database named `Judgments`in the Marklogic interface.
4. After creating the database, attach a `Forest` named `Judgments1`. The interface should tell you that the database
   does not have any Forests attached. To create this Forest click on the link provided within the interface, or click in
   the Forest folder and follow the instructions.
5. In the Backup/Restore tab in Marklogic for your new Judgments database, initiate a restore, using the following as the
   `"directory": s3://tna-judgments-marklogic-backup/`

Assuming you have entered the S3 credentials correctly, this will kick off a restore from s3. Once you have the data locally,
you can then back it up locally using the path `/var/opt/backup` in the management console. It will be backed up to your local
machine in `docker/db/backup`

### Adding indexes

In theory the restore from backup should create indexes in the database. If it does not, you will need to create them
manually.

In the Marklogic [management interface](http://localhost:8001/), first create a namespace for the index.
Go to `Databases -> Judgments -> Path namespaces` and create a new namespace with the prefix `akn` and url
`http://docs.oasis-open.org/legaldocml/ns/akn/3.0`

Then, go to `Databases -> Judgments -> Path Range indexes` and create a new index with the scalar type of `date` and
the path expression of `akn:FRBRWork/akn:FRBRdate/@date`. You can leave the other options as the defaults.

### Adding the XSLT transformation template

The XSLT which transforms the LegalDocML documents into HTML needs to be stored on Marklogic itself. To do this:

1. Open your terminal in the root of this project
2. Run this `curl` command:

```bash
curl --anyauth --user admin:admin -X PUT --data-binary @"./judgments/bootstrap/judgment2.xsl" \
 -H "Content-type: application/xslt+xml" \
  "http://localhost:8000/LATEST/documents?database=Modules&uri=/judgments/xslts/judgment2.xsl"
```

3. Open the Marklogic Query console at http://localhost:8000/ and choose tyhe `Modules` database from the Database
   dropdown
4. Click `Explore` to ensure the XSLT is in place, it should be called `/judgments/xslts/judgment2.xsl`

### Create some managed Judgments

Marklogic has the concept of "managed documents" which we use in order to store versioned Judgments and other Marklogic
features. Marking all 48000+ Judgments in the database takes too long, so we mark a subset of them as managed and use
these in development. To mark 100 Judgments as managed:

1. Open the Marklogic Query console at http://localhost:8000/
2. Copy the text in `judgments/xquery/manage_judgments.xqy` and paste it into the XQuery console
3. Run it against the database `Judgments` using the `XQuery` query type (see the dropdown options in the UI to configure
   these)
4. Once the script has run, 100 Judgments should be visible in the front-end UI

If you wish to set more than 100 to be managed, alter the `"limit=100"` parameter in the XQuery
(`cts:uris("", xs:string("limit=100"))`) to be a different number. Note that larger numbers will take a few minutes to
run.

### Publish all Judgments

By default, Judgments are not marked as published and therefore not visible in the app. To publish all Judgments locally:

1. Open the Marklogic Query console at http://localhost:8000/
2. Copy the text in `judgments/xquery/publish_all_judgments.xqy` and paste it into the XQuery console
3. Run it against the database `Judgments` using the `XQuery` query type (see the dropdown options in the UI to configure
   these), the XQuery will take a few minutes to run
4. Once the script has run, all Judgments should be visible in the front-end UI

### Set the versioned documents retention policy

We need to set Marklogic up so that when Judgments are edited, all earlier versions of the Judgment are preserved.

1. Open the Marklogic Query console at http://localhost:8000/
2. Copy the text in `judgments/xquery/set_retention_policy.xqy` and paste it into the XQuery console
3. Run it against the database `Judgments` using the `XQuery` query type (see the dropdown options in the UI to configure
   these)

### Marklogic URL Guide

- http://localhost:8000/ this is the query interface where you can browse documents in the `Judgments` database.
- http://localhost:8001/ this is the management console where you can administer your database.
- http://localhost:8002/ this is the monitoring dashboard.
- http://localhost:8011/ this is the application server for the Marklogic REST interface

All four URLs use basic auth, username and password are both `admin`.

### WeasyPrint PDF Library

We are using the [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/) library to handle PDF generation on the backend. If you are using the provided Docker images, the dependencies are bundled in the Dockerfile.

If you see an error containing this message:

If you are running the application locally, without using Docker (for example in a local virtualenv), then you need to follow the steps outlined [here](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) to install the WeasyPrint dependencies on your local machine. You may need to recreate your virtualenv after following these steps.

```python
cannot load library 'gobject-2.0-0'
```

Then it means the dependencies for WeasyPrint have not been installed correctly. Try rebuilding the docker image using the command `docker-compose build django` and then running `fab run`.

## Using the pre-push hook (optional)

Copy `pre-push.sample` to `.git/hooks/pre-push` to set up the pre-push hook. This will run Python linting and style checks when you push to the repo and alert you to any linting issues that will cause CI to fail.

## Front end development

Included in this repository is:

* Webpack and Babel for transpiling JavaScript
* Sass for compiling CSS

### Working with SASS/CSS

* Ensure you have NodeJS & NPM installed.
* Install SASS globally by running `npm install -g sass`.
* To watch and build the site SASS, run `npm run start-sass`
* To modify styles, navigate to the `sass` folder in your editor.

### Working with JavaScript

* In a new terminal session run `npm run start-scripts` to kick off a Webpack watch task

### Internationalisation

We're using [the built-in django translation module](https://docs.djangoproject.com/en/4.0/topics/i18n/translation) to handle our translations.

#### Adding translations

1) Ensure that the `i18n` module is loaded at the top of the file:

```django
{% extends 'base.html' %}
{% load i18n %}
...
```

2) Add the translation string to the page:
```
<h1>{% translate "namespace.mytranslation" %}</h1>
```

3) Update the locale file by running the following command:
```
django-admin makemessages -l {langage_code}
```

where `language_code` is the ISO 3166-1 country code (e.g. en_gb)

4) In the generated `.po` file, find the generated msgid string and add the translation below it

```
msgid "naamespace.mytranslation"
msgstr "This is my translation"
```

5) Compile the translations to a binary file:
```
django-admin compilemessages
```
