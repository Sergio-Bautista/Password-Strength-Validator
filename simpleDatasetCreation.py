import csv
import re 

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
        # 'num_count': sum(1 for c in password if c.isdigit()), 
        # 'special_count': sum(1 for c in password if not c.isalnum()), 

        # Advanced features
        'starts_with_upper': len(password) > 0 and password[0].isupper(),
        'ends_with_number': len(password) > 0 and password[-1].isdigit(),
        'numbers_cluster': bool(re.search(r'\d{2,}', password)), 
        'keyboard_pattern' : any(p in password.lower() for p in ['qwerty', 'asdf', '123456']),
        'entropy': calculate_entropy(password) 
    }
    return features
    # features = {
    #     'password': password, 
    #     'length': len(password), 
    #     'has_uppercase' : True if any(c.isupper() for c in password) else False, 
    #     'has_lowercase' : True if any(c.islower() for c in password) else False, 
    #     'has_number' : True if any(c.isdigit() for c in password) else False, 
    #     'has_special' : any(not c.isalnum() for c in password),
    #     'num_count': sum(1 for c in password if c.isdigit()), 
    #     'special_count': sum(1 for c in password if not c.isalnum()), 

    #     #advance features
    #     'starts_with_upper': len(password) > 0 and password[0].isupper(),
    #     'ends_with_number': len(password) > 0 and password[-1].isdigit(),
    #     'numbers_cluster': True if re.search(r'\d{2,}', password) else False, # sequential numbers
    #     'keyboard_pattern' : True if any(p in password.lower() for p in ['qwerty', 'asdf', '123456']) else False,
    #     'entropy': calculate_entropy(password) #randomness score
    # }
    # return features

def calculate_entropy(password):
    """Calculates Shannon entropy (measure of randomness)"""
    import math
    
    char_set_size = len(set(password))
    if char_set_size == 0:
        return 0
    
    return len(password) * math.log2(char_set_size)
    
    # entropy = math.log2(char_set_size ** len(password))
    # return min(entropy / 100, 1.0) # normalize to 0-1


# testing training datasets

# Open the file and read each line into a list
with open("weak_passwords.txt", "rb") as weak:
    # .strip() removes the newline characters (\n) from each line
    weak_passwords = [line.strip() for line in weak if line.strip()]

# Test that it loaded correctly
print(f"Successfully loaded {len(weak_passwords)} weak passwords.")
print("First 5 samples:", weak_passwords[:5])

# Open the file and read each line into a list
with open("medium_passwords.txt", "rb") as medium:
    # .strip() removes the newline characters (\n) from each line
    medium_passwords = [line.strip() for line in medium if line.strip()]

# Test that it loaded correctly
print(f"Successfully loaded {len(medium_passwords)} medium passwords.")
print("First 5 samples:", medium_passwords[:5])

# Open the file and read each line into a list
with open("strong_passwords.txt", "rb") as strong:
    # .strip() removes the newline characters (\n) from each line
    strong_passwords = [line.strip() for line in strong if line.strip()]

# Test that it loaded correctly
print(f"Successfully loaded {len(strong_passwords)} strong passwords.")
print("First 5 samples:", strong_passwords[:5])


data = []

for pwd in weak_passwords:
    features = extract_features(pwd)
    features['label'] = 0
    data.append(features)

for pwd in medium_passwords:
    features = extract_features(pwd)
    features['label'] = 1
    data.append(features)

for pwd in strong_passwords:
    features = extract_features(pwd)
    features['label'] = 2
    data.append(features)


# save it as a csv
with open('password_data.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)