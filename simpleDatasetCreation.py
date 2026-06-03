import csv
import re 

def extract_features(password):
    """Extracts important features from a password"""

    features = {
        'password': password, 
        'length': len(password), 
        'has_uppercase' : True if any(c.isupper() for c in password) else False, 
        'has_lowercase' : True if any(c.islower() for c in password) else False, 
        'has_number' : True if any(c.isdigit() for c in password) else False, 
        'has_special' : True if any(c.isalnum() for c in password) else False, 
        'num_count': sum(1 for c in password if c.isdigit()), 
        'special_count': sum(1 for c in password if not c.isalnum()), 

        #advance features
        'starts_with_upper': True if password[0].isupper() else False,
        'ends_with_number': True if password[-1].isdigit() else False,
        'numbers_cluster': True if re.search(r'\d{2,}', password) else False, # sequential numbers
        'keyboard_pattern' : True if any(p in password.lower() for p in ['qwerty', 'asdf', '123456']) else False,
        'entropy': calculate_entropy(password) #randomness score
    }
    return features

def calculate_entropy(password):
    """Calculates Shannon entropy (measure of randomness)"""
    import math
    
    char_set_size = len(set(password))
    if char_set_size == 0:
        return 0
    
    entropy = math.log2(char_set_size ** len(password))
    return min(entropy / 100, 1.0) # normalize to 0-1


# testing training datasets

weak_passwords = ["password123", 'dragon2024', 'qwerty123']
strong_passwords = ['Tr0p!cSunset#2024', "9xL$kP2@mQ6"]


data = []

for pwd in weak_passwords:
    features = extract_features(pwd)
    features['label'] = 0 # 0 = weak
    data.append(features)
    


for pwd in strong_passwords:
    features = extract_features(pwd)
    features['label'] = 1 # 1 = strong
    data.append(features)


# save it as a csv
with open('password_data.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)