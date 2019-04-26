.PHONY: docker help

VERSION ?= latest

help:
	@echo "Usage: make docker VERSION"

docker:
	docker build --tag pilosa/getting-started:$(VERSION) .
