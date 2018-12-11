CONTAINER_PATH=/app

webopenccg/generated_openccg_parser.py: OpenCCG.ebnf
	docker run --rm --name web-openccg-make -v $$(pwd):/tmp web-openccg tatsu --generate-parser /tmp/$< --outfile /tmp/$@

.PHONY: build
build:
	docker build . --build-arg GRAMMAR_VERSION=legacy/grammar -t web-openccg

webopenccg/static/%.js:
	docker run --rm --detach --name web-openccg-build-$(notdir $@) web-openccg
	docker cp web-openccg-build-$(notdir $@):${CONTAINER_PATH}/$@ $$(pwd)/$@
	docker stop web-openccg-build-$(notdir $@)

.PHONY: run
run: webopenccg/static/viz.js webopenccg/static/lite.render.js
	docker run --rm -p 5000:5000 -v $$(pwd)/webopenccg:${CONTAINER_PATH}/webopenccg:ro --name web-openccg web-openccg python3 ${CONTAINER_PATH}/webopenccg/webapp.py

.PHONY: test
test:
	docker run --rm -v $$(pwd)/webopenccg:${CONTAINER_PATH}/webopenccg:ro -v $$(pwd)/tests:/tests:ro --name web-openccg-test web-openccg python3 -m unittest discover /tests
