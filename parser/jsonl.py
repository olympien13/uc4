import pandas as pd

df = pd.read_json('ftdata1.jsonl', lines=True)
print(df)
for row in df.itertuples(index=True, name='Pandas'):
    print(f"Index: {row.Index}")
    print(f"input: {row.input}")
    print("####")