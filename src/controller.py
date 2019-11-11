import time, logging, os
from retrying import retry
from flask import Flask

from settings import report
import epi_report, ga_data

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

#take the report source and map it to a function
sources = {
    "epi": epi_report.epi_pages_report,
    "ga":ga_data.get_ga_report
}

#define key functions
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,stop_max_attempt_number=10)
def retry(fn):
    try:
        fn

    except Exception as err:
        logging.error(err)
        raise err


def get(r):
    r.source_fn = sources[r.source]
    retry(r.get_data())


def send(r):
    retry(r.send_data())


#the uri to set things running
@app.route('/')
def go():
    for r in reports:
        get(r)
        send(r)
    return ("all done")





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
