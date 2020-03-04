.PHONY: test
test: informed_search_experiments.py heuristics.py
	@rm -rf out && mkdir out
	@for test in Heuristics2D Heuristics3D Density Repetition ; do \
		echo test $$test ; \
			python3 informed_search_experiments.py $$test >out/test-$$test.csv ; \
	done

.PHONY: clean
clean:
	rm -rf out
