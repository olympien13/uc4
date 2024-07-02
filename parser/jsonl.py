import pandas as pd
import random
import string
import yaml 
def generate_random_id(prefix):
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

df = pd.read_json('ftdata.jsonl', lines=True)
print(df)
for row in df.itertuples(index=True, name='Pandas'):
    print(f"Index: {row.Index}")
    print(f"input: {row.input}")
    print(f"output: {row.output}")
    dct = yaml.safe_load(f"{row.output}")
    print(dct)
    print(f"#### - {generate_random_id('agxt')}")