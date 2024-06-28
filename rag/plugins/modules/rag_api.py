#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests
import os
import json 

def run_module():
    # Define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        url=dict(type='str', required=True),
        method=dict(type='str', required=True, choices=['GET', 'POST', 'PUT']),
        headers=dict(type='dict', required=False, default={}),
        payload=dict(type='dict', required=False, default={}),
        file_url=dict(type='str', required=False, default=None)
    )

    # Seed the result dict in the object
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # The AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Load configuration from JSON file
    config = load_config(module)
    
    # If the module is in check mode, do not make any changes
    if module.check_mode:
        module.exit_json(**result)

    # Extract the parameters from the Ansible module input
    url = module.params['url']
    method = module.params['method']
    headers = module.params['headers']
    payload = module.params['payload']
    file_url = module.params['file_url']

    try:
        # Download the file if file_url is provided
        file_path = None
        if file_url and method == 'PUT':
            local_filename = file_url.split('/')[-1]
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Check if the download request was successful
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            file_path = local_filename

        # Perform the HTTP request
        if method == 'POST':
            response = requests.post(url, headers=headers, json=payload)
        elif method == 'GET':
            response = requests.get(url, headers=headers, params=payload)
        elif method == 'PUT':
            if file_path:
                with open(file_path, 'rb') as f:
                    files = {'file': (file_path, f)}
                    response = requests.put(url, headers=headers, files=files)
                # Clean up the downloaded file
                os.remove(file_path)
            else:
                response = requests.put(url, headers=headers, json=payload)
        
        response.raise_for_status()  # Raise an error for bad status codes
        result['changed'] = True
        result['original_message'] = payload if method in ['POST', 'PUT'] else None
        result['message'] = response.json()
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=str(e), **result)

    # Exit the module and return the result
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
