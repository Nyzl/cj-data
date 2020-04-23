# This file is for testing
import auth, data_to_bq, search_console

def test():
    for x in range(0,500000,25000):
        y = search_console.get_data(startDate='2020-04-22',endDate='2020-04-22',startRow=x)
        data_to_bq.send_data_bq(frame=y, name='gsc_fullsite', writeType='WRITE_APPEND')
        if len(y) < 25000:
            break
        else:
            continue
    

if __name__ == '__main__':
    test()