app/generated_openccg_parser.py: OpenCCG.ebnf
	tatsu --generate-parser $< --outfile $@

.PHONY: run
run:
	docker run --rm -p 5000:5000 -v $$(pwd)/app:/app:ro web-openccg python3 /app/ccgapp.py

.PHONY: test
test:
	docker run --rm -v $$(pwd)/app:/app:ro -v $$(pwd)/tests:/tests:ro web-openccg python3 -m unittest discover /tests
