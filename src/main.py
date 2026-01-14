import os
import sys

import json
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import config
from gmail_service import get_unread_emails, parse_email, mark_as_read
from Sheet_server import append_to_sheet

def authenticate_google():
    """Handle OAuth login - creates token.json after first run"""
    creds = None
    
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def load_processed_emails():
    """Load list of already processed email IDs"""
    if os.path.exists(config.STATE_FILE):
        with open(config.STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_emails(processed_emails):
    """Save processed email IDs to prevent duplicates"""
    with open(config.STATE_FILE, 'w') as f:
        json.dump(list(processed_emails), f)

def main():
    print("🚀 Starting Gmail to Sheets automation...")
    
    # 1. Authenticate
    creds = authenticate_google()
    service_gmail = build('gmail', 'v1', credentials=creds)
    service_sheets = build('sheets', 'v4', credentials=creds)
    
    # 2. Load previously processed emails
    processed_emails = load_processed_emails()
    print(f"Already processed {len(processed_emails)} emails")
    
    # 3. Get unread emails
    messages = get_unread_emails(service_gmail)
    new_rows = []
    
    # 4. Process each email
    for msg in messages:
        msg_id = msg['id']
        if msg_id in processed_emails:
            print(f"Skipping already processed: {msg_id}")
            continue
        
        print(f"Processing new email: {msg_id}")
        
        # Parse email
        email_data = parse_email(service_gmail, msg_id)
        if email_data:
            row = [
                email_data['from'],
                email_data['subject'],
                email_data['date'],
                email_data['content']
            ]
            new_rows.append(row)
            
            # Mark as read
            mark_as_read(service_gmail, msg_id)
            processed_emails.add(msg_id)
    
    # 5. Save to Google Sheets
    if new_rows:
        success = append_to_sheet(service_sheets, new_rows)
        if success:
            save_processed_emails(processed_emails)
            print(f"✅ Successfully added {len(new_rows)} new emails to sheet!")
        else:
            print("❌ Failed to save to sheet")
    else:
        print("ℹ️ No new emails to process")

if __name__ == '__main__':
    main()
