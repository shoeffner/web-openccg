app/openccg_parser.py: OpenCCG.ebnf
	tatsu --generate-parser $< --outfile $@
