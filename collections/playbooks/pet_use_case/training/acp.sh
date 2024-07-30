#!/usr/local/bin/bash

ansible-content-parser --skip-ansible-lint --source-description "Ansible modules collection for PetStore API" --source-license IBM  --repo-name "IBM PetStore Ansible Collections" --repo-url https://gitlab.cagip-wca.mop.ibm/cagip-wca4al/cagip-wca-for-ansible-lightspeed/-/tree/main/use_case_4/collections/playbooks/pet_use_case/training/playbooks  ./playbooks/ ./CustomModel-$$
echo "Output directory: CustomModel-$$"
