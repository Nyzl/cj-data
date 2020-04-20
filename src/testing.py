# This file is for testing

import auth, data_to_bq, search_console

data = search_console.get_data()
data_to_bq.send_data_bq(data,"search_console")