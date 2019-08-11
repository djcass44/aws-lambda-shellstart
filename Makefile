.PHONY: zip
zip:
	cd venv/lib/python3.6/site-packages && zip -r9 ../../../../func.zip . && cd ../../../../
	zip -g func.zip func.py