app/generated_openccg_parser.py: OpenCCG.ebnf
	tatsu --generate-parser $< --outfile $@

.PHONY: build
build:
	docker build . -t web-openccg
	# Copy over the viz.js files for the local development server (mounting would otherwise overwrite it)
	docker run --rm --detach --name web-openccg web-openccg
	docker cp web-openccg:/app/static ./app/static
	docker stop web-openccg

.PHONY: run
run:
	docker run --rm -p 5000:5000 -v $$(pwd)/app:/app:ro web-openccg python3 /app/ccgapp.py

.PHONY: test
test:
	docker run --rm -v $$(pwd)/app:/app -v $$(pwd)/tests:/tests:ro web-openccg python3 -m unittest discover /tests
