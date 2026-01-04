import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'http\s+', '', text)
    text = re.sub(r'www\.\s+', '', text)
    
    return text.strip()
        