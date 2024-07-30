import pandas as pd
import json

# Sample DataFrame with a URL column
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'url': ['http://example.com/alice', 'http://example.com/bob', 'http://example.com/charlie']
}

df = pd.DataFrame(data)

# Write the DataFrame to a JSONL file without escaping URLs
with open('output.jsonl', 'w', encoding='utf-8') as file:
    for record in df.to_dict(orient='records'):
        json_record = json.dumps(record, ensure_ascii=False)
        file.write(json_record + '\n')
