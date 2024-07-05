import pandas as pd

# Create sample DataFrames
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c']
})

df2 = pd.DataFrame({
    'A': [4, 5, 6],
    'B': ['d', 'e', 'f']
})

# Compare columns using equals()
columns_equal = df1.columns.equals(df2.columns)
print(df1.columns)
print(df2.columns)
print(columns_equal)
