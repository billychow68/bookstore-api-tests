all: install test
	#install lint test
	
setup:
	python3 -m venv ~/.bookstore_api
	echo "alias bookstore='source ~/.bookstore_api/bin/activate'" >> ~/.bash_profile
	source ~/.bash_profile

install:
	# pip3 install --upgrade pip && pip3 install -r requirements.txt
	pip3 install --upgrade --user pip && pip3 install --user -r requirements.txt

test:
	# pytest -s -v --setup-show -p no:randomly --html=reports/report.html --self-contained-html
    	# pytest -s -v --setup-show -n auto --html=reports/report.html --self-contained-html --capture=sys
	pytest -v --setup-show -n auto --count=1
	# pytest -s -v --setup-show -n auto -p no:randomly --html=reports/report.html --self-contained-html
	# pytest -s -v --setup-show -n auto -p no:randomly --html=reports/report.html --self-contained-html --count=10

smoketest:
	pytest -v --setup-show -n auto -m "smoketest"

lint:
	pylint tests

