.PHONY: container clean_container

container:
	docker build -t $(shell basename $(CURDIR)):$(shell grep 'version' ./pyproject.toml | cut -d'"' -f2) -f ./Dockerfile .

clean_container:
	-docker rmi -f $(shell basename $(CURDIR)):$(shell grep 'version' ./pyproject.toml | cut -d'"' -f2)