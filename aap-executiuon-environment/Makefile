# Make targets for building the IBM example helloworld edge service


COLLECTION_VERSION:=1.1.0
COLLECTION_NAMESPACE:=ibm
COLLECTION_NAME:=ce_emea_rag

all: build 

build:
	#ansible-builder build --build-arg platform=linux/arm64 -t quay.io/tncibmniceteam/custom-ee-ssl-rag-rhel8:1.0.0-690
	ansible-builder build --build-arg platform=linux/arm64 -t quay.io/tncibmniceteam/custom-ee-ssl-rag-rhel8:1.0.0-690
	#ansible-builder create
	#podman manifest create ee-test-111
	#podman build --platform=linux/amd64 --manifest ee-test-111 -f context/Containerfile -t quay.io/tncibmniceteam/custom-ee-ssl-rag-rhel8:latest

