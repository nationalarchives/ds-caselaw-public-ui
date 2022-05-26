
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

**NOTE**: This app is intended to edit Judgments in the Marklogic database defined in [ds-caselaw-public-access-service/marklogic](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/marklogic). If you do
not already have this application installed, you will need to follow the setup instructions for it.

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

### 5. Run Marklogic

Switch to the location of ds-caselaw-public-access-service/marklogic and run:

```console
$ docker-compose up
```

### 6. Create Docker network

``` console
$ docker network create caselaw
```

### 7. Start Docker containers

```console
$ fab start
```

### 8. Start a shell session with the 'django' container

```console
$ fab sh
```

### 9. Apply database migrations

```console
$ python manage.py migrate
```

### 10. Run a 'development' web server

```console
$ python manage.py runserver_plus 0.0.0.0:3000
```

### 11. Access the site

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
