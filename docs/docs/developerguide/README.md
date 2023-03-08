# Developer guide

## Architecture
```
├── .github/workflows/    # github actions workflow files
├── teamware/             # Django project
│   └── settings/
├── backend/              # Django app
├── charts/               # Helm charts for Kubernetes
├── cypress/              # integration test configurations
├── docs/                 # documentation
├── examples/             # example data files
├── frontend/             # all frontend, in VueJS framework
├── nginx/                # Nginx configurations
|
# Top level directory contains scripts for management and deployment,
# main project package.json, python requirements, docker configs
├── build-images.sh
├── deploy.sh
├── create-django-db.sh
├── docker-compose.yml
├── Dockerfile
├── generate-docker-env.sh
├── manage.py
├── migrate-integration.sh
├── package.json
├── package-lock.json
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
└── run-server.sh

```

## Installation for development

The service depends on a combination of python and javascript libraries. We recommend developing inside a `conda` conda environment as it is able to install
python libraries and nodejs which is used to install javascript libraries.

* Install anaconda/miniconda
* Create a blank virtual conda env
  ```bash
  $ conda create -n teamware python=3.9
  ```
* Activate conda environment
  ```bash
  $ source activate teamware
  # or
  $ conda activate teamware
  ```
* Install python dependencies in conda environment using pip
  ```bash
  (teamware)$ pip install -r requirements.txt -r requirements-dev.txt
  ```
* Install nodejs, postgresql and openssl in the conda environment
  ```bash
  (teamware)$ conda install -y -c conda-forge postgresql=14.*
  (teamware)$ conda install -y -c conda-forge nodejs=14.*
  ```
* Install nodejs dependencies
  ```bash
  (teamware)$ npm install
  ```

Set up a new postgreSQL database and user for development:
```
# Create a new directory for the db data and initialise
mkdir -p pgsql/data
initdb -D pgsql/data

# Launch postgres in the background
postgres -p 5432 -D pgsql/data &

# Create a DB user, you'll be prompted to input password, "password" is the default in teamware/settings/base.py for development
createuser -p 5432 -P user --createdb

# Create a rumours_db with rumours as user
createdb -p 5432 -O user teamware_db

# Migrate & create database tables
python manage.py migrate

# create a new superuser - when prompted enter a username and password for the db superuser
python manage.py createsuperuser
```

## Updating packages
To update packages after a merge, run the following commands:

```bash
# Activate the conda environment
source activate teamware
# Update any packages changed in the python requirements.txt and requirements-dev.txt files
pip install -r requirements.txt -r requirements-dev.txt
# Update any packages changed in package.json
npm install
```

## Development server
The application uses django's dev server to serve page contents and run the RPC API, it also uses Vue CLI's 
development server to serve dynamic assets such as javascript or stylesheets allowing for hot-reloading
during development.

To run both servers together:

  ```bash
  npm run serve
  ```

To run separately:

* Django server
  ```bash
  npm run serve:backend
  ```
* Vue CLI dev server
  ```bash
  npm run serve:frontend
  ```

## Deployment using Docker
Teamware can be deployed via [docker-compose](https://docs.docker.com/compose/), using [NGINX](https://www.nginx.com/) to serve static content, a separate [postgreSQL](https://hub.docker.com/_/postgres) service containing the database and a database backup service (see `docker-compose.yml` for details).

1. Run `./generate-docker-env.sh` to create a `.env` file containing randomly generated secrets which are mounted as environment variables into the container. See [below](#env-config) for details.

2. Then build the images via:
  ```bash
  ./build-images.sh
  ```

3. then deploy the stack with

  ```bash
  ./deploy.sh production # (or prod) to deploy with production settings
  ./deploy.sh staging # (or stag) to deploy with staging settings
  ```

To bring the stack down, run `docker-compose down`, using the `-v` flag to destroy the database volume (be careful with this).

### Configuration using environment variables (.env file)<a id="env-config"></a>

To allow the app to be easily configured between instances especially inside containers, many of the app's configuration can be done through environment variables.

Run `./generate-docker-env.sh` to generate a `.env` file with all configurable environment parameters.

To set values for your own deployment, add values to the variables in `.env`, most existing values will be kept after running `generate-docker-env.sh`, see comments in `.env` for specific details. Anything that is left blank will be filled with a default value. Passwords and keys are filled with auto-generated random values.

Existing `.env` files are copied into a new file named `saved-env.<DATE-TIME>` by `generate-docker-env.sh`.

### Backups

In a docker-compose based deployment, backups of the database are managed by the service `pgbackups` which uses the [`prodrigestivill/postgres-backup-local:12`](https://hub.docker.com/r/prodrigestivill/postgres-backup-local) image.
By default, backups are taken of the database daily, and the `docker-compose.yml` contains settings for the number of backups kept under the options for the `pgbackups` service.
Backups are stored as a gzipped SQL dump from the database.

#### Taking a manual backup

A shell script is provided for manually triggering a backup snapshot.
From the main project directory run

```sh
$ ./backup_manual.sh
```

This uses the `pgbackups` service and all settings and envrionment variables it is configured with in `docker-compose.yml`, so backups will be taken to the same location as configured for the main backup schedule.

#### Restoring from a backup
1. Locate the backup file (`*.sql.gz`) on your system that you would like to restore from.
2. Make sure that the stack is down, from the main project directory run `docker-commpose down`.
3. Run the backup restore shell script, passing in the path to your backup file as the only argument:

```sh
$ ./backup_restore.sh path/to/my/backup.sql.gz
```

This will first launch the database container, then via Django's `dbshell` command, running in the `backend` service, execute a number of SQL commands before and after running all the SQL from the backup file.

4. Redeploy the stack, via `./deploy.sh staging` or `./deploy.sh production`, whichever is the case.
5. The database *should* be restored.


## Deployment using Kubernetes

A Helm chart to deploy Teamware on Kubernetes is published to the GATE team public charts repository.  The chart requires [Helm](https://helm.sh) version 3.7 or later, and is compatible with Kubernetes version 1.23 or later.  Earlier Kubernetes versions back to 1.19 _may_ work provided autoscaling is not enabled, but these have not been tested.

The following quick start instructions assume you have a compatible Kubernetes cluster and a working installation of `kubectl` and `helm` (3.7 or later) with permission to create all the necessary resource types in your target namespace.

First generate a random "secret key" for the Django application.  This must be at least 50 random characters, a quick way to do this is

```
# 42 random bytes base64 encoded becomes 56 random characters
kubectl create secret generic -n {namespace} django-secret \
   --from-literal="secret-key=$( openssl rand -base64 42 )"
```

Add the GATE charts repository to your Helm configuration:

```
helm repo add gate https://repo.gate.ac.uk/repository/charts
helm repo update
```

Create a `values.yaml` file with the key settings required for teamware.  The following is a minimal set of values for a typical installation:

```yaml
# Public-facing web hostname of the teamware application, the public
# URL will be https://{hostName}
hostName: teamware.example.com

email:
  # "From" address on emails sent by Teamware
  adminAddress: admin@teamware.example.com
  # Send email via an SMTP server - alternatively "gmail" to use GMail API
  backend: "smtp"
  smtp:
    host: mail.example.com
    # You will also need to set user and passwordSecret if your
    # mail server requires authentication

privacyPolicy:
# Contact details of the host and administrator of the teamware instance, if no admin defined, defaults to the host values.
  host:
    # Name of the host
    name: "Service Host"
    # Host's physical address
    address: "123 Example Street, City. Country."
    # A method of contacting the host, field supports HTML for e.g. linking to a form
    contact: "<a href='mailto:info@examplehost.com'>Email</a>"
  admin:
    name: "Service Host"
    address: "123 Example Street, City. Country."
    contact: "<a href='mailto:info@examplehost.com'>Email</a>"

backend:
  # Name of the random secret you created above
  djangoSecret: django-secret

# Initial "super user" created on the first install.  These are just
# the *initial* settings, you can (and should!) change the password
# once Teamware is up and running
superuser:
  email: me@example.com
  username: admin
  password: changeme
```

Some of these may be omitted or others may be required depending on the setup of your specific cluster - see the [chart README](https://github.com/GateNLP/charts/blob/main/gate-teamware/README.md) and the chart's own values file (which you can retrieve with `helm show values gate/gate-teamware`) for full details.  In particular these values assume:

- your cluster has an ingress controller, with a default ingress class configured, and that controller has a default TLS certificate that is compatible with your chosen hostname (e.g. a `*.example.com` wildcard)
- your cluster has a default storageClass configured to provision PVCs, and at least 8 GB of available PV capacity
- you can send email via an SMTP server with no authentication
- you do not need to back up your PostgreSQL database - the chart does include the option to store backups in Amazon S3 or another compatible object store, see the full README for details

Once you have created your values file, you can install the chart or upgrade an existing installation using

```
helm upgrade --install gate-teamware gate/gate-teamware \
       --namespace {namespace} --values teamware-values.yaml
```

## Configuration

### Django settings files

Django settings are located in `teamware/settings` folder. The app will use `base.py` setting by default
and this must be overridden depending on use.

### Database
A SQLite3 database is used during development and during integration testing.

For staging and production, postgreSQL is used, running from a `postgres-12` docker container. Settings are found in `teamware/settings/base.py` and `deployment.py` as well as being set as environment variables by `./generate-docker-env.sh` and passed to the container as configured in `docker-compose.yml`.

In Kubernetes deployments the PostgreSQL database is installed using the Bitnami `postresql` public chart. 


### Sending E-mail 
It's recommended to specify e-mail configurations through environment variables (`.env`). As these settings will include username and passwords that should not be tracked by version control.

#### E-mail using SMTP
SMTP is supported as standard in Django, add the following configurations with your own details
to the list of environment variables:

```bash
DJANGO_EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
DJANGO_EMAIL_HOST='myserver.com'
DJANGO_EMAIL_PORT=22
DJANGO_EMAIL_HOST_USER='username'
DJANGO_EMAIL_HOST_PASSWORD='password'
```

#### E-mail using Google API
The [django-gmailapi-backend](https://github.com/dolfim/django-gmailapi-backend) library
has been added to allow sending of mail through Google's API as sending through SMTP is disabled as standard.

Unlike with SMTP, Google's API requires OAuth authentication which means a project and a credential has to be 
created through Google's cloud console.

* More information on the Gmail API: [https://developers.google.com/gmail/api/guides/sending](https://developers.google.com/gmail/api/guides/sending)
* OAuth credentials for sending emails: [https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough](https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough)

This package includes the script linked in the documentation above, which simplifies the setup of the API credentials. The following outlines the key steps:

1. Create a project in the Google developer console, [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Enable the Gmail API
3. Create OAuth 2.0 credentials, you'll likely want to create a `Desktop` 
4. Create a valid refresh_token using the helper script included in the package:
  ```bash
  gmail_oauth2 --generate_oauth2_token \
    --client_id="<client_id>" \
    --client_secret="<client_secret>" \
    --scope="https://www.googleapis.com/auth/gmail.send"
  ```
5. Add the created credentials and tokens to the environment variable as shown below:
  ```bash
  DJANGO_EMAIL_BACKEND='gmailapi_backend.mail.GmailBackend'
  DJANGO_GMAIL_API_CLIENT_ID='google_assigned_id'
  DJANGO_GMAIL_API_CLIENT_SECRET='google_assigned_secret'
  DJANGO_GMAIL_API_REFRESH_TOKEN='google_assigned_token'
  ```


#### Teamware Privacy Policy and Terms & Conditions

Teamware includes a default privacy policy and terms & conditions, which are required for running the application.

The default privacy policy is compliant with UK GDPR regulations, which may comply with the rights of users of your deployment, however it is your responsibility to ensure that this is the case.

If the default privacy policy covers your use case, then you will need to include configuration for a few contact details.

Contact details are required for the **host** and the **administrator**: the **host** is the organisation or individual responsible for managing the deployment of the teamware instance and the **administrator** is the organisation or individual responsible for managing users, projects and data on the instance. In many cases these roles will be filled by the same organisation or individual, so in this case specifying just the **host** details is sufficient.

For deployment from source, set the following environment variables:

* `PP_HOST_NAME`
* `PP_HOST_ADDRESS`
* `PP_HOST_CONTACT`
* `PP_ADMIN_NAME`
* `PP_ADMIN_ADDRESS`
* `PP_ADMIN_CONTACT`

For deployment using docker-compose, set these values in `.env`.

##### Including a custom Privacy Policy and/or Terms & Conditions

If the default privacy policy or terms & conditions do not cover your use case, you can easily replace these with your own documents.

If deploying from source, include HTML files in a `custom-policies` directory in the project root with the exact names `custom-policies/privacy-policy.html` and/or `custom-policies/terms-and-conditions.html` which will be rendered at the corresponding pages on the running web app.

If deploying with docker compose, place files with these names at the same location as the `docker-compose.yml` file before running `./deploy.sh` as above.

An example custom privacy policy file contents might look like:

```html
<h1>Organisation X Teamware Privacy Policy</h2>
...
...
<h2>Definitions of Roles and Terminology</h2>
...
...
```