# GATE Teamware

![GATE Teamware logo](./img/gate-teamware-logo.svg "GATE Teamware logo")

A web application for collaborative document annotation.

This is a documentation for Teamware version: <strong><DisplayVersion></DisplayVersion></strong>

## Key Features
* Free and open source software.
* Configure annotation options using a highly flexible JSON config.
* Set limits on proportions of a task that annotators can annotate.
* Import existing annotations as CSV or JSON.
* Export annotations as CSV or JSON.
* Annotation instructions and document rendering supports markdown and HTML.

## Getting started
A quickstart guide for annotators is [available here](annotatorguide).

To use an existing instance of GATE Teamware as a project manager or admin, find instructions in the [Managers and Admins guide](manageradminguide).

Documentation on deploying your own instance can be found in the [Developer Guide](developerguide).

## Installation Guide

### Quick Start

The simplest way to deploy your own copy of GATE Teamware is to use Docker Compose on Linux or Mac.  Installation on Windows is possible but not officially supported - you need to be able to run `bash` shell scripts for the quick-start installer.

1. Install Docker - [Docker Engine](https://docs.docker.com/engine/) for Linux servers or [Docker Desktop](https://docs.docker.com/desktop/) for Mac.
2. Install [Docker Compose](https://github.com/docker/compose), if your Docker does not already include it (Compose is included by default with Docker Desktop)
3. Download the [installation script](https://gate.ac.uk/get-teamware.sh) into an empty directory, run it and follow the instructions.

```
mkdir gate-teamware
cd gate-teamware
curl -LO https://gate.ac.uk/get-teamware.sh
bash ./get-teamware.sh
```

### Deployment using Kubernetes

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
  # Contact details of the host and administrator of the teamware
  # instance, if no admin defined, defaults to the host values.
  host:
    # Name of the host
    name: "Service Host"
    # Host's physical address
    address: "123 Example Street, City. Country."
    # A method of contacting the host, field supports HTML for e.g. linking to a form
    contact: "<a href='mailto:info@examplehost.com'>Email</a>"
  admin:
    name: "Dr. Service Admin"
    address: "Department of Example Studies, University of Example, City. Country."
    contact: "<a href='mailto:s.admin@example.ac.uk'>Email</a>"
    
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


## Bug reports and feature requests
Please make bug reports and feature requests as Issues on the [GATE Teamware GitHub repo](https://github.com/GATENLP/gate-teamware).

# Using Teamware
Teamware is developed by the [GATE](https://gate.ac.uk) team, an academic research group at The University of Sheffield. As a result, future funding relies on evidence of the impact that the software provides. If you use Teamware, please let us know using the contact form at [gate.ac.uk](https://gate.ac.uk/g8/contact). Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.

## Citation
For published work that has used Teamware, please cite this repository. One way is to include a citation such as:

> Karmakharm, T., Wilby, D., Roberts, I., & Bontcheva, K. (2022). GATE Teamware (Version 0.1.4) [Computer software]. https://github.com/GateNLP/gate-teamware

Please use the `Cite this repository` button at the top of the [project's GitHub repository](https://github.com/GATENLP/gate-teamware) to get an up to date citation.

The Teamware version can be found on the 'About' page of your Teamware instance.
