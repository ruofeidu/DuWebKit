from __future__ import print_function
import httplib2
import os
import logging
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
  import argparse

  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'DuWebsite'


def get_credentials():
  """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
  credential_path = os.path.join(
      credential_dir, 'sheets.googleapis.com-python-quickstart.json')

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else:
      logging.warn('Please use Python 3+ for compilation.')
      pass
    logging.warn('Storing credentials to ' + credential_path)
  return credentials


def get_publications(service, spreadsheetId):
  """Gets publications from gSheet."""
  range_name = 'publications!A:AZ'
  results = service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=range_name).execute()
  values = results.get('values', [])
  if not values:
    logging.error('No publication found in gSheets.')
    exit(1)
  return values


def get_arts(service, spreadsheetId):
  """Gets arts from gSheet."""
  range_name = 'arts!A:AZ'
  results = service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=range_name).execute()
  values = results.get('values', [])
  if not values:
    logging.error('No art found in gSheets.')
    exit(1)
  return values


def get_people(service, spreadsheetId):
  """Gets people from gSheet."""
  range_name = 'people!A:BB'
  results = service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=range_name).execute()
  values = results.get('values', [])
  if not values:
    logging.error('No people found in gSheets.')
    exit(1)
  return values


def get_service():
  """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = ("https://sheets.googleapis.com/$discovery/rest?" "version=v4")
  service = discovery.build(
      'sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
  return service
