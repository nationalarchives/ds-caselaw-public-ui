
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

## Getting started

**NOTE**: For any of the following commands to work, you must first [install Fabric](https://www.fabfile.org/installing.html). Once installed, you can type `fab -l` to see a list of available commands.

### 1. Get access to Marklogic

This app is intended to edit Judgments in the Marklogic database defined in [ds-caselaw-public-access-service/marklogic](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/marklogic).

Unless you are intending to do any database/Marklogic development work, it is simpler to access a
shared Marklogic database running on the `staging` environment than to build your own.

If you wish to run your own Marklogic instance, you will need to follow the setup instructions for it at
[ds-caselaw-public-access-service/marklogic](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/marklogic).

The **recommended** alternative is to access the shared staging Marklogic database. The way you do this
depends on where you work:

#### dxw developers

You will need to be using the dxw vpn. Retrieve the staging Marklogic credentials from dalmatian (or ask
one of the other developers/ops). Use these to fill MARKLOGIC_HOST, MARKLOGIC_USER and MARKLOGIC_PASSWORD
in your `.env` file (see step 2).

The MARKLOGIC_HOST should likely begin with `caselaw`

#### TNA/other developers

You will need vpn credentials from the dxw ops team, and the staging Marklogic credentials from one of the
dxw development team. Use these to fill MARKLOGIC_HOST, MARKLOGIC_USER and MARKLOGIC_PASSWORD
in your `.env` file (see step 2).

The MARKLOGIC_HOST should most likely begin with `internal`. Some people have experienced difficulties using
the domain name to connect to the server -- IP addresses may work better.

In both cases, when you run the application, you will be viewing data on staging Marklogic. This
data is also used for testing and occasionally user research, so please exercise caution when creating/
editing content!

### 2. Create `.env`

```console
$ cp .env.example .env
```

If new environment variables are required, you might need to update .env to reflect that. Check .env.example
for suitable default values

### 3. Compile frontend assets

With the dependencies installed as described in [Front end development](#front-end-development)

```bash
npm run build
```

### 4. Build Docker containers

```console
$ fab build
```

You might need to run this periodically if there are changes to the setup of the docker container;
it's a good thing to run if your environment suddenly stops working.

If this fails early on, it's very likely that Docker isn't running, and you'll need to start it by
clicking the Whale icon.

### 5. Run Marklogic

**Note** If you are using the staging instance of Marklogic, you do not need to
follow this step.

Switch to the location of ds-caselaw-public-access-service/marklogic and run:

```console
$ docker-compose up
```

### 6. Create Docker network

If you see an error message referring to a missing docker network, run the following
command to create it:

``` console
$ docker network create caselaw
```

### 7. Quick start

At this point you can run the following command to "quick start" the application:

```console
$ fab run
```

This command takes care of the following:

1. Starting all of the necessary Docker containers
2. Installing any new python dependencies
3. Applying any new database migrations
4. Starting the Django development server

You can then access the site in your browser:

<http://127.0.0.1:3000>

### 8. Other development tips

For day to day development, running `fab run` should provide you with all you need.

Other useful commands are:

#### Start Docker containers (in the background)

Note that running this command will fail if you have already started the application with
`fab run`

```console
$ fab start
```

To stop any running containers:

```console
$ fab stop
```

#### Start a shell session with the 'django' container

```console
$ fab sh
```

#### Apply database migrations

Run the following inside the `django` container

```console
# python manage.py migrate
```

#### Run a 'development' web server

```console
$ python manage.py runserver_plus 0.0.0.0:3000
```

### Running the test suite

```console
$ fab test
```

### Viewing code coverage

```console
$ fab coverage
```

This will generate an HTML file at `htmlcov/index.html` to view code coverage

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

where `language_code` is the ISO 3166-1 country code (e.g. en_GB)

4) In the generated `.po` file, find the generated msgid string and add the translation below it

```
msgid "naamespace.mytranslation"
msgstr "This is my translation"
```

5) Compile the translations to a binary file:
```
django-admin compilemessages
```

## Deployment

### Staging

The `main` branch is automatically deployed with each commit. The deployed app can be viewed at [https://staging.caselaw.nationalarchives.gov.uk/](https://staging.caselaw.nationalarchives.gov.uk/)

### Production

To deploy to production:

1. Create a [new release](https://github.com/nationalarchives/ds-caselaw-public-ui/releases).
2. Set the tag and release name to `vX.Y.Z`, following semantic versioning.
3. Publish the release.
4. Automated workflow will then force-push that release to the `production` branch, which will then be deployed to the production environment.

The production app is at [https://caselaw.nationalarchives.gov.uk/](https://caselaw.nationalarchives.gov.uk/)

### Local setup hints

1. Remember to `git pull` the freshest files
2. If `fab build` fails early, check that Docker is running? (Click the blue whale)
3. If the public-ui takes forever to load, check that the VPN is running -- you might need to change
   the IP address if DNS isn't working for you.
4. If it was working, and you `git pull`ed, and now it isn't, re-run `fab build`.
5. If it's saying environment variables aren't set (especially after a `git pull`), you might need
   to add lines to `.env` -- take them from `.env.example`
