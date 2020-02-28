
.PHONY: build deploy

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
