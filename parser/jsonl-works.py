import pandas as pd
import random
import string
import yaml 
import sys
import json

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

df_agent = pd.read_json('ftdata-agent.jsonl', lines=True)
#print(df_agent.columns)
df_document = pd.read_json('ftdata-document.jsonl', lines=True)
output_df_agent = pd.DataFrame(columns=df_agent.columns)
#print(output_df_agent.columns)
columns_equal = df_agent.columns.equals(output_df_agent.columns)
#print(columns_equal)

output_df_document = pd.DataFrame(columns=df_document.columns)

indx = 1

for i in range(1,3):
    for row in df_agent.itertuples(index=True, name='Pandas'):
        #print(f"Index: {row.Index}")
        #print(f"input: {row.input}")
        #print(f"output: {row.output}")
        
        # Modify last task of "input"
        dct_input_agent = yaml.safe_load(f"{row.input}")
        s = dct_input_agent[-1]['tasks'][-1]['name']
        dct_input_agent[-1]['tasks'][-1]['name'] = f"{s} \"{indx}\""
        #print(json.dumps(dct_input_agent[-1]['tasks'][-1], indent=4))
        # Convert the modified input dictionary back to a YAML string
        modified_dct_input = yaml.dump(dct_input_agent, sort_keys=False, width=float("inf"))


        # Update the DataFrame with the modified input
        df_agent.at[row.Index, 'input'] = modified_dct_input


        # Modify last task of "output"
        dct_output_agent = yaml.safe_load(f"{row.output}")
        dct_output_agent['ibm.ce_emea_rag.rag_agent']['rag_output_key'] = f"{indx}"
        # Convert the modified input dictionary back to a YAML string
        modified_dct_output = yaml.dump(dct_output_agent, sort_keys=False, width=float("inf"))
        df_agent.at[row.Index, 'output'] = modified_dct_output
        output_df_agent = output_df_agent._append(pd.DataFrame([df_agent.loc[row.Index]],columns = row._fields), ignore_index=True)
        #output_df_agent.loc[len(output_df_agent.index)] = row.
        
        dct_input_agent[-1]['tasks'][-1]['name'] = f"{s}"
        modified_dct_input = yaml.dump(dct_input_agent, sort_keys=False)
        df_agent.at[row.Index, 'input'] = modified_dct_input

        indx += 1

# Write DataFrame to jsonl file
output_df_agent.to_json('output.jsonl', orient='records', lines=True)

print("DataFrame has been written to output.jsonl")
