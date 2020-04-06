import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool 

import auth, data_to_bq


session = requests.Session()

def getPostoffices(site, tableName, classOfPOElement):
    """ Returns a list of all the branches found on the site along with the URL of the branch page """
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id=tableName)
    postofficeElement = results.find_all(class_=classOfPOElement, href=True)
    postlist = []

    for officeElement in postofficeElement:
        # get the office name and the href containing the office URL
        postlist.append([officeElement.text, officeElement["href"]])
    return postlist


def getTimes(office):
    """ Returns a list of opening times for the specified office """
    officename = office[0]
    officelink = office[1]
    times_array = []
    days = ["day", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    page = session.get("https://www.postoffice.co.uk" + officelink)
    print(officename)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="NormalOpeningTimes")

    try:
        timesElement = results.find_all(class_="TimesTextCell")
        for time, day in zip(timesElement, days):
            times_array.append([day, time.text])
        times_array.pop(0)  # remove the dummy data from the front of the list

    except AttributeError as err:
        times_array = "Error finding times"

    return [officename, times_array]

def get_data(*args):
    """ Create a dataframe containing all the branches along with its opening hours """
    URL = "https://www.postoffice.co.uk/all-locations"
    TABLE_ID = "table_id"  # This is the table that holds all the Post offfice elements
    CLASS_OF_PO_ELEMENT = (
        "bsm-link shah"
    )  # This is the element that contains each Post Office details

    hoursOpen = []
    postOffices = getPostoffices(URL, TABLE_ID, CLASS_OF_PO_ELEMENT)
    '''with open("postOffices.txt", 'w') as output:
        for row in postOffices:
            output.write(str(row) + '\n')'''

    with Pool(50) as p:
        records = p.map(getTimes, postOffices)

    df = pd.DataFrame(records)
    #return df

    data_to_bq.send_data_bq(df,"postoffice")
    return "done"

if __name__ == '__main__':
    get_data(x)