# CAGIP WCA for Ansible Lightspeed - RAG API Sample

## API Key & Model ID


* API Key: al2xx67KXpMt13aKzm1gJXEpkzOeB3C1sZRCdFRFS0y9
* Base Model ID: e91406f5-6d8c-4616-bd31-08264637f4d2<|sepofid|>granite-3b
* Custom Model ID: e91406f5-6d8c-4616-bd31-08264637f4d2<|sepofid|>451d2163-4f05-4e17-9b0b-2343dbca5395
* JSONL training file [output-ftdata-54733.jsonl](./training/CustomModel-54733/output-ftdata-54733.jsonl)
* Collection tarball: [ibm-ce_emea_petstore-1.0.0.tar.gz](../../ibm/petstore/ibm-ce_emea_petstore-1.0.0.tar.gz)

## install the collection locally on your local ansible environment
```
ansible-galaxy collection install --force ibm-ce_emea_petstore-1.0.0.tar.gz
```