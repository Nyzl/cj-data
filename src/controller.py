import time, logging
from retrying import retry
from settings import report
from flask import Flask

app = Flask(__name__)
port = os.environ.get('PORT') 


#create all the report objects

reports = [
           report(name="epi_public", source="epi", dest="", site="public"),
           report(name="epi_adviser", source="epi", dest="", site="advisernet"),
           report(name="ga_public_rating", source="ga", dest="", site="public", source_args="rating"),
           report(name="ga_public_size", source="ga", dest="", site="public", source_args="size"),
           report(name="ga_adviser_rating", source="ga", dest="", site="advisernet", source_args="rating"),
           report(name="ga_adviser_size", source="ga", dest="", site="advisernet", source_args="size")
]


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,stop_max_attempt_number=10)
def retry(fn):
    try:
        fn

    except Exception as err:
        logging.error(err)
        raise err



def get(r):
    retry(r.get_data())


def send(r):
    retry(r.send_data())

@app.route('/')
def go():
    for r in reports:
        get(r)
        send(r)





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
