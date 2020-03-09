
.PHONY: build deploy

PORT=8080
project=/customerjourney-214813/cj-datatest
dev_project=customerjourney-214813/cj-data-test

build:
	gcloud builds submit \
	--tag gcr.io/customerjourney-214813/cj-data

deploy:
	gcloud run deploy \
	--platform managed \
	--image gcr.io/customerjourney-214813/cj-data \
	--service-account cj-datapipeline@customerjourney-214813.iam.gserviceaccount.com \
	--memory 500M


dev-build:
	gcloud builds submit \
	--tag gcr.io/customerjourney-214813/cj-data-test

dev-deploy:
	gcloud run deploy \
	--platform managed \
	--image gcr.io/customerjourney-214813/cj-data-test \
	--service-account cj-datapipeline@customerjourney-214813.iam.gserviceaccount.com \
	--memory 500M \
	--update-env-vars bq_dataset=cj_data_test

test: 
	PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} gcr.io/customerjourney-214813/cj-data-test

test2:
	sudo docker pull gcr.io/${dev_project}

test3:
	PORT=8080 && docker run \
	-p 9090:${PORT} \
	-e PORT=${PORT} \
	-e K_SERVICE=dev \
	-e K_CONFIGURATION=dev \
	-e K_REVISION=dev-00001 \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/FILE_NAME.json \
	-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/FILE_NAME.json:ro \
	gcr.io/PROJECT_ID/IMAGE
