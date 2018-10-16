app/openccg_parser.py: OpenCCG.ebnf
	tatsu --generate-parser $< --outfile $@

.PHONY: run
run:
	docker-compose run -p 5000:5000 -v $$(pwd)/app:/app openccg python3 /app/ccgapp.py
