# This file is for manually runnign GSC data
import auth, data_to_bq, search_console
import sys

def manual(**kwargs):
    startDate = kwargs['startDate']
    endDate = kwargs['endDate']

    #for x in range(0,500000,25000):
    #    y = search_console.get_data(startDate=startDate,endDate=endDate,startRow=x)
    #    data_to_bq.send_data_bq(frame=y, name='gsc_fullsite', writeType='WRITE_APPEND')
    #    if len(y) < 25000:
    #        break
    #    else:
    #        continue


    x = 0
    while True:
        y = search_console.get_data(startDate=startDate,endDate=endDate,startRow=x)
        data_to_bq.send_data_bq(frame=y, name='gsc_fullsite', writeType='WRITE_APPEND')
        x += 25000
        if len(y) < 25000:
            break
        else:
            continue


if __name__ == '__main__':
    sys.argv[1]
    startDate = sys.argv[1]
    endDate = sys.argv[2]
    testing(startDate=startDate,endDate=endDate )