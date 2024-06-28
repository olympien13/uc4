#!/usr/bin/python


from ansible_collections.ibm.ce_emea_rag.plugins.module_utils.utils import get_config, get_agent_payload
from ansible.module_utils.basic import AnsibleModule


import requests
import os
import json 


def run_module():
    
    # Define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        rag_workspace_id=dict(type='str', required=True),
        rag_agent_id=dict(type='str', required=False),
        method=dict(type='str', required=True, choices=['LIST', 'CREATE', 'UPDATE', 'GET_BY_ID', 'DELETE']),
        system_prompt=dict(type='str', required=False, default='You are a helpful assistant that supports users. You respond in valid markdown format. Your answers are concise and a relevant to the question.'),
        agent_name=dict(type='str', required=False, default='FirstName LastName'),
        model_id=dict(type='str', required=False, default='meta-llama/llama-3-70b-instruct'),
        collection_embeddings_metric_type=dict(type='str', required=False, choices=['L2', 'IP', 'COSINE'], default='L2'),
        collection_embeddings_index_type=dict(type='str', required=False, choices=['FLAT', 'IVF_FLAT', 'IVF_SQ8', 'GPU_IVF_FLAT', 'DISKANN'], default='FLAT')
    )

    # Seed the result dict in the object
    result = dict(
        changed=False,
        original_message='',
        json_payload=''
    )

    # The AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Load configuration from JSON file
    config = get_config()
    
    # If the module is in check mode, do not make any changes
    if module.check_mode:
        module.exit_json(**result)

    # Extract the parameters from the Ansible module input
    rag_workspace_id = module.params['rag_workspace_id']
    system_prompt = module.params['system_prompt']
    agent_name = module.params['agent_name']
    model_id = module.params['model_id']
    collection_embeddings_metric_type = module.params['collection_embeddings_metric_type']
    collection_embeddings_index_type = module.params['collection_embeddings_index_type']
    method = module.params['method']
    rag_agent_id = module.params['rag_agent_id']
    headers = {**config['default_headers']}

    agent_payload = get_agent_payload()
    agent_payload['workspace_id'] = rag_workspace_id
    agent_payload['system_prompt'] = system_prompt
    agent_payload['name'] = agent_name
    agent_payload['model_id'] = model_id
    agent_payload['collection_embeddings_metric_type'] = collection_embeddings_metric_type
    agent_payload['collection_embeddings_index_type'] = collection_embeddings_index_type

    try:
        if method == 'LIST':
            response = requests.get(f'{config['api_base_url']}/v1/agents?workspace_id={rag_workspace_id}', headers=headers, verify=False)
        elif method == 'CREATE':
            response = requests.post(f'{config['api_base_url']}/v1/agents', json=agent_payload, headers=headers, verify=False)
        elif method == 'UPDATE':
            if rag_agent_id is not None:
                response = requests.patch(f'{config['api_base_url']}/v1/agents/{rag_agent_id}', json=agent_payload, headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_agent_id required parameter missing!")
        elif method == 'GET_BY_ID':
            if rag_agent_id is not None:
                response = requests.get(f'{config['api_base_url']}/v1/agents/{rag_agent_id}', headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_agent_id required parameter missing!")      
        elif method == 'DELETE':
            if rag_agent_id is not None:
                response = requests.delete(f'{config['api_base_url']}/v1/agents/{rag_agent_id}', headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_agent_id required parameter missing!")     
        response.raise_for_status()  # Raise an error for bad status codes
        result['changed'] = True
        result['original_message'] = None
        result['json_payload'] = response.json()
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=str(e), **result)

    # Exit the module and return the result
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
