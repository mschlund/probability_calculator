
.PHONY: clean
clean:
	rm dist/*

.PHONY: build
build:
	python3 -m build

.PHONY: upload
upload:
	python3 -m twine upload dist/*

.PHONY: test
test:
	python3 -m pytest -v

.PHONY: generate_readme
generate_readme:
	jupyter nbconvert --to markdown --output-dir . docs/README.ipynb
