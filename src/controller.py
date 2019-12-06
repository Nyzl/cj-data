import time, logging, os
from retrying import retry
from flask import Flask

from report import Report
import epi_report, ga_data

import testing

app = Flask(__name__)
port = os.environ.get('PORT') 


#create all the report objects

reports = [
           Report(name="epi_public", source="epi", dest="", site="public"),
           Report(name="epi_adviser", source="epi", dest="", site="advisernet"),
           Report(name="ga_public_rating", source="ga", dest="", site="public", source_args="rating"),
           Report(name="ga_public_size", source="ga", dest="", site="public", source_args="size"),
           Report(name="ga_adviser_rating", source="ga", dest="", site="advisernet", source_args="rating"),
           Report(name="ga_adviser_size", source="ga", dest="", site="advisernet", source_args="size")
]

#take the report source and map it to a function
sources = {
    "epi": epi_report.epi_pages_report,
    "ga":ga_data.get_ga_report
}

#define key functions
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,stop_max_attempt_number=10)
def retry_wrap(fn):
    try:
        fn

    except Exception as err:
        logging.error(err)
        raise err


def get(r):
    r.source_fn = sources[r.source]
    retry_wrap(r.get_data())


def send(r):
    retry_wrap(r.send_data())


#the uri to set things running
@app.route('/')
def go():
    for r in reports:
        get(r)
        r.clean_data()
        r.save_data()
        #send(r)
    return "all done"

@app.route('/test')
def test():
    return testing.test2()




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
