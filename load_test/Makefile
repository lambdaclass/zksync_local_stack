.PHONY: run.server run.loadtest tests

run.server:
	python -m flask --app api/app.py run

run.loadtest:
	python main.py

tests:
	python tests/pipeline_tests.py