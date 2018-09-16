import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Memory_Palace:
    def __init__(self, sheet_select):
        palace = get_palace(sheet_select)
        self.loci = palace.col_values(1)
        self.facts = palace.col_values(2)
        self.mnemonics = palace.col_values(3)
        self.image_files = palace.col_values(4)

def get_palace(sheet_select):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    # Open passed through sheet name

    wk_book = client.open_by_key('1ynNFt25lPaMsjj3RPk0LH6hdia1qRWxX1rdNPIzp1f0')
    sheets = wk_book.worksheets() 
    palace = sheets[sheet_select]
    return palace


if __name__ == "__main__":
    testPalace = Memory_Palace(0)
