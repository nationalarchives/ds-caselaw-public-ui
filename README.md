# The National Archives: Find Case Law

This repository is part of the [Find Case Law](https://caselaw.nationalarchives.gov.uk/) project at [The National Archives](https://www.nationalarchives.gov.uk/). For more information on the project, check [the documentation](https://github.com/nationalarchives/ds-find-caselaw-docs).

# Public Interface

![Tests](https://img.shields.io/github/actions/workflow/status/nationalarchives/ds-caselaw-public-ui/ci.yml?branch=main&label=tests) ![Coverage](https://img.shields.io/codeclimate/coverage/nationalarchives/ds-caselaw-public-ui) ![Maintainability](https://img.shields.io/codeclimate/maintainability/nationalarchives/ds-caselaw-public-ui)

A public interface to the service, allowing users to search archived items of case law.

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

This app is intended to edit Judgments in the Marklogic database defined in [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic).

Unless you are intending to do any database/Marklogic development work, it is simpler to access a
shared Marklogic database running on the `staging` environment than to build your own.

If you wish to run your own Marklogic instance, you will need to follow the setup instructions for it at [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic).

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
cp .env.example .env
```

If new environment variables are required, you might need to update .env to reflect that. Check .env.example for suitable default values

### 3. Compile frontend assets

With the dependencies installed as described in [Front end development](#front-end-development)

```bash
npm run build
```

### 4. Build Docker containers

```console
fab build
```

You might need to run this periodically if there are changes to the setup of the docker container;
it's a good thing to run if your environment suddenly stops working.

If this fails early on, it's very likely that Docker isn't running, and you'll need to start it.

### 5. Create Docker network

The `docker-compose` files in this repo and in [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic) both specify an external default network named `caselaw`.

We need to create a network with this name if it does not yet exist:

```console
docker network create caselaw
```

### 6. Run Marklogic

**Note** If you are using the staging instance of Marklogic, you do not need to
follow this step.

Switch to the location of [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic) and run:

```console
docker-compose up
```

### 7. Quick start

At this point you can run the following command to "quick start" the application:

```console
fab run
```

This command takes care of the following:

1. Starting all of the necessary Docker containers
2. Installing any new python dependencies
3. Applying any new database migrations
4. Starting the Django development server

You can then access the site in your browser:

<http://127.0.0.1:3000>

#### Fixing an issue when another project is already running

When starting up, if you encounter an error message like this:

`ERROR: for postgres Cannot start service postgres: driver failed programming external connectivity on endpoint ds-caselaw-public-ui_postgres_1 (0fb7572d583761d3a348e8fd9139b0007638a17c6f91b15e8678f2575f94ffa7): Bind for 0.0.0.0:5432 failed: port is already allocated`

It's because the editor UI project is still running, you'll need to reopen that project and run the command `fab stop`.
Now go back to the Public UI project and use the same command `fab stop`.
Now you can restart the project up again with `fab run`.

### 8. Other development tips

For day to day development, running `fab run` should provide you with all you need.

Other useful commands are:

#### Start Docker containers (in the background)

Note that running this command will fail if you have already started the application with
`fab run`

```console
fab start
```

#### To stop any running containers

```console
fab stop
```

#### Start a shell session with the 'django' container

```console
fab sh
```

#### Apply database migrations

Run the following inside the `django` container

```console
python manage.py migrate
```

#### Run a 'development' web server

```console
python manage.py runserver_plus 0.0.0.0:3000
```

#### Running the test suite

```console
fab test
```

#### Viewing code coverage

```console
fab coverage
```

This will generate an HTML file at `htmlcov/index.html` to view code coverage

### PDF Generation

We used the [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/) library to handle PDF generation on the backend, but moved to producing PDFs via [LibreOffice](https://github.com/nationalarchives/ds-caselaw-pdf-conversion). But WeasyPrint is still used as a fallback if the PDF is not found in the S3 bucket.

If you are using the provided Docker images, the dependencies for WeasyPrint are bundled in the Dockerfile.

If you see an error containing this message:

If you are running the application locally, without using Docker (for example in a local virtualenv), then you need to follow the steps outlined [here](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) to install the WeasyPrint dependencies on your local machine. You may need to recreate your virtualenv after following these steps.

```python
cannot load library 'gobject-2.0-0'
```

Then it means the dependencies for WeasyPrint have not been installed correctly. Try rebuilding the docker image using the command `docker-compose build django` and then running `fab run`.

## Using the pre-push hook (optional)

Copy `pre-push.sample` to `.git/hooks/pre-push` to set up the pre-push hook. This will run Python linting and style checks when you push to the repo and alert you to any linting issues that will cause CI to fail. To use this, you will need to install [pre-commit](https://pre-commit.com/) on your development machine which should be installed in the poetry environment.

## Setting up commit signing

Any commit that's merged to `main` needs to be [signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits), to ensure the identity of the author is who they say they are.

We recommend signing with your ssh key, as it's probably the easiest method of doing so. Assuming you already have an ssh key created, just follow the following steps:

- Add your SSH key as a _signing key_ in your [github account](https://github.com/settings/keys) - note this is different to an _authentication key_, which you likely already have set up. You can use the same key for both purposes, but you need to add it separately for each one twice.
- In your terminal, run the following commands. This assumes you want to set up commit signing by default for all repositories. If you don't want this for whatever, reason, leave out the `--global` flag (but in that case you'll have to remember to repeat these steps in every TNA repository you work on):
  - Enable signing with `git config --global commit.gpgsign true`
  - Specify that we'll use SSH for signing with: `git config --global gpg.format ssh`
  - Specify the key you'll use to sign. If it's not id_rsa.pub, give the correct path here: `git config --global user.signingkey ~/.ssh/id_rsa.pub`

If you have already made some unsigned commits on a branch before setting up signing, you'll need to sign them before they can be merged. You can do this by rebasing, typically using for example `git rebase --force-rebase main` then doing a force push. Care should obviously be taken here however, especially if there's anyone else working on your branch!

## Front end development

### Pre-requisites

- Ensure you have NodeJS & NPM installed.
- Install SASS globally by running `npm install -g sass`.

### Dependencies in this repository

Install these with:

```console
npm i
```

- Webpack and Babel for transpiling JavaScript
- Sass for compiling CSS

### Working with SASS/CSS

- To watch and build the site SASS, run `npm run start-sass`
- To modify styles, navigate to the `sass` folder in your editor.

#### Note about `ds_judgements_public_ui/sass/includes/_judgment_text.scss`

The Judgment display CSS `_judgment_text.scss` should be the same between both
this application and `ds-caselaw-editor-ui`. Ensuring edits to this repository were being
replicated to the editor repository was tricky as it relied on the developers
remembering to make changes in both places.

Instead, we share the judgment CSS between both apps. This repository is the
"source of truth". Any edits made in `ds-caselaw-public-ui` which are then merged to main and included in a
production release, will be reflected in `ds-caselaw-editor-ui` (note that the changes have to be included in
[a release](https://github.com/nationalarchives/ds-caselaw-public-ui/releases) before they are used in the editor).

Note that if a release is made on `ds-caselaw-public-ui` which contains edits to this CSS, a deployment will need to be
made to `ds-caselaw-editor-ui` to force that app to pick up the new version of the CSS. A deployment can be made via
dalmatian, without needing to do a full release of the editor.

`_judgment_text.scss` only contains styles for the HTML judgment view. Other CSS styles for the public UI and editor
UI applications are not shared.

### Working with JavaScript

In a new terminal session run `npm run start-scripts` to kick off a Webpack watch task

### Internationalisation

We're using [the built-in django translation module](https://docs.djangoproject.com/en/4.0/topics/i18n/translation) to handle our translations.

#### Adding new translations

1. Ensure that the `i18n` module is loaded at the top of the file:

   ```django
   {% extends 'layouts/base.html' %}
   {% load i18n %}
   ...
   ```

2. Add the translation string to the page:

   ```
   <h1>{% translate "namespace.mytranslation" %}</h1>
   ```

3. Update the locale file by running the following command in a `fab sh` shell:

   ```
   python manage.py makemessages --no-obsolete --add-location file -l en_GB
   ```

4. In the generated `.po` file, find the generated translation section, it will be a block like this, with the `msgid` corresponding to the key you added in the template:

   ```
   #: ds_caselaw_editor_ui/templates/includes/my_template.html
   #, fuzzy
   #| msgid "namespace.othertranslation"
   msgid "namespace.mytranslation"
   msgstr "An existing translation autofilled as an example"
   ```

   You need to do two things here - first remove the line starting with `#, fuzzy` and any lines starting with `#|` below it, then edit the line starting with `msgstr` to include your translation string. The end result will look something like this:

   ```
   #: ds_caselaw_editor_ui/templates/includes/my_template.html
   msgid "namespace.mytranslation"
   msgstr "This is my translation"
   ```

5. Compile the translations to a binary file (this should also be run inside a `fab sh` shell):
   ```
   python manage.py compilemessages
   ```

### Changing existing translations

1. Find the translation string you want to change in the template:

   ```django
      <h1>{% translate "namespace.mytranslation" %}</h1>
   ```

2. Go and look for this translation in the `django.po` file (you'll be looking for a line with `msgid` at the start and the string you saw in the template):

   ```
   msgid "namespace.mytranslation"
   msgstr "This is my translation"
   ```

3. Change the text on the following line (begining with `msgstr` to the new translation you want):

   ```
   msgid "namespace.mytranslation"
   msgstr "This is the new tranlation text I have edited"
   ```

4. Compile the translations again to make your changes show up (this should be run inside a `fab sh` shell):

   ```
   python manage.py compilemessages
   ```

## A note on running `django` commands locally

django commands need to be run within the `django` docker container, not on your machine itself, so from your terminal, you will need to first run `fab sh`, which will give you a console where you can run commands within the container (you'll see your terminal change from saying something like `tim@Tims-Macbook` at the start of each line to `root@abcde12345`). You can then run the commands you need to (such as `python manage.py shell_plus`), and when you're done, type the command `exit` to exit back out to your own machine again (the start of each line will change back).

## Adding or removing stop words from the search

Anyone with access to the Github repo can add or remove stop words from the search.

1. Edit `judgments/fixtures/stop_words.py` to add or remove stop words as desired. Pay attention to the file format -
   the stop words must be in a Python list, quoted and followed by a comma.
2. Commit your changes to the repo and open a pull request as normal.
3. Once the PR is merged, the modified list of stop words will be used in the search.

## Deployment

### Environment variables

If there are new or changed environment variables, a dxw-er will need to run:
`dalmatian service set-environment-variable -i caselaw-stg -e staging -s public -k NEW_ENV_VAR -v VALUE`
(possibly with `caselaw` and `prod` for production and `editor` for the editor ui)

### Staging

The `main` branch is automatically deployed with each commit. The deployed app can be viewed at [https://staging.caselaw.nationalarchives.gov.uk/](https://staging.caselaw.nationalarchives.gov.uk/)

### Production

To deploy to production:

1. Create a [new release](https://github.com/nationalarchives/ds-caselaw-public-ui/releases).
2. Set the tag and release name to `vX.Y.Z`, following semantic versioning.
3. Publish the release.
4. Automated workflow will then force-push that release to the `production` branch, which will then be deployed to the production environment.
5. If you need to roll back to an earlier version, force-push that version to `production` manually.

The production app is at [https://caselaw.nationalarchives.gov.uk/](https://caselaw.nationalarchives.gov.uk/)

### Local setup hints

1. Remember to `git pull` the freshest files
2. If `fab build` fails early, check that Docker is running? (Click the blue whale)
3. If the public-ui takes forever to load, check that the VPN is running -- you might need to change
   the IP address if DNS isn't working for you.
4. If it was working, and you `git pull`ed, and now it isn't, re-run `fab build`.
5. If it's saying environment variables aren't set (especially after a `git pull`), you might need
   to add lines to `.env` -- take them from `.env.example`
