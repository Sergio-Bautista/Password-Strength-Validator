import csv
import re 
# from collections import Counter

def extract_features(password):
    """Extracts important features from a password"""
    # CRITICAL FIX: Convert integers/floats/NaNs to a clean string
    password = str(password) if password is not None else ""

    features = {
        'password': password, 
        'length': len(password), 
        # Cleaned up: any() naturally returns True or False
        'has_uppercase' : any(c.isupper() for c in password), 
        'has_lowercase' : any(c.islower() for c in password), 
        'has_number' : any(c.isdigit() for c in password), 
        'has_special' : any(not c.isalnum() for c in password),

        # Advanced features
        'starts_with_upper': len(password) > 0 and password[0].isupper(),
        'ends_with_number': len(password) > 0 and password[-1].isdigit(),
        'numbers_cluster': bool(re.search(r'\d{2,}', password)), 
        'keyboard_pattern' : any(p in password.lower() for p in ['qwerty', 'asdf', '123456']),
        'entropy': calculate_entropy(password) 
    }
    return features

def calculate_entropy(password):
    """Calculates Shannon entropy (measure of randomness)"""
    import math
    
    char_set_size = len(set(password))
    if char_set_size == 0:
        return 0
    
    return len(password) * math.log2(char_set_size)
    
    # entropy = math.log2(char_set_size ** len(password))
    # return min(entropy / 100, 1.0) # normalize to 0-1



def assign_label(password):
    
    score = 0

    # Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    # Character variety
    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    # Penalties
    common_patterns = [
        'password',
        'admin',
        'qwerty',
        '123456',
        'welcome',
        'letmein'
    ]

    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 2

    # Convert score to label
    if score <= 2:
        return 0      # Weak
    elif score <= 5:
        return 1      # Medium
    else:
        return 2      # Strong
    


# Function to read the passwords from a text file and manually assign labels
def read_password_from_file(filename):
    with open(filename, 'r') as file:
        passwords = file.read().splitlines()
        
    data = []
    for password in passwords:
        features = extract_features(password)
        label = assign_label(password)
        # label = 0 if len(password) <= 8 else (1 if 'password' not in password.lower() and 'admin' not in password.lower() else 2)
        features['label'] = label
        data.append(features)
    
    return data

filename = 'text.txt'
data_from_file = read_password_from_file(filename)

# save it as a csv
with open('password_data.csv', 'w') as f:
    data = data_from_file
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)