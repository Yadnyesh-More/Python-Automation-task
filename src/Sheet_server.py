import config
from googleapiclient.discovery import build

def append_to_sheet(service, rows):
    """Add new email rows to Google Sheet"""
    try:
        range_name = 'Sheet1!A:D'  # Columns A,B,C,D
        body = {
            'values': rows
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=config.SHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"Added {len(rows)} rows to sheet!")
        return True
    except Exception as error:
        print(f"Error writing to sheet: {error}")
        return False
