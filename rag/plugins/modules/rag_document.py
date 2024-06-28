#!/usr/bin/python


from ansible_collections.ibm.ce_emea_rag.plugins.module_utils.utils  import get_config, remove_file
from ansible.module_utils.basic import AnsibleModule


import requests
import os
import json 

def create_document(config, agent_id, file_name):
    create_payload = {
        "agent_id": f"{agent_id}",
        "name": f"{file_name}",
        "file_type": "pdf"
    }
    response = requests.post(f'{config['api_base_url']}/v1/documents', json=create_payload, headers={**config['default_headers']}, verify=False)
    response.raise_for_status()  

    new_document_id = response.json()['id']
    return new_document_id

def generate_upload_url(config, rag_doc_id):
    response = requests.get(f'{config['api_base_url']}/v1/documents/{rag_doc_id}/presignedPostPolicy', headers={**config['default_headers']}, verify=False)
    response.raise_for_status()  
    json_response = response.json()
    return {
        'rag_upload_url':  json_response['url'],
        'rag_x_amz_date': json_response['formData']['x-amz-date'],
        'rag_policy': json_response['formData']['policy'],
        'rag_x_amz_credential': json_response['formData']['x-amz-credential'],
        'rag_x_amz_signature': json_response['formData']['x-amz-signature']

    }

def upload_file(file_url, upload_url,  file_name, upload_data, tmp_dir):
    #file_path = f"{tmp_dir}"
    local_filename = f'{tmp_dir}/{file_url.split('/')[-1]}'
    response = requests.get(file_url, stream=True, verify=False)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


    forms_files = {
        'file': (local_filename, open(local_filename, 'rb'), 'application/pdf')
    }

    forms_data = {
        'key': file_name,
        'x-amz-date': upload_data['rag_x_amz_date'],
        'policy': upload_data['rag_policy'],
        'x-amz-credential': upload_data['rag_x_amz_credential'],
        'x-amz-signature': upload_data['rag_x_amz_signature'],
        'x-amz-algorithm': 'AWS4-HMAC-SHA256'
}
    # Perform the request
    response = requests.post(upload_url, data=forms_data, files=forms_files, verify=False)
    return local_filename

def update_document(config, rag_doc_id):
    response = requests.patch(f'{config['api_base_url']}/v1/documents/{rag_doc_id}', json={'is_uploaded': True}, headers={**config['default_headers']}, verify=False)
    response.raise_for_status()
    return 

def get_csrf_token(session, config):
    response = session.get(f'{config['api_base_url']}/auth/csrf', headers={**config['default_headers']}, verify=False)
    response.raise_for_status()  
    json_response = response.json()
    #raise Exception(session.cookies.get_dict(), json_response['csrfToken'], response.headers)
    return {
        'csrf_token':  json_response['csrfToken']
    }

def get_session_auth_token(session, config, csrf_token):
    auth_data = {
        'email': config['username'],
        'password': config['password'],
        'json': 'true',
        'redirect': 'false',
        'callbackUrl': 'https://rag-turbo-app-rag-turbo.apps.wxai-ocp-ga.p126.cesc.nca.ihost.com',
        'csrfToken': f'{csrf_token}'
    }
    #raise Exception(auth_data)
    c_headers = {}
    c_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    #raise Exception(config)
    
    response = session.post(f'{config['api_base_url']}/auth/callback/credentials', data=auth_data, headers=c_headers, verify=False)
    #raise Exception(session.cookies.get_dict(), csrf_token, response.json())
    response.raise_for_status()  

    #raise Exception(response.headers, response.cookies.get_dict())
    return 


def embed_document(config, agent_id, rag_doc_id, chunk_overlap, chunk_size):
    session = requests.Session()
    
    token = get_csrf_token(session, config)

    get_session_auth_token(session, config, token['csrf_token'])
    embed_payload = {
        '0': {
            'json': {
                'document_ids': [
                    f"{rag_doc_id}",
                ],
                'agent_id': f"{agent_id}",
                'chunk_overlap': chunk_overlap,
                'chunk_size': chunk_size
            }
        }
    }

    # Add the specific cookie to the session
    response = session.post(f'{config['api_base_url']}/trpc/documents.embedPdfDocuments?batch=1', json=embed_payload, headers={**config['default_headers']}, verify=False)
    #raise Exception(session.cookies.get_dict(), response.json())
    response.raise_for_status()  
    return

def run_module():
    
    # Define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        rag_agent_id=dict(type='str', required=True),
        rag_document_id=dict(type='str', required=False),
        rag_file_name=dict(type='str', required=False),
        rag_file_url=dict(type='str', required=False),
        rag_tmp_directory=dict(type='str', required=False),
        rag_keep_files=dict(type='bool', required=False, default=False),
        rag_chunk_overlap=dict(type='int', required=False),
        rag_chunk_size=dict(type='int', required=False),
        method=dict(type='str', required=True, choices=['LIST', 'CREATE', 'UPDATE', 'GET_BY_ID', 'DELETE']),
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
    method = module.params['method']
    rag_agent_id = module.params['rag_agent_id']
    rag_document_id = module.params['rag_document_id']
    rag_file_name = module.params['rag_file_name']
    rag_file_url = module.params['rag_file_url']
    rag_chunk_overlap = module.params['rag_chunk_overlap']
    rag_chunk_size = module.params['rag_chunk_size']
    rag_tmp_directory = module.params['rag_tmp_directory']
    rag_keep_files = module.params['rag_keep_files']
    if rag_tmp_directory is None:
        rag_tmp_directory = config['default_tmp_directory']
    headers = {**config['default_headers']}
    
    try:
        if method == 'LIST':
            response = requests.get(f'{config['api_base_url']}/v1/documents?agent_id={rag_agent_id}', headers=headers, verify=False)
        elif method == 'CREATE':
            if rag_file_name is not None and rag_file_url is not None:
                
                new_document_id = create_document(config, rag_agent_id, rag_file_name)
                x_azm_payload = generate_upload_url(config, new_document_id)
                file_path = upload_file(rag_file_url, x_azm_payload['rag_upload_url'], rag_file_name, x_azm_payload, rag_tmp_directory)
                update_document(config, new_document_id)
                embed_document(config, rag_agent_id, new_document_id, rag_chunk_overlap, rag_chunk_size)
                if not rag_keep_files:
                    remove_file(file_path)

                response = requests.get(f'{config['api_base_url']}/v1/documents/{new_document_id}', headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_file_name required parameter missing!")     
        elif method == 'GET_BY_ID':
            if rag_document_id is not None:
                response = requests.get(f'{config['api_base_url']}/v1/documents/{rag_document_id}', headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_document_id required parameter missing!")      
        elif method == 'DELETE':
            if rag_document_id is not None:
                response = requests.delete(f'{config['api_base_url']}/v1/documents/{rag_document_id}', headers=headers, verify=False)
            else:
                module.fail_json(msg="rag_document_id required parameter missing!")     
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
