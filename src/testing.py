# This file is for testing

import auth, data_to_bq, web_postoffice_test

data = web_postoffice_test.get_data()
data_to_bq.send_data_bq(data,"postoffice")