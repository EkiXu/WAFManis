# WAF Manis Implmentation with Atheris

## Setup Environment

```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Example: Fuzz with flask

1. Setup

```
pip install -r ./webapp_validator/python_app/flask_app/requirements.txt
```

configure your waf setting in `config.py`

2. Generate initial seeds

```
python gen_initial_seed.py 10
```

3. Fuzzing

```
python fuzzer.py ./inital_seed
```

Evasion case will save to fuzzing/solution by default, then you can minimize it with centrifuge and feedback to corpus


