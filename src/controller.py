# This is the Flask app which gets the list of reports and handels routing 

import os, logging
from retrying import retry
from flask import Flask, request, render_template
import report_list

app = Flask(__name__)
port = os.environ.get('PORT') 
reports = report_list.reports


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
    try:
        report = request.args.get('report')
        if report in reports:
            r = reports[report]
            retry_wrap(r.get_data())
            r.clean_data()
            retry_wrap(r.send_data())
            return  render_template('report.html', title=report, report=report)
        else:
            err = "did you get the report name right?"
            return render_template('error.html', title='Error', error=err)
    except Exception as err:
        err = str(err)
        return render_template('error.html', title='Error', error=err)


@app.route('/status')
def test():
    try:
        for report in reports:
            r = reports[report]
            retry_wrap(r.get_upload_date())
        return render_template('status.html', title='Status', reports=reports)
    except Exception as err:
        err = str(err)
        return render_template('error.html', title='Error', error=err)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
