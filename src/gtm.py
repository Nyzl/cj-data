# This gets data from Google Tag Manager api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os, sys, logging
import report
import auth