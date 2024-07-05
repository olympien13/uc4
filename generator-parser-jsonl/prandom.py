import random
import string

def generate_random_id():
    prefix = "clxt"
    letters = string.ascii_lowercase
    digits = string.digits

    random_part = (
        ''.join(random.choices(letters, k=4)) +  # 4 lowercase letters
        ''.join(random.choices(digits, k=8)) +   # 8 digits
        ''.join(random.choices(letters, k=1)) +  # 1 lowercase letter
        ''.join(random.choices(digits, k=1)) +   # 1 digit
        ''.join(random.choices(letters, k=2)) +  # 2 lowercase letters
        ''.join(random.choices(letters, k=1)) +  # 1 lowercase letter
        ''.join(random.choices(digits, k=1)) +   # 1 digit
        ''.join(random.choices(letters, k=1)) +  # 1 lowercase letter
        ''.join(random.choices(digits, k=1))     # 1 digit
    )

    return prefix + random_part

# Generate and print a random ID
random_id = generate_random_id()
print(random_id)
