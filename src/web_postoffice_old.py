"""
postoffice
~~~~~~~~~~~~~
Extracts the url of all branches from the Post Office site then loops though 
and collects the opening hours these are then returned in a dataframe
"""

import pandas as pd
import requests

from bs4 import BeautifulSoup


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
    times_array = []
    days = ["day", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    page = requests.get("https://www.postoffice.co.uk" + office)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="NormalOpeningTimes")

    timesElement = results.find_all(class_="TimesTextCell")

    for time, day in zip(timesElement, days):
        times_array.append([day, time.text])

    times_array.pop(0)  # remove the dummy data from the front of the list
    return times_array


def makeDataFrame():
    """ Create a dataframe containing all the branches along with its opening hours """
    URL = "https://www.postoffice.co.uk/all-locations"
    TABLE_ID = "table_id"  # This is the table that holds all the Post offfice elements
    CLASS_OF_PO_ELEMENT = (
        "bsm-link shah"
    )  # This is the element that contains each Post Office details

    hoursOpen = []
    postOffices = getPostoffices(URL, TABLE_ID, CLASS_OF_PO_ELEMENT)
    for postOffice in postOffices:
        print(postOffice[0])
        # uncomment when testing for small subset
        # if postOffice[0] == "Stansted":
        #     break
        hoursOpen.append([postOffice[0], getTimes(postOffice[1])])

    df = pd.DataFrame(hoursOpen)

    print(df)
    return df


makeDataFrame()