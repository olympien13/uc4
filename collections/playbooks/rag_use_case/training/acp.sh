#!/usr/local/bin/bash

ansible-content-parser --skip-ansible-lint --source-description "Ansible modules collection for Specific API agentx API" --source-license IBM  --repo-name "IBM RAG agentx API Ansible Collections" --repo-url https://gitlab.cagip-wca.mop.ibm/cagip-wca4al/cagip-wca-for-ansible-lightspeed/-/tree/main/use_case_4/collections/playbooks/rag_use_case/training/playbooks/examples-custom-single-task-specific-api  ./playbooks/examples-custom-single-task-specific-api ./CustomModel-$$
echo "Output directory: CustomModel-$$"
