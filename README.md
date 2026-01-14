# Gmail to Google Sheets Automation

Yadnyesh More
Full Stack Developer Intern
14th January 2026

# 1) Project Overview

This Python automation reads UNREAD emails from Gmail inbox and logs them into Google Sheets with columns: From , Subject , Date , Content. Successfully processed emails with zero duplicates! 

# 2) Architecture Diagram (Hand Drawn)




# 3) Step-by-Step Setup Instructions

1. Google Cloud Console Setup 

a. Created a New Project in Google Cloude and named as gmail-sheet-intern
b. In Api services Enable Gmail API , Google Sheets Api 
c. OAuth consent screen in that i added test user email id to test the sheet 
d. Create Credentials 
e. Download the Credentials file as a Json 

2. Local Development Setup

git clone https://github.com/yadnyeshmore/gmail-to-sheets.git

pip install -r requirements.txt

# Put credentials/credentials.json (downloaded from step 1)

python src/main.py


# 4) Technical Implementation Details

OAuth 2.0 Authentication Flow

1st Run: 
- Browser opens → Gmail login → Permissions → token.json created
- Uses InstalledAppFlow.run_local_server()

Future Runs:
- token.json auto-refreshed (no browser needed)
- Credentials valid for weeks/months

Duplicate Prevention Logic

processed_emails.json stores Gmail Message IDs:
["19bbc887a426b6d6", "19bbc7922434074d", ...90 total]

Before processing each email:
if msg_id in processed_emails:
    print("Skipping duplicate")
    continue

After successful sheet append:
processed_emails.add(msg_id)
json.dump(list(processed_emails), file)

# 5) Challenges Faced & How I Solved Them

### **Challenge 1: OAuth "Access Blocked" Error**

PROBLEM: "Gmail Sheets Intern not verified" blocked access

SOLUTION:

OAuth Consent Screen → Added yadnyeshmore@gmail.com as Test User

Browser → Advanced → "Go to Gmail Sheets Intern (unsafe)" → Allow

Screenshot captured for proof!

text


## 📊 Proof of Execution 

### **Screenshots** (All in `/proof/` folder):


### **Video Demo** (2:47 minutes)
proof/demo.mp4 shows:



## ⚠️ Limitations of Current Solution

1. **Plain Text Only**: HTML emails show raw HTML tags
2. **Single Machine State**: JSON file doesn't sync across servers
3. **No API Retry**: Network failures stop execution
4. **500 Char Content Limit**: Truncated to fit Sheets cell limits
5. **Local State File**: Could grow large over years

##  **Bonus Features Ready** (Uncomment to enable)

```python
# Subject filtering (line 75 in main.py)
if "Invoice" not in email_data['subject']:
    continue  # Process invoices only

# HTML to plain text (add html2text library)
# content = html2text.html2text(raw_html)

# Timestamp logging
# print(f"[{datetime.now()}] Processed {len(new_rows)} emails")


📈 Results & Performance

Total Emails Processed: 90
Duplicate Entries: 0
Success Rate: 100%
Sheet Rows: 91 (including header)