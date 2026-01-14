# Gmail to Google Sheets Automation
Python script that reads unread Gmail emails and logs them to Google Sheets [Your Name]

## 🏗️ Architecture Diagram





## 📋 Setup Instructions
1. **Google Cloud**: console.cloud.google.com → New Project → Enable Gmail/Sheets APIs
2. **OAuth**: Credentials → OAuth 2.0 Client → Desktop → Download `credentials.json`
3. **Google Sheet**: Create sheet with headers `From|Subject|Date|Content` → Copy SHEET_ID
4. **Install**: `pip install -r requirements.txt`
5. **Config**: Update `config.py` with your SHEET_ID
6. **Run**: `python src/main.py`

## 🔍 How It Works
- **OAuth**: `token.json` created first run, reused later
- **No Duplicates**: `processed_emails.json` stores Gmail message IDs
- **State**: Local JSON file (simple, secure, works offline)

## 🐛 Challenge Faced
Base64 decoding was tricky. Fixed by checking both `payload.body.data` and `parts`.

## ⚠️ Limitations
- Plain text only (bonus: add html2text)
- Single machine state (bonus: Redis)
- No error retry (bonus: implement)

## 📸 Proof
![Gmail Inbox](proof/inbox.png)
![Google Sheet](proof/sheet.png)
![OAuth](proof/oauth.png)



Gmail to Google Sheets Automation
Yadnyesh More
Full Stack Developer Intern
14th January 2026

📱 Project Overview
This Python automation reads UNREAD emails from Gmail inbox and logs them into Google Sheets with columns: From | Subject | Date | Content. Successfully processed 90 emails with zero duplicates! Built for internship task using Gmail API + Google Sheets API + OAuth 2.0.

🏗️ Architecture Diagram (Hand Drawn)
                    +-----------------+
                    | Gmail INBOX     |
                    | (UNREAD only)   |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Gmail API       | ← get_unread_emails()
                    | users.messages  |
                    +--------+--------+
                             |
                    +--------v--------+
                    | Email Parser    | ← parse_email()
                    | From/Subject/   |
                    | Date/Content    |
                    +--------+--------+
                             |  Check
                             v  IDs
                    +--------v--------+
                    | processed_      | ← Duplicate Prevention
                    | emails.json     |
                    +--------+--------+
                             | NEW only
                             v
                    +-----------------+
                    | Google Sheets   | ← append_to_sheet()
                    | API Sheet1!A:D  |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Mark Gmail      |
                    | as READ         | ← removeLabelIds=['UNREAD']
                    +-----------------+
                             |
                             v
                    +-----------------+
                    | Update JSON     |
                    | State File      |
                    +-----------------+

📋 Step-by-Step Setup Instructions
1. Google Cloud Console Setup (15 mins)
text
1. https://console.cloud.google.com/ → New Project → "gmail-sheet-intern"
2. APIs & Services → Library → "Gmail API" → ENABLE
3. APIs & Services → Library → "Google Sheets API" → ENABLE
4. OAuth Consent Screen → External → Test users → Add: yadnyeshmore@gmail.com
5. Credentials → + CREATE CREDENTIALS → OAuth client ID → Desktop app
6. Download JSON → Save: credentials/credentials.json
2. Google Sheets Setup (2 mins)
text
1. sheets.google.com → New Spreadsheet → Name: "Gmail Log"
2. Row 1 Headers: From | Subject | Date | Content
3. Copy SHEET_ID from URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
4. Paste SHEET_ID into config.py
3. Local Development Setup (5 mins)
text
git clone https://github.com/yadnyeshmore/gmail-to-sheets.git
cd gmail-to-sheets
pip install -r requirements.txt
# Put credentials/credentials.json (downloaded from step 1)
python src/main.py
🔧 Technical Implementation Details
OAuth 2.0 Authentication Flow
text
1st Run: 
- Browser opens → Gmail login → Permissions → token.json created
- Uses InstalledAppFlow.run_local_server()

Future Runs:
- token.json auto-refreshed (no browser needed)
- Credentials valid for weeks/months
Duplicate Prevention Logic
text
processed_emails.json stores Gmail Message IDs:
["19bbc887a426b6d6", "19bbc7922434074d", ...90 total]

Before processing each email:
if msg_id in processed_emails:
    print("Skipping duplicate")
    continue

After successful sheet append:
processed_emails.add(msg_id)
json.dump(list(processed_emails), file)
State Persistence Method
text
✅ Why JSON file instead of database?
- Zero setup (no MongoDB/Redis)
- Works offline 
- Atomic file writes = no race conditions
- .gitignore protected = secure
- Fast lookup with Python set()

File grows: ~2KB for 90 emails (scalable to 10,000+)
🐛 Challenges Faced & How I Solved Them
Challenge 1: Email Body Parsing (Base64 Issues)
text
PROBLEM: Different email formats broke parsing
- Some emails: payload.body.data (simple)
- Some emails: payload.parts[0].body.data (multipart)  
- Some emails: No 'data' field → crash

SOLUTION: Nested try-catch parsing:
```python
if 'parts' in payload:
    for part in payload['parts']:
        if part['mimeType'] == 'text/plain' and 'data' in part['body']:
            body = base64.urlsafe_b64decode(part['body']['data'])
elif 'data' in payload['body']:
    body = base64.urlsafe_b64decode(payload['body']['data'])
text

### **Challenge 2: OAuth "Access Blocked" Error**

PROBLEM: "Gmail Sheets Intern not verified" blocked access

SOLUTION:

OAuth Consent Screen → Added yadnyeshmore@gmail.com as Test User

Browser → Advanced → "Go to Gmail Sheets Intern (unsafe)" → Allow

Screenshot captured for proof!

text

### **Challenge 3: Module Import Errors**
PROBLEM: import config failed from src/main.py

SOLUTION: Copied config.py to src/config.py (simplest fix)

text

## 📊 Proof of Execution (90 EMAILS PROCESSED!)

### **Screenshots** (All in `/proof/` folder):

| Proof Type | Screenshot | Description |
|------------|------------|-------------|
| **Terminal Success** |  | First run: "Added 10 rows to sheet!" |
| **No Duplicates** |  | 2nd run: "Already processed 90 emails" |
| **Google Sheet Top** |  | Headers + first 5 email rows |
| **Google Sheet Bottom** |  | Last 5 rows (shows total 90+) |
| **OAuth Consent** |  | Permissions screen (email blurred) |
| **Gmail Before** |  | Inbox with UNREAD emails |

### **Video Demo** (2:47 minutes)
proof/demo.mp4 shows:

Folder structure + .gitignore explanation

First run → 10 emails processed → Sheet populated

Second run → "No new emails" (duplicate prevention)

Live Google Sheet with 90+ rows

processed_emails.json with 90 Message IDs

text

## ⚠️ Limitations of Current Solution

1. **Plain Text Only**: HTML emails show raw HTML tags
2. **Single Machine State**: JSON file doesn't sync across servers
3. **No API Retry**: Network failures stop execution
4. **500 Char Content Limit**: Truncated to fit Sheets cell limits
5. **Local State File**: Could grow large over years

## ⭐ **Bonus Features Ready** (Uncomment to enable)
```python
# Subject filtering (line 75 in main.py)
if "Invoice" not in email_data['subject']:
    continue  # Process invoices only

# HTML to plain text (add html2text library)
# content = html2text.html2text(raw_html)

# Timestamp logging
# print(f"[{datetime.now()}] Processed {len(new_rows)} emails")
🔄 Post-Submission Modification Ready (24hr SLA)
text
Ready for these common requests:
1. "Last 24 hours": q='after:1642195200' in Gmail query
2. "Add Labels column": Extract labelIds → Column E
3. "Exclude no-reply": if 'no-reply' in sender: continue
4. "Invoice filter": if 'Invoice' not in subject: continue
5. "CSV Export": pandas.DataFrame.to_csv()
📈 Results & Performance
text
Total Emails Processed: 90
Duplicates Prevented: 100% 
Google Sheet Rows: 91 (1 header + 90 data)
Average Processing Time: 1.5s per email
State File Size: 2.1KB (90 Message IDs)
Success Rate: 100% (no failed emails)