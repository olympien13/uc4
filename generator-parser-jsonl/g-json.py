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

def insert_string_at_index(original, to_insert, index):
    return original[:index] + to_insert + original[index:]

def manage_df(df_input, output_df_output, rag_json_key):
    global indx

    for row in df_input.itertuples(index=True, name='Pandas'):
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
        df_input.at[row.Index, 'input'] = modified_dct_input

        # Modify last task of "output"
        dct_output_agent = yaml.safe_load(f"{row.output}")
        dct_output_agent[rag_json_key]['rag_output_key'] = f"{indx}"
        # Convert the modified input dictionary back to a YAML string
        modified_dct_output = yaml.dump(dct_output_agent, sort_keys=False, width=float("inf"))
        df_input.at[row.Index, 'output'] = modified_dct_output
        
        output_df_output = output_df_output._append(pd.DataFrame([df_input.loc[row.Index]],columns = row._fields), ignore_index=True)
        #output_df_input.loc[len(output_df_output.index)] = row.
        
        dct_input_agent[-1]['tasks'][-1]['name'] = f"{s}"
        modified_dct_input = yaml.dump(dct_input_agent, sort_keys=False)
        df_input.at[row.Index, 'input'] = modified_dct_input
        indx += 1

    return output_df_output


set_number = int(sys.argv[1])
input_file = sys.argv[2]
output_file = f'output-{input_file.split(".")[0]}.jsonl'
df_data = pd.read_json(input_file, lines=True)
cols_to_be_removed = ['data_source_description', 'module', 'license', 'path', 'repo_name', 'repo_url']
for col in cols_to_be_removed:
    df_data.pop(col)

output_df_data = pd.DataFrame(columns=df_data.columns)
number = 0
current_index_dataframe = 0
for index, row in df_data.iterrows():
    print(current_index_dataframe)
    output_df_data.loc[current_index_dataframe] = [df_data.at[index, 'input'], df_data.at[index, 'output']]
    current_index_dataframe += 1
    df_data.at[index, 'input'] = f"{row['input']}" + " \"{number}\"\n"

    # search_key= 'ibm.ce_emea_rag.rag_agent:\n'
    # try:
    #     str_idx_search = f"{row['output']}".index(search_key)
    # except ValueError:
    #     search_key= 'ibm.ce_emea_rag.rag_document:\n'

    # try:    
    #     str_idx_search = f"{row['output']}".index(search_key)
    # except ValueError:
    #     continue

    
    # df_data.at[index, 'output'] = insert_string_at_index(df_data.at[index, 'output'], "        rag_output_key: \"{number}\"\n", str_idx_search + len(search_key))
    output_df_data.loc[current_index_dataframe] = [df_data.at[index, 'input'], df_data.at[index, 'output']]
    for i in range(1, set_number):
        output_df_data.at[current_index_dataframe, 'input'] = df_data.at[index, 'input'].replace("{number}", str(i))
        #output_df_data.at[current_index_dataframe, 'output'] = df_data.at[index, 'output'].replace("{number}", str(i))
        output_df_data.loc[current_index_dataframe] = [output_df_data.at[current_index_dataframe, 'input'], df_data.at[index, 'output']]
        current_index_dataframe += 1

    #output_df_data = output_df_data._append(df_data.at[index], ignore_index=True)
# Write DataFrame to jsonl file
output_df_data.to_json(output_file, orient='records', lines=True)

print(f"DataFrame has been written to {output_file}")
