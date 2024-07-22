import json
import os 
import zipfile

# def load_config():
#     #module_path = os.path.abspath(__file__)[:-8] + 'config.json'
#     module_path = os.path.abspath(__file__)[:-8] 
#     file_path = os.path.join(module_path, 'config.json')
#     with open(file_path, 'r') as config_file:
#         config = json.load(config_file)
#     return config

def remove_file(file_path):
    try:
        os.remove(file_path)
        #raise Exception(f"File {file_path} has been removed successfully.")
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")
    except PermissionError:
        raise Exception(f"Permission denied: cannot delete {file_path}.")
    except Exception as e:
        raise Exception(f"Error occurred while trying to delete {file_path}: {e}")

def get_config():

    return {
        "default_tmp_directory": "/tmp",
        "default_headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        "timeout": 30
}

def get_update_document_payload():
    return {
        "name": "string",
        "is_embedding": False,
        "is_uploaded": False
    }

def get_agent_payload(): 
    return {
        "collection_embeddings_index_type": "FLAT",
        "collection_embeddings_metric_type": "L2",
        "decoding_method": "greedy",
        "cache_enabled": False,
        "cache_score_threshold": 0.2,
        "description": "string",
        "knowledge_enabled": False,
        "knowledge_rerank_enabled": True,
        "knowledge_rerank_score_threshold": 0.5,
        "knowledge_rerank_embeddings_limit": 100,
        "knowledge_score_threshold": 10,
        "knowledge_embeddings_limit": 10,
        "name": "string",
        "model_id": "meta-llama/llama-3-70b-instruct",
        "repetition_penalty": 1,
        "min_new_tokens": 1,
        "max_new_tokens": 1000,
        "temperature": 1,
        "top_k": 1,
        "top_p": 50,
        "share_enabled": False,
        "share_branding_enabled": True,
        "system_prompt": "You are a helpful assistant that supports users. You respond in valid markdown format. Your answers are concise and a relevant to the question.",
        "knowledge_prompt": "Use the data provided between the <DATA> and </DATA> tags to answer the users query. Do not answer general knowledge questions.",
        "knowledge_prompt_fallback": "",
        "knowledge_response_prefix": "Based on information in the **{document_names}** ",
        "knowledge_response_prefix_fallback": "",
        "knowledge_response_stop_sequence_fallback": "",
        "workspace_id": "string"
    }

