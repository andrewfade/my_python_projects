from googleapiclient.discovery import build
from google.oauth2 import service_account
import slack
import time




SLACK_TOKEN = "xoxb-2424764285255-2872526286838-4XxBuNx0GY3xTrV3ctMwrQES"
client = slack.WebClient(token = SLACK_TOKEN)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1hw_C5tfi089BtX-k0U6Hw3skN4EAGjlC_qeMRVxlioc'
SAMPLE_RANGE_NAME = 'Form Responses 1!E2:E'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()


#kaldığı yerden devam etmesi için range i ayarla

while True :
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    liste = []
    for i in result["values"]:
        liste.append(i)
    print(liste)
    counter = list(range(0,400,5))
    print(counter)
    if len(liste) in counter == 0 :
        data = liste.count(["Data Science"])
        aws = liste.count(["AWS/Devops"])
        full = liste.count(["Full Stack"])
        cyber = liste.count(["Cyber Security"])
        yazi = f"Anketi dolduran kişi sayısı {len(liste)} olmuştur. \n Full Stack = {full} \n Data Science = {data} \n AWS/Devops = {aws} \n Cyber ={cyber}"
        client.chat_postMessage(channel="#010_core_team", text = yazi)
        print(yazi)
    time.sleep(20)