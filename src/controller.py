import os, logging
from retrying import retry
from flask import Flask, request, render_template
import report_list

#path1 = os.path.dirname(os.path.realpath(__file__))
#parentPath = os.path.dirname(path1)
#dotenv.load_dotenv(os.path.join(parentPath, '.env'))

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
    rt = request.args.get('report')
    if rt in reports:
        r = reports[rt]
        retry_wrap(r.get_data())
        retry_wrap(r.clean_data())
        retry_wrap(r.send_data())

        return  "completed " + rt

    else:
        return "did you get the report name right?"

    return "All done"



@app.route('/test')
def test():
    for report in reports:
        r = reports[report]
        retry_wrap(r.get_upload_date())
    return render_template('index.html', title='Status', reports=reports)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
