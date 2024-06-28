# Make targets for building the IBM example helloworld edge service


COLLECTION_VERSION:=1.0.0
COLLECTION_NAMESPACE:=ceemea
COLLECTION_NAME:=rag

all: build run

build:
	ansible-galaxy  collection build --force . 
	ansible-galaxy collection install --force $(COLLECTION_NAMESPACE)-$(COLLECTION_NAME)-$(COLLECTION_VERSION).tar.gz
run:
	ansible-playbook examples/$(playbook)

