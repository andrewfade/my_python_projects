from googleapiclient.discovery import build
from google.oauth2 import service_account
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time
import slack
from cre import password



SLACK_TOKEN = "xxxxxxxxxx"
client = slack.WebClient(token = SLACK_TOKEN)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = 'xxxxxxx'
SAMPLE_RANGE_NAME = 'Form Yanıtları 1!A2:C'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()


#kaldığı yerden devam etmesi için range i ayarla
ex_len = 0
counter_s = 0
counter_f = 0
while True :
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    liste = []
    for i in result["values"]:
        liste.append(i)
    new_len = len(liste)
    ranger = ex_len - new_len
    ex_len = new_len
    if ranger < 0 :    
        mail =  smtplib.SMTP("smtp.gmail.com",587)  
        mail.ehlo() 
        mail.starttls()
        mail.login("xxxxx",password) 
    
        for i in range(-1,ranger-1,-1) : 
            mesaj = MIMEMultipart()  
            mesaj["From"] =  "xxxxxxxx" 
            mesaj["To"] = liste[i][-1] 
            mesaj["Subject"] = "Smtp Mail Gönderme" 
            yazi = f"Merhaba, {liste[i][-2].upper()} Python ile mail gönderiyorum. {liste[i][-1]} sisteme eklendi. Sisteme eklenen {liste.index(liste[i])+1}. kişisiniz. teşekkür ederim."  
            mesaj_govdesi =  MIMEText(yazi,"plain") 
            mesaj.attach(mesaj_govdesi) 
            try:
                mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())  # Mailimizi gönderiyoruz.
                print(f"Mail {liste[i][-1]} adresine başarıyla gönderildi....")
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                client.chat_postMessage(channel="#test", text = yazi)
                counter_s += 1
                with open("log.txt", 'a', encoding="utf-8") as file:
                    file.write(f"{time_string} zamanında {liste[i][-1]} adresine başarıyla e-posta gönderildi. Toplam başaılı işlem sayısı {counter_s}\n")  

            except:
                sys.stderr.write(f"{liste[i][-1]} adresine Mail göndermesi başarısız oldu...") # Herhangi bir bağlanma sorunu veya mail gönderme sorunu olursa
                sys.stderr.flush()
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                counter_f += 1
                with open("log.txt", 'a', encoding="utf-8") as file:
                    file.write(f"{time_string} zamanında {liste[i][-1]} adresine Mail göndermesi başarısız oldu. Başarısız işlem sayısı {counter_f}\n")
        mail.close()
    else: 
        print("yeni giriş olmamıştır")
    time.sleep(20)
