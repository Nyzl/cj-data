
.PHONY: build deploy local

PORT=8080
project=customerjourney-214813/cj-data
dev_project=customerjourney-214813/cj-data-test
keyfile=/Users/Ian/Documents/GitHub/cj-data/creds/cj_data.json

build:
	gcloud builds submit \
	--tag gcr.io/${project}

deploy:
	gcloud run deploy \
	--platform managed \
	--image gcr.io/${project} \
	--service-account cj-datapipeline@customerjourney-214813.iam.gserviceaccount.com \
	--memory 2Gi

dev-build:
	gcloud builds submit \
	--tag gcr.io/${dev_project}

dev-deploy:
	gcloud run deploy \
	--platform managed \
	--image gcr.io/${dev_project} \
	--service-account cj-datapipeline@customerjourney-214813.iam.gserviceaccount.com \
	--memory 2Gi \
	--update-env-vars bq_dataset=cj_data_test

local:
	PORT=8080 && docker run \
	-p 9090:${PORT} \
	-e PORT=${PORT} \
	-e K_SERVICE=dev \
	-e K_CONFIGURATION=dev \
	-e K_REVISION=dev-00001 \
	-v ${keyfile}:/cj-data/creds/cj_data.json:ro \
	-e GOOGLE_APPLICATION_CREDENTIALS=/cj-data/creds/cj_data.json \
	gcr.io/${dev_project}

pull:
	docker pull gcr.io/${dev_project}

compose:
	docker-compose up \ 
	-e GOOGLE_APPLICATION_CREDENTIALS=/cj-data/creds/cj_data.json