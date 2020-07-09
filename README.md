# Content prioritisation data pipeline

This is a Python project that collects data from various sources and sends them to Big Query.
A mini data pipeline type of thing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment-to-google-cloud-run) for notes on how to deploy the project. 

Please read if you plan on contributing to the project:
[Code of conduct for this project](docs/CODE_OF_CONDUCT.md)
and
[Contribution guidelines for this project](docs/CONTRIBUTING.md)

### Prerequisites

You will need a Google Cloud account, [Google Cloud SDK](https://cloud.google.com/sdk) and [Docker](https://www.docker.com/).
Make sure you hace gcloud installed and run `gcloud auth configure-docker`

## Environments

### Installing locally

To use a local development environment you will have to download a new service account keyfile that has read permission to Google Cloud Storage.
You will also have to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the location of that keyfile.
eg `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/file.json`

### Hosted environjment on Goog Cloud Run

A Dockerfile is used to define the hosted environment on Google CLoud run 

The Dockerfile details all the required environment variables:

`gcp_project` this is the Google Cloud project

`bq_dataset` this is the data set to send data to

`advisernet_ga` this is used with `ga_data.py` to get GA data for Advisernet

`public_ga` this is used with `ga_data.py` to get GA data for the Public site

`all_ga` this is used with `ga_data.py` to get GA data for all sites


The contents of folders `creds` and `store` will not be committed to git or included in the Docker image. The intention is that `creds` can be used to locally store credential files and `store` can be used as a local store for data files.


## Deployment to Google Cloud Run

Deployment is handled via the Makefile:

`make build` - Builds the image on [Google Container Repository](https://cloud.google.com/container-registry)

`make deploy` - Deploys the image on [Google Cloud Run](https://cloud.google.com/run)

`make dev-build` - Builds a development image on Google Container Repository

`make dev-deploy` - Deploys the development image and overwrites the env variable for the BQ dataset to write to test tables rather than writing to the production tables



## The code

this bit will explain how it all works, but it's yet to be written


## Authors

**Ian Ansell** - *Initial work* - [Nyzl](https://github.com/Nyzl)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

[Alec Johnson](https://github.com/MrAlecJohnson) for helping with the alpha of this codebase and for being a general sounding board throughout the development.
[Daniel Nissenbaum](https://github.com/danielnissenbaum) for help getting the code and documentation into something approaching maintainable


