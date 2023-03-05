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

## Bug reports and feature requests
Please make bug reports and feature requests as Issues on the [GATE Teamware GitHub repo](https://github.com/GATENLP/gate-teamware).

# Using Teamware
Teamware is developed by the [GATE](https://gate.ac.uk) team, an academic research group at The University of Sheffield. As a result, future funding relies on evidence of the impact that the software provides. If you use Teamware, please let us know using the contact form at [gate.ac.uk](https://gate.ac.uk/g8/contact). Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.

## Citation
For published work that has used Teamware, please cite this repository. One way is to include a citation such as:

> Karmakharm, T., Wilby, D., Roberts, I., & Bontcheva, K. (2022). GATE Teamware (Version 0.1.4) [Computer software]. https://github.com/GateNLP/gate-teamware

Please use the `Cite this repository` button at the top of the [project's GitHub repository](https://github.com/GATENLP/gate-teamware) to get an up to date citation.

The Teamware version can be found on the 'About' page of your Teamware instance.
