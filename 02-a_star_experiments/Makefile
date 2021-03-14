RESULTS=results/

.PHONY: test
test: informed_search_experiments.py heuristics.py
	@rm -rf $(RESULTS) && mkdir $(RESULTS)
	@for test in Heuristics2D Heuristics3D Density Repetition ; do \
		echo test $$test ; \
			python3 informed_search_experiments.py $$test >$(RESULTS)/$$test.csv ; \
	done

.PHONY: clean
clean:
	rm -rf $(RESULTS)
