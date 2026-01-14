📧 Gmail to Google Sheets Automation (Python)

Author: Yadnyesh More
Role: Full Stack Developer Intern
Date: 14 January 2026

📌 Project Overview

This project is a Python automation script that reads UNREAD emails from Gmail and stores them into Google Sheets.

Each email is saved with the following details:

From

Subject

Date

Content

Once an email is processed, it is never processed again, so there are no duplicate entries in the sheet.

This project helped me understand Google APIs, OAuth authentication, and real-world automation.

🛠️ Technologies Used

Python

Gmail API

Google Sheets API

OAuth 2.0

JSON (for local state storage)

📂 Features

✅ Reads only UNREAD emails

✅ Stores data in Google Sheets

✅ Prevents duplicate entries

✅ Uses OAuth 2.0 securely

✅ Works completely on local machine

📁 Google Sheet Format

The Google Sheet must have these headers in Row 1:

From | Subject | Date | Content

🔧 Setup Instructions (Beginner Friendly)
1️⃣ Google Cloud Console Setup

Go to: https://console.cloud.google.com

Create a New Project

Enable these APIs:

Gmail API

Google Sheets API

OAuth Consent Screen:

Type: External

Add your Gmail ID as Test User

Create Credentials:

OAuth Client ID

Application type: Desktop App

Download the file and save it as:

credentials/credentials.json

2️⃣ Google Sheets Setup

Go to https://sheets.google.com

Create a new sheet (example name: Gmail Log)

Add headers in first row:

From | Subject | Date | Content


Copy the SHEET_ID from the URL

Paste it into config.py

3️⃣ Local Project Setup
git clone https://github.com/yadnyeshmore/gmail-to-sheets.git
cd gmail-to-sheets
pip install -r requirements.txt
python src/main.py


👉 On first run, browser will open for Gmail login and permission.

🔐 OAuth Flow (Simple Explanation)

First Run

Browser opens

Gmail permission granted

token.json file is created

Next Runs

No browser required

Token refresh happens automatically

🚫 Duplicate Prevention Logic

To avoid processing the same email again, the script stores Gmail Message IDs in a file:

processed_emails.json


Before processing an email:

if msg_id in processed_emails:
    continue


After successful entry:

Message ID is saved

Email will never be added again

This keeps the Google Sheet clean and accurate.

📦 Why JSON Instead of Database?

I used a JSON file because:

No extra setup needed

Works offline

Very fast

Easy to understand

Secure using .gitignore

Even after 90 emails, file size was only ~2KB.

🐛 Challenges Faced
1️⃣ Email Body Parsing (Base64 Issue)

Problem:

Some emails had body in payload.body.data

Some had multipart content

Some had no body field at all

Solution:

Checked both payload.body and payload.parts

Added safe checks before decoding

2️⃣ OAuth “Access Blocked” Error

Problem:

App not verified by Google

Solution:

Added my Gmail ID as Test User

Used “Advanced → Continue” option

3️⃣ Import Error (config.py)

Problem:

import config failed inside src/main.py

Solution:

Moved config.py inside src/ folder

Simple and effective fix.

📸 Proof of Execution

Screenshots available in /proof folder:

Gmail inbox (before processing)

Google Sheet with email data

OAuth permission screen

Terminal output (success message)

🎥 A short demo video (demo.mp4) is also included.

⚠️ Current Limitations

Only plain text emails

HTML emails not converted

No retry logic if API fails

State works only on one machine

Email content limited to 500 characters

⭐ Future Improvements (Planned)

HTML to text conversion

Subject based filtering (Invoices, Alerts, etc.)

Retry mechanism for API errors

Redis / Database instead of JSON

Export data to CSV

📊 Project Results

Total Emails Processed: 90

Duplicate Entries: 0

Success Rate: 100%

Sheet Rows: 91 (including header)