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

### 1. Gain access to the marklogic image

Access to the marklogic Docker image is restricted to those who have 'purchased' it on Docker Hub. It's actually FREE to purchase, but you need to fill out [a short form](https://hub.docker.com/_/marklogic/purchase).

### 2. Create `.env`

```console
$ cp .env.example .env
```

### 3. Build Docker containers

```console
$ fab build
```

### 4. Start Docker containers

```console
$ fab start
```

### 5. Start a shell session with the 'django' container

```console
$ fab sh
```

### 6. Apply database migrations

```console
$ python manage.py migrate
```

### 7. Run a 'development' web server

```console
$ python manage.py runserver_plus 0.0.0.0:3000
```

### 8. Access the site

<http://127.0.0.1:3000>

**NOTE**: Compiled CSS is not included and therefore needs to be built initially, and after each git pull.

## Additional development tips

### Quick start with `fab run`

While it's handy to be able to access the django container via a shell and interact with it directly, sometimes all you want is to view the site in a web browser. In these cases, you can use:

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

### Running tests

```console
$ fab test
```

### Importing Judgments data

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

### Marklogic URL Guide

- http://localhost:8000/ this is the query interface where you can browse documents in the `Judgments` database.
- http://localhost:8001/ this is the management console where you can administer your database.
- http://localhost:8002/ this is the monitoring dashboard.
- http://localhost:8011/ this is the application server for the Marklogic REST interface
All four URLs use basic auth, username and passward are both `admin`.

### Using the pre-push hook (optional)

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

