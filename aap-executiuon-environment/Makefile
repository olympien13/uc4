# Make targets for building the IBM example helloworld edge service


COLLECTION_VERSION:=1.1.0
COLLECTION_NAMESPACE:=ibm
COLLECTION_NAME:=ce_emea_rag

all: build 

build:
	ansible-builder build -t quay.io/tncibmniceteam/ee-supported-rag-rhel8:latest

