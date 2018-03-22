import pandas as pd
import httplib2
from apiclient import discovery
from oauth2client.file import Storage
global json_path, DB_CRED

json_path = "/home/user/...."
DB_CRED = "/home/user/...."


def get_data(data_type):
    conn = connect_db("yourdatabase", DB_CRED)
    if data_type == "category":
        df = pd.read_sql("""YOUR SQL QUERY""", conn)

    elif data_type == "product":
        df = pd.read_sql("""YOUR SQL QUERY""", conn)

    conn.close()
    print("db data ok")
    return df

def authorize(json_path):
    store = Storage(json_path)
    credentials = store.get()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    print("Auth ok!")
    return service

def insert_data(sheetname, df, service):
    spreadsheetID = 'your_spreadsheet_id'
    # This always clears the sheet and inserts more data
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetID, range=sheetname, body={})
    response = request.execute()
    data = df.values.tolist()
    data.insert(0, list(df.columns))
    result = service.spreadsheets().values().append(
                spreadsheetId=spreadsheetID, range=sheetname,
                valueInputOption="USER_ENTERED", body={'values': data}).execute()

def main():
    '''
    data_type : category | product
    '''
    service = authorize(json_path)

    for data_type in ['category', 'product']:
        print(data_type)
        df = get_data(data_type)
        insert_data(data_type, df, service)

if __name__ == '__main__':
    main()