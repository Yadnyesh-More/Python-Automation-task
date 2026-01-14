import base64
import email
from googleapiclient.discovery import build

def get_unread_emails(service):
    """Get only UNREAD emails from INBOX"""
    try:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX', 'UNREAD'],
            maxResults=10  # Don't get too many
        ).execute()
        messages = results.get('messages', [])
        print(f"Found {len(messages)} unread emails")
        return messages
    except Exception as error:
        print(f"Error getting emails: {error}")
        return []

def parse_email(service, msg_id):
    """Extract From, Subject, Date, Content from email"""
    try:
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        
        # Get headers
        headers = msg['payload']['headers']
        email_data = {}
        
        for header in headers:
            name = header['name']
            value = header['value']
            if name == 'From':
                email_data['from'] = value
            elif name == 'Subject':
                email_data['subject'] = value
            elif name == 'Date':
                email_data['date'] = value
        
        # Get email body (simple version)
        if 'parts' in msg['payload']:
            parts = msg['payload']['parts']
            body_data = ''
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body_data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
        else:
            if 'data' in msg['payload']['body']:
                body_data = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        
        email_data['content'] = body_data[:500]  # First 500 chars only
        email_data['id'] = msg_id
        return email_data
        
    except Exception as error:
        print(f"Error parsing email {msg_id}: {error}")
        return None

def mark_as_read(service, msg_id):
    """Mark email as READ after processing"""
    try:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Marked email {msg_id} as read")
    except Exception as error:
        print(f"Error marking email as read: {error}")
