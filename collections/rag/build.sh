

cd /Users/livigni/Documents/TNC/WCA4A/clients/CAGIP/playbooks/cagip/uc4/collection/ceemea/rag
ansible-galaxy  collection build --force . 

ansible-galaxy collection install ceemea-rag-1.0.0.tar.gz