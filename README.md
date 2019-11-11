# Content prioritisation data pipeline

This project collects data from various sources and sends them to Big Query

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need Docker installed.


### Installing

A step by step series of examples that tell you how to get a development env running

The following ENV variables are needed and can be supplied in a .env file
```
export epiname=xxxx
export epipass=xxxx

export gcp_project=xxxx
export bq_dataset=xxxx

export advisernet_ga=xxxx
export public_ga=xxxx
export all_ga=xxxx

export key_file_name=xxxx

export public_epi=xxxx
export advisernet_epi=xxxx
```
Build the Docker image with: 
```docker build -t pipeline .```

Run the docker container, this will start Flask:
```docker run pipeline```

Flack is listening on port 8080



## The code

Setting.py defines a report object wit the following properties:
```
name
data
source
site
source_args
dest
status
source_fn
```
And the following methods:
```
get_data()
send_data()
clean_data()
save_data()
```

Report object have a status:


## Authors

* **Ian Ansell** - *Initial work* - [Nyzl](https://github.com/Nyzl)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Alec Johnson for helping wit the alpha of this codebase
