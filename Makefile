all:
	( \
	python3.7 -m venv venv; \
	source venv/bin/activate; \
	pip install antlr4-python3-runtime; \
	) \
