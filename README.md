# GATE Teamware

![](/frontend/public/static/img/gate-teamware-logo.svg "GATE Teamware")

A web application for collaborative document annotation. 

Full documentation can be found at: <https://gatenlp.github.io/gate-teamware/>

GATE teamware provides a flexible web app platform for managing classification of documents by human annotators.

# Running the app
## Requirements
We recommend the following software as a minimum requirement for running GATE Teamware:
* OS: Linux
* git
* docker & docker-compose
* bash (or similar shell)

## Instructions
Follow these steps to run the app on your local machine:
1. Clone this repository by running `git clone https://github.com/GateNLP/gate-teamware.git` and move into the `gate-teamware` directory.
1. From inside the `gate-teamware` directory run `./generate-env.sh` to create a set of passwords and keys in a `.env` file.
1. Run `./build-images.sh` to build the backend and frontend images, this may take a while the first time it is run. 
1. Run `./deploy.sh production` or `./deploy.sh staging`. Note: You may want to change the value of `DJANGO_ALLOWED_HOSTS` in `deploy.sh` to match the URL(s) that you are deploying to.

Open `127.0.0.1:8076` (the default IP & port) in your browser. The initial admin login has the username `admin` and password `password`, this should be changed immediately.`


# Development
Developer documentation is provided at <https://gatenlp.github.io/gate-teamware/developerguide/>.

# Contribution
We welcome contributions to this open source project. Please create a fork of this repository and make a pull request against it with your changes.





[docs]: https://gatenlp.github.io/gate-teamware/