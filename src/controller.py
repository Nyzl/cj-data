import os, logging
from retrying import retry
from flask import Flask, request, render_template
from report import Report
import epi_report, ga_data

app = Flask(__name__)
port = os.environ.get('PORT') 

#  create all the report objects

reports = {
           "epi_public" : Report(name="epi_public", source="epi", dest="", site="public"),
           "epi_adviser" : Report(name="epi_adviser", source="epi", dest="", site="advisernet"),
           "ga_public_rating" : Report(name="ga_public_rating", source="ga", dest="", site="public", source_args="rating"),
           "ga_public_size" : Report(name="ga_public_size", source="ga", dest="", site="public", source_args="size"),
           "ga_adviser_rating" : Report(name="ga_adviser_rating", source="ga", dest="", site="advisernet", source_args="rating"),
           "ga_adviser_size" : Report(name="ga_adviser_size", source="ga", dest="", site="advisernet", source_args="size")
}

#  take the report source and map it to a function
sources = {
    "epi": epi_report.epi_pages_report,
    "ga":ga_data.get_ga_report
}

#  retry wrapper for functions
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,stop_max_attempt_number=10)
def retry_wrap(fn):
    try:
        fn

    except Exception as err:
        logging.error(err)
        print(str(err))
        raise err

#  define endpoints
@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/report')
def rpt():
    rt = request.args.get('report')
    if rt in reports:
        r = reports[rt]
        r.source_fn = sources[r.source]
        retry_wrap(r.get_data())
        r.clean_data()
        retry_wrap(r.send_data())

        return  "completed " + rt

    else:
        return "did you get the report name right?"

    return "All done"



@app.route('/test')
def test():
    reports = reports
    # get last upload date
    return render_template('index.html', title='Home', reports=reports)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
