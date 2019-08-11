.PHONY: zip
zip:
	rm func.zip || true
	cd venv/lib/python3.6/site-packages && zip -r9 ../../../../func.zip . && cd ../../../../
	zip -g func.zip func.py

setup:
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

clean:
	rm func.zip || true
	deactivate || true
	rm -rf venv || true