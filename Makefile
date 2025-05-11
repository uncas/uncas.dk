venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || python3 -m venv .venv
	source .venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	touch .venv/touchfile

build:
	dotnet publish uncas.dk --runtime win-x86 --self-contained

upload: venv
	source .venv/bin/activate
	python3 upload.py

deploy: build upload
