import pandas as pd

# Sample DataFrame
data = {
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
}
df = pd.DataFrame(data)

# Write DataFrame to jsonl file
df.to_json('output.jsonl', orient='records', lines=True)

print("DataFrame has been written to output.jsonl")
