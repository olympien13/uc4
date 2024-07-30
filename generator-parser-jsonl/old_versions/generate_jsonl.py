import json

# Template for input and output with placeholders
input_template = "- name: Sample Ansible playbooks to manage Artificial Intelligence (AI) assistant agents in a Retrieval-Augmented Generation (RAG) framework\n  hosts: localhost\n  gather_facts: False\n  tasks:\n    - name: Create an AI assistant agent in a Retrieval-Augmented Generation (RAG) framework \"{number}\"\n"
output_template = "      rag_agent:\n        rag_workspace_id: \"{{ rag_workspace_id }}\"\n        agent_name: \"{{ agent_name }}\"\n        method: CREATE\n        rag_output_key: \"{number}\"\nregister: create_result\n"

# Generate 100 entries
entries = []
for i in range(1, 101):
    entry = {
        "input": input_template.format(number=i),
        "output": output_template.format(number=i)
    }
    entries.append(entry)

# Write entries to a JSONL file
with open('generated_data.jsonl', 'w') as file:
    for entry in entries:
        file.write(json.dumps(entry) + '\n')

print("JSONL file generated with 100 entries.")
