venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || virtualenv .venv
	. .venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	touch .venv/touchfile

deploy: venv
	. .venv/bin/activate
	python3 deploy.py
