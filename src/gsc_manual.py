# This file is for manually runnign GSC data
import auth, data_to_bq, search_console
import sys
import pandas as pd

def manual(**kwargs):
    startDate = kwargs['startDate']
    endDate = kwargs['endDate']

    x = 0
    while True:
        frame = search_console.get_data(startDate=startDate,endDate=endDate,startRow=x)
        frame['report_date'] = pd.to_datetime('today')
        data_to_bq.send_data_bq(frame=frame, name='gsc_fullsite', writeType='WRITE_APPEND')
        x += 25000
        if len(frame) < 25000:
            break
        else:
            continue

if __name__ == '__main__':
    sys.argv[1]
    startDate = sys.argv[1]
    endDate = sys.argv[2]
    manual(startDate=startDate,endDate=endDate )