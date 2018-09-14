import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Breath-a07644f00238.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1ynNFt25lPaMsjj3RPk0LH6hdia1qRWxX1rdNPIzp1f0/edit#gid=0")
sh = wks.sheet1
info = sh.get_all_values()

#info is now a 2-D List/Matrix with all values.  
#Iterate through this 
for i in info:
    print(i[1])
# In app make the list of images to load into viewer this list
