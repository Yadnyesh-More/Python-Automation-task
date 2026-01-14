# Simple parser - most work done in gmail_service.py
# Can add HTML to plain text conversion here later
def clean_content(content):
    """Clean email content"""
    if content:
        return content.strip()[:500]  # Keep first 500 chars
    return "No content"
