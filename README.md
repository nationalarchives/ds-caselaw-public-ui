# The National Archives: Find Case Law

This repository is part of the [Find Case Law](https://caselaw.nationalarchives.gov.uk/) project at [The National Archives](https://www.nationalarchives.gov.uk/). For more information on the project, check [the documentation](https://github.com/nationalarchives/ds-find-caselaw-docs).

# Public Interface

![Tests](https://img.shields.io/github/actions/workflow/status/nationalarchives/ds-caselaw-public-ui/ci.yml?branch=main&label=tests)
![Code Coverage](https://img.shields.io/codecov/c/github/nationalarchives/ds-caselaw-public-ui)

A public interface to the service, allowing users to search archived items of case law.

## Local development

This project uses Docker to create a consistent environment for local development.

On macOS and Windows, Docker requires [Docker
Desktop](https://www.docker.com/products/docker-desktop) to be installed. Linux
users should install the Docker engine using their distribution's package
manager or [download a `.deb` or
`.rpm`](https://docs.docker.com/engine/install/)

Once installed, we need to build our containers. We use
[`docker compose`](https://docs.docker.com/compose/) to orchestrate the
building of the project's containers:

### Services

- **`django`** — The application container, built from a multi-stage Dockerfile (local dev stage by default)
- **`postgres`** — PostgreSQL database
- **`e2e_tests`** — Playwright end-to-end tests (opt-in via `--profile e2e_tests`)

### Compose files

#### `docker-compose.yml` — Local development (default)

The base compose file targets the `python-local-stage` of the multi-stage Dockerfile. This stage installs all dependencies (including dev dependencies) but does **not** run the application server — instead it runs `tail -f /dev/null` so the container stays alive and you use `fab run` or `docker exec` to start the Django dev server, watch Sass, etc. Source code is mounted from the host (`.:/app:z`) so edits are reflected immediately without rebuilding.

#### `docker-compose.prod-test.yml` — Production image verification

This override file targets the final `python-production-stage` of the Dockerfile, which is the same image deployed to AWS ECS. Key differences from the local stage:

- **No volume mounts** — the app runs entirely from the files baked into the image, exactly as it would in production.
- **Separate entrypoint and start scripts** — `compose/docker/entrypoint` waits for Postgres and runs migrations, then `compose/docker/start` compiles frontend assets (`npm run build`), collects static files (`collectstatic`), and starts gunicorn on port 5000.
- **Runs as the `django` user** — not root, matching the production security model.
- **Includes a healthcheck** — polls `http://localhost:5000/check` to confirm the app is actually serving traffic, not just that the container started.

You won't use this during normal development, but it lets you catch production-only failures locally — for example, file permission issues, missing static assets, or entrypoint bugs that volume mounts would mask. CI runs this automatically on every push using `docker compose ... up --build --wait` to verify the production image builds and starts successfully before merging.

To verify the production image locally:

```console
docker compose -f docker-compose.yml -f docker-compose.prod-test.yml up --build --wait
```

## Getting started

**NOTE**: For any of the following commands to work, you must first [install Fabric](https://www.fabfile.org/installing.html). (Homebrew is also an option: `brew install fabric`.) Once installed, you can type `fab -l` to see a list of available commands.

### 1. Create `.env`

```console
cp .env.example .env
```

If new environment variables are required, you might need to update .env to reflect that. Check .env.example for suitable default values

### 2. Create Docker network

The compose files in this repo and in other caselaw services share an external network named `caselaw`. Create it if it does not yet exist:

```console
docker network create caselaw
```

### 3. MarkLogic

A MarkLogic instance is required for some functionality of the public interface, such as searching and viewing judgments.

You may not need to configure MarkLogic if you are not working on MarkLogic-dependent features or if the example MarkLogic responses provided by the VCR cassettes are sufficient.

The VCR cassettes provide MarkLogic responses for:

- [recently published judgments](http://127.0.0.1:3000/)
- [a judgment /eat/2023/1](http://127.0.0.1:3000/eat/2023/1)
- [a search query](http://127.0.0.1:3000/search?query=Imperial)

If you need to connect to a live MarkLogic instance, there are two main options:

1. Connect to the shared staging MarkLogic database.
2. Set up a local MarkLogic server.

**Setting up a local MarkLogic server:**

Clone and follow the README of the [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic) repository to set up a local MarkLogic server.

You can then set `MARKLOGIC_HOST=marklogic` in your `.env` to point the public interface at the local MarkLogic instance.

### 4. Compile frontend assets

With the dependencies installed as described in [Front end development](#front-end-development)

```bash
npm run build
```

### 5. Build Docker containers

```console
fab build
```

You might need to run this periodically if there are changes to the setup of the docker container;
it's a good thing to run if your environment suddenly stops working.

If this fails early on, it's very likely that Docker isn't running, and you'll need to start it.

### 6. Quick start

At this point you can run the following command to "quick start" the application:

```console
fab run
```

This command takes care of the following:

1. Starting all of the necessary Docker containers
2. Installing any new python dependencies
3. Applying any new database migrations
4. Starting the Django development server
5. Watching the Sass and JavaScript files for changes

You can then access the site in your browser:

<http://127.0.0.1:3000>

(NOTE: The output of the asset and JS builds are logged in the ./assets.log file)

#### Fixing an issue when another project is already running

When starting up, if you encounter an error message like this:

`ERROR: for postgres Cannot start service postgres: driver failed programming external connectivity on endpoint ds-caselaw-public-ui_postgres_1 (0fb7572d583761d3a348e8fd9139b0007638a17c6f91b15e8678f2575f94ffa7): Bind for 0.0.0.0:5432 failed: port is already allocated`

It's because the editor UI project is still running, you'll need to reopen that project and run the command `fab stop`.
Now go back to the Public UI project and use the same command `fab stop`.
Now you can restart the project up again with `fab run`.

## Other development tips

For day to day development, running `fab run` should provide you with all you need.

Other useful commands are:

### Start Docker containers (in the background)

Note that running this command will fail if you have already started the application with
`fab run`

```console
fab start
```

### To stop any running containers

```console
fab stop
```

### Start a shell session with the 'django' container

```console
fab sh
```

### Apply database migrations

Run the following inside the `django` container

```console
python manage.py migrate
```

### Run a 'development' web server

```console
python manage.py runserver_plus 0.0.0.0:3000
```

### Running the test suite

After running `fab start`

Pytest unit tests can be run with `fab test`.

We also have a suite of end to end tests (in the `e2e_tests/` directory) written with [playwright-pytest](https://playwright.dev/python/docs/api/class-playwright), which can be run with `fab e2etest`.
These will run by default against the running `django` container. You can supply a `baseURL` argument to test against staging or production.

### VCR Cassettes

To allow running the E2E tests in isolation, and to run the application in a state where it doesn't call out to external services, we have added VCR cassettes that can be played for external requests instead of calling out to that external service.

To enable these, add the following to your .env:

VCR_ENABLED=true // Controls whether to use recorded cassettes for HTTP requests
VCR_MODE=playback // VCR modes: playback (use cassettes), record (save requests)

### memray memory tools

To generate a flamegraph run `fab flamegraph`. After using the application, press Ctrl-C and the application will quit and the flamegraph will appear in your browser.

To see live memory usage run `fab memray` and `fab live` in different terminals.

### Accessibility testing with E2E tests

We use axe playwright to automatically check for accessibility issues on our pages. When adding a new page, you should also add a test to ensure it is accessible and stays accessible.

To add an automatic accessibility check you can add the `assert_is_accessible` check to your tests, for example:

### Visual Regression Tests

We use `skimage` to perform visual regression testing by comparing screenshots using the Structural Similarity Index (SSIM). Each test compares a newly generated screenshot with a previously stored snapshot in the codebase.

If the structural similarity score drops below an acceptable threshold, the test will fail.

#### What to do when a test fails

- Check the screenshots located in `e2e_tests/snapshots`:
- Expected snapshots are prefixed with `_expected`
- Actual (newly generated) screenshots are prefixed with `_actual`

- If the visual changes are intentional and acceptable:
- Delete the corresponding `_expected` snapshot
- Re-run the test to generate a new baseline snapshot
- Commit the the changed files

#### Adding visual regression tests for a new page

To add a visual regression test for a new page:

- Use the `assert_matches_snapshot` helper function
- Run the test once to generate the initial snapshot

```python
def test_my_page(page: Page):
    page.goto("/my_page")
    assert_is_accessible(page)
```

    If the page is accessible, the console won't output anything other than the usual test output. If there are accessibility issues, there will be output that explains what the issues are and also helpful links explaining how to fix them.

#### Test traces in CI

If there are failing tests in the end to end tests, there will be test traces available as artifacts in Github. Download the zipfile, extract a failing test file from inside (also a zip) and drag it onto the [Playwright Trace Viewer](https://trace.playwright.dev/)

### Viewing code coverage

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

### Setting up the pre-commit hooks (strongly advised)

To use this, you will need to install [pre-commit](https://pre-commit.com/) on your development machine, typically using `pip install pre-commit`. If you prefer Homebrew, you can use `brew install pre-commit`.

Install the git hooks configured in `.pre-commit-config.yaml` with:

`pre-commit install`

This will set up various checks including Python linting and style checks when you commit and push to the repo and alert you to any linting issues that will cause CI to fail.

### Setting up commit signing

Any commit that's merged to `main` needs to be [signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits), to ensure the identity of the author is who they say they are.

We recommend signing with your ssh key, as it's probably the easiest method of doing so. Assuming you already have an ssh key created, just follow the following steps:

- Add your SSH key as a _signing key_ in your [github account](https://github.com/settings/keys) - note this is different to an _authentication key_, which you likely already have set up. You can use the same key for both purposes, but you need to add it separately for each one twice.
- In your terminal, run the following commands. This assumes you want to set up commit signing by default for all repositories. If you don't want this for whatever reason, leave out the `--global` flag (but in that case you'll have to remember to repeat these steps in every TNA repository you work on):
  - Enable signing with `git config --global commit.gpgsign true`
  - Specify that we'll use SSH for signing with: `git config --global gpg.format ssh`
  - Specify the key you'll use to sign. If it's not id_rsa.pub, give the correct path here: `git config --global user.signingkey ~/.ssh/id_rsa.pub`

If you have already made some unsigned commits on a branch before setting up signing, you'll need to sign them before they can be merged. You can do this by rebasing, typically using for example `git rebase --force-rebase main` then doing a force push. Care should obviously be taken here however, especially if there's anyone else working on your branch!

## Front end development

### Pre-requisites

- Ensure you have NodeJS & NPM installed.

### Dependencies in this repository

Install these with:

```console
npm i
```

- Webpack and Babel for transpiling JavaScript
- Sass for compiling CSS

### Working with local copies of shared `nationalarchives/ds-caselaw-frontend`

To use a local development copy of `nationalarchives/ds-caselaw-frontend`, for example to use your local copy of the shared CSS instead of what's currently in its github repo's main branch:

```console
npm link ../path/to/your/copy/nationalarchives/ds-caselaw-frontend
```

To stop using your local copy, you can then run:

```console
npm unlink ../path/to/your/copy/nationalarchives/ds-caselaw-frontend
```

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

### Working with Storybook for Django/Ninja Components

In a new terminal session run `npm run storybook`

Storybook 8 for html-webpack5 should then start automatically. You can access it in your browser at <http://localhost:6006>.

The repository also publishes Storybook to GitHub Pages using [.github/workflows/publish-storybook.yml](.github/workflows/publish-storybook.yml), which is intended to provide a stable, shareable URL for design interaction.

After GitHub Pages is enabled for this repository (Settings > Pages > Build and deployment: GitHub Actions), the live URL will be:

<https://nationalarchives.github.io/ds-caselaw-public-ui/>

## A note on running `django` commands locally

django commands need to be run within the `django` docker container, not on your machine itself, so from your terminal, you will need to first run `fab sh`, which will give you a console where you can run commands within the container (you'll see your terminal change from saying something like `tim@Tims-Macbook` at the start of each line to `root@abcde12345`). You can then run the commands you need to (such as `python manage.py shell_plus`), and when you're done, type the command `exit` to exit back out to your own machine again (the start of each line will change back).

## Adding or removing stop words from the search

Anyone with access to the Github repo can add or remove stop words from the search.

1. Edit `judgments/fixtures/stop_words.py` to add or remove stop words as desired. Pay attention to the file format -
   the stop words must be in a Python list, quoted and followed by a comma.
2. Commit your changes to the repo and open a pull request as normal.
3. Once the PR is merged, the modified list of stop words will be used in the search.

## Local setup hints

1. Remember to `git pull` the freshest files
2. If `fab build` fails early, check that Docker is running? (Click the blue whale)
3. If the public-ui takes forever to load, that usually means it can't connect to MarkLogic.
   Check that MarkLogic or the VPN is running.
4. If it was working, and you `git pull`ed, and now it isn't, re-run `fab build`.
5. If it's saying environment variables aren't set (especially after a `git pull`), you might need
   to add lines to `.env` -- take them from `.env.example`.

## Deployment

<!-- last_review: 2026-04-08 -->

See the [deployment documentation](docs/DEPLOY.md).
