#############################################################################
# Description:
# ------------
# This is an easily makefile file. The purpose is to
# provide an instant building by SoftPymes aplication
#
# Make Target:
# ------------
# init:
# 		run api server
#
# test:
#		run unit tests
#
# doc
#		generate API documentation 
#
#############################################################################


# Internal variables.
SOURCEDIR   = pymes-plus
DOCDIR		= docs


SPHINXOPTS	    = -c $(DOCDIR) -a -E
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(DOCFOLDER)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS)  $(DOCDIR)


init:
	. env3/bin/activate && \
	cd pymes-plus && \
	pwd && \
	gunicorn -w 4 -b 0.0.0.0:5000 run:app

test:
	@echo "unit tests"
	. env3/bin/activate && \
	cd $(SOURCEDIR) && \
	python test.py

doc:
	@echo "generate doc"
	. env3/bin/activate && \
	cd docs/ && \
	make html && \
	doxygen Doxyfile
	

clean:
	cd docs/ && \
	rm -rfv html && \
	make clean