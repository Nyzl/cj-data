# Content prioritisation data pipeline

This project collects data from various sources and sends them to Big Query.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Please read if you plan on contributing to the project:
[Code of conduct for this project](docs/CODE_OF_CONDUCT.md)
and
[Contribution guidelines for this project](docs/CONTRIBUTING.md)

### Prerequisites

You will need a Google Cloud account, the Google Cloud SDK and Docker.


### Installing locally

A step by step series of examples that tell you how to get a development env running

Currently there is no local development environment for the project. There is a cloud development environment instead, ensuring credentials are secure at all times. 

The Dockerfile details all the required environment variables:
`gcp_project` this is the Google Cloud project
`bq_dataset` this is the data set to send data to
`advisernet_ga` this is used with `ga_data.py` to get GA data for a specific profile
`public_ga` this is used with `ga_data.py` to get GA data for a specific profile
`all_ga` this is used with `ga_data.py` to get GA data for a specific profile


### Deployment to Google Cloud Run

Deployment is handled via the Makefile
`make build` - Builds the image on gcr
`make deploy` - Deploys the image on Cloud Run
`make dev-build` - Builds a development image on gcr
`make dev-deploy` - Deploys the development image and overwrites the env variable for the BQ dataset


## The code

this bit will explain how it works


## Authors

* **Ian Ansell** - *Initial work* - [Nyzl](https://github.com/Nyzl)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* @MrAlecJohnson for helping with the alpha of this codebase and for being a general sounding board throughout the development.


