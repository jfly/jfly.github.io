.DEFAULT_GOAL := build

out ?= ./_site

.PHONY: run
run:
	jekyll serve --watch --source ./src --destination $(out)

.PHONY: build
build:
	jekyll build --source ./src --destination $(out)
