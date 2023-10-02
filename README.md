# GATE Teamware

![](/frontend/public/static/img/gate-teamware-logo.svg "GATE Teamware")

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7899193.svg)](https://doi.org/10.5281/zenodo.7899193)

A web application for collaborative document annotation. 

Full documentation can be [found here][docs].

GATE Teamware provides a flexible web app platform for managing classification of documents by human annotators.

## Key Features
* Configure annotation options using a highly flexible JSON config.
* Set limits on proportions of a task that annotators can annotate.
* Import existing annotations as CSV or JSON.
* Export annotations as CSV or JSON.
* Annotation instructions and document rendering supports markdown and HTML.
* Deploy with [kubernetes](https://kubernetes.io/) or [docker compose](https://docs.docker.com/compose/).

# Running the app

## Latest release

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

[A Helm chart](https://github.com/GateNLP/charts/tree/main/gate-teamware) is also available to allow deployment on Kubernetes.

### Upgrading

**When upgrading GATE Teamware it is strongly recommended to ensure you have a recent backup of your database before starting the upgrade procedure.**  Database schema changes should be applied automatically as part of the upgrade but unexpected errors may cause data corruption - **always** take a backup before starting any significant changes to your database, so you can roll back in the event of failure.

Check the [changelog](CHANGELOG.md) - any breaking changes and special considerations for upgrades to particular versions will be documented there.

To upgrade a GATE Teamware installation that you installed using `get-teamware.sh`, simply download and run the latest version of the script in the same folder.  It will detect your existing configuration and prompt you for any new settings that have been introduced in the new version.  Note that any manual changes you have made to the `docker-compose.yml` and other files will not be duplicated automatically for the new version, you will have to port the necessary changes to the new files by hand.

Upgrading a Kubernetes deployment generally consists simply of installing the new chart version with `help upgrade`.  As above, check the GATE Teamware changelog and the [chart readme](https://github.com/GateNLP/charts/tree/main/gate-teamware) for any special considerations, new or changed configuration values, etc. and ensure you have a recent database backup before starting the upgrade process.

## Building locally
Follow these steps to run the app on your local machine using `docker-compose`:
1. Clone this repository by running `git clone https://github.com/GateNLP/gate-teamware.git` and move into the `gate-teamware` directory.
1. From inside the `gate-teamware` directory run `./generate-docker-env.sh` to create a set of passwords and keys in a `.env` file.
1. Run `./build-images.sh` to build the backend and frontend images, this may take a while the first time it is run.  Images are built using `docker buildx`, which requires Docker Engine 19.03 or later.
1. Run `./deploy.sh production` or `./deploy.sh staging`. Note: You may want to change the value of `DJANGO_ALLOWED_HOSTS` in `deploy.sh` to match the URL(s) that you are deploying to.

Open `127.0.0.1:8076` (the default IP & port) in your browser. The initial admin login has the username `admin` and password `password`, this should be changed immediately. Note: the port is set in `docker-compose.yml`.


*Notes on deployment*:
* A development server can be run without docker, see the [developer documentation][dev-docs] for more info.
* [A Helm chart](https://github.com/GateNLP/charts/tree/main/gate-teamware) is available to deploy GATE Teamware on a kubernetes cluster.

# Development
Developer documentation is [provided here][dev-docs].

# Contribution
We welcome contributions to this open source project. Please [create a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of this repository and make a pull request against the `dev` branch with your changes.

# Using Teamware
Teamware is developed by the [GATE](https://gate.ac.uk) team, an academic research group at The University of Sheffield. As a result, future funding relies on evidence of the impact that the software provides. If you use Teamware, please let us know using the contact form at [gate.ac.uk](https://gate.ac.uk/g8/contact). Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.

## Citation
For published work that has used Teamware, please cite this repository. One way is to include a citation such as:

> Karmakharm, T., Wilby, D., Roberts, I., & Bontcheva, K. (2022). GATE Teamware (Version 2.1.1) [Computer software]. https://github.com/GateNLP/gate-teamware

Please use the `Cite this repository` button at the top of the [project's GitHub repository](https://github.com/GATENLP/gate-teamware) to get an up to date citation.


[docs]: https://gatenlp.github.io/gate-teamware/
[dev-docs]: https://gatenlp.github.io/gate-teamware/development/developerguide/
