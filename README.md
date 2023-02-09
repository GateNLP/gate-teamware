# GATE Teamware

![](/frontend/public/static/img/gate-teamware-logo.svg "GATE Teamware")

A web application for collaborative document annotation. 

Full documentation can be [found here][docs].

GATE teamware provides a flexible web app platform for managing classification of documents by human annotators.

## Key Features
* Configure annotation options using a highly flexible JSON config.
* Set limits on proportions of a task that annotators can annotate.
* Import existing annotations as CSV or JSON.
* Export annotations as CSV or JSON.
* Annotation instructions and document rendering supports markdown and HTML.
* Deploy with [kubernetes](https://kubernetes.io/) or [docker compose](https://docs.docker.com/compose/).

# Running the app
## Requirements
We recommend the following software as a minimum requirement for running GATE Teamware:
* recommended OS: linux or macOS.
* [git](http://git-scm.com/)
* [docker](https://www.docker.com/) & [docker-compose](https://docs.docker.com/compose/)
* [bash](https://www.gnu.org/software/bash/)

## Instructions
Follow these steps to run the app on your local machine using `docker-compose`:
1. Clone this repository by running `git clone https://github.com/GateNLP/gate-teamware.git` and move into the `gate-teamware` directory.
1. From inside the `gate-teamware` directory run `./generate-docker-env.sh` to create a set of passwords and keys in a `.env` file.
1. Run `./build-images.sh` to build the backend and frontend images, this may take a while the first time it is run. 
1. Run `./deploy.sh production` or `./deploy.sh staging`. Note: You may want to change the value of `DJANGO_ALLOWED_HOSTS` in `deploy.sh` to match the URL(s) that you are deploying to.

Open `127.0.0.1:8076` (the default IP & port) in your browser. The initial admin login has the username `admin` and password `password`, this should be changed immediately. Note: the port is set in `docker-compose.yml`.


*Notes on deployment*:
* A development server can be run without docker, see the [developer documentation][dev-docs] for more info.
* The app can also be deployed on a kubernetes cluster, helm charts are available in the `charts/` directory.

# Development
Developer documentation is [provided here][dev-docs].

# Contribution
We welcome contributions to this open source project. Please [create a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of this repository and make a pull request against the `dev` branch with your changes.

# Using Teamware
Teamware is developed by the [GATE](https://gate.ac.uk) team, an academic research group at The University of Sheffield. As a result, future funding relies on evidence of the impact that the software provides. If you use Teamware, please let us know using the contact form at [gate.ac.uk](https://gate.ac.uk/g8/contact). Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.

## Citation
For published work that has used Teamware, please cite this repository. One way is to include a citation such as:

> Karmakharm, T., Wilby, D., Roberts, I., & Bontcheva, K. (2022). GATE Teamware (Version 0.1.4) [Computer software]. https://github.com/GateNLP/gate-teamware

Please use the `Cite this repository` button at the top of the [project's GitHub repository](https://github.com/GATENLP/gate-teamware) to get an up to date citation.


[docs]: https://gatenlp.github.io/gate-teamware/
[dev-docs]: https://gatenlp.github.io/gate-teamware/development/developerguide/
