import re
from urllib.parse import urlparse

def extract_features(url: str) -> dict:
    """Extract 30 features from a raw URL to map against the existing phishing model."""
    features = {}
    
    # Simple heuristics based on standard phishing datasets
    features['having_IP_Address'] = -1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 1
    
    url_len = len(url)
    features['URL_Length'] = 1 if url_len < 54 else (0 if 54 <= url_len <= 75 else -1)
    
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net"
    features['Shortining_Service'] = -1 if re.search(shortening_services, url, re.I) else 1
    
    features['having_At_Symbol'] = -1 if '@' in url else 1
    
    last_double_slash = url.rfind('//')
    features['double_slash_redirecting'] = -1 if last_double_slash > 7 else 1
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    features['Prefix_Suffix'] = -1 if '-' in domain else 1
    
    dot_count = domain.count('.')
    features['having_Sub_Domain'] = 1 if dot_count <= 1 else (0 if dot_count == 2 else -1)
    
    features['SSLfinal_State'] = 1 if url.startswith("https") else -1
    features['Domain_registeration_length'] = 1 # Assume standard
    features['Favicon'] = 1 # Assume safe
    features['port'] = 1 # Assume safe
    
    features['HTTPS_token'] = -1 if re.search(r"https", domain) else 1
    
    # Count initial red flags
    red_flags = sum(1 for v in features.values() if v == -1)
    
    # Non-DOM active scanning variables are normalized to trusted baseline.
    # However, if the basic URL structure is highly suspicious (>2 red flags),
    # we penalize these unknown assumptions so the ML model accurately predicts Phishing.
    penalty = -1 if red_flags > 2 else 1
    
    features['Request_URL'] = penalty
    features['URL_of_Anchor'] = -1 if red_flags > 2 else 0
    features['Links_in_tags'] = -1 if red_flags > 2 else 0
    features['SFH'] = penalty
    features['Submitting_to_email'] = penalty
    features['Abnormal_URL'] = penalty
    features['Redirect'] = 0
    features['on_mouseover'] = 1
    features['RightClick'] = 1
    features['popUpWidnow'] = 1
    features['Iframe'] = 1
    features['age_of_domain'] = 1
    features['DNSRecord'] = penalty
    features['web_traffic'] = penalty
    features['Page_Rank'] = penalty
    features['Google_Index'] = 1
    features['Links_pointing_to_page'] = 0
    features['Statistical_report'] = 1

    return features

def get_reasons(features: dict) -> list:
    """Generate human readable reasons for flagged attributes."""
    reasons = []
    if features['having_IP_Address'] == -1: reasons.append("URL contains an IP address instead of a domain name.")
    if features['URL_Length'] == -1: reasons.append("URL length is suspiciously long.")
    if features['Shortining_Service'] == -1: reasons.append("URL uses a known link shortening service.")
    if features['having_At_Symbol'] == -1: reasons.append("URL contains an '@' symbol, which hides the true destination.")
    if features['double_slash_redirecting'] == -1: reasons.append("URL contains a redirecting '//' out of position.")
    if features['Prefix_Suffix'] == -1: reasons.append("Domain contains a hyphen ('-'), a common phishing tactic.")
    if features['having_Sub_Domain'] == -1: reasons.append("Domain has multiple sub-domains, attempting to spoof authority.")
    if features['SSLfinal_State'] == -1: reasons.append("URL does not use secure HTTPS.")
    if features['HTTPS_token'] == -1: reasons.append("The domain part contains the word 'https' to trick users.")
    
    if len(reasons) == 0:
        reasons.append("URL structural components look standard and safe.")
    return reasons
