# Simple API tests

**Project setup**

- Install <b><a href="https://www.python.org/downloads/">Python</a></b> (v3.7+) and <b><a href="https://pip.pypa.io/en/stable/installation/">PIP</a></b> and add to your System PATH
```
unzip simple_api_tests.zip
cd simple_api_tests
pip install virtualenv
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
```

**Starting auto tests**

```
python -m pytest
```

**Starting auto tests with simple report**
```
python -m pytest --html=report.html
```

**Starting auto tests with allure report**
```
python -m pytest --alluredir=./allure-results
allure serve
```
or
(opens only from IDE)
```
python -m pytest --alluredir=./allure-results
allure generate
```