# Centrifuge Module

Minimize the evasion sample and feedback to the corpus.

## Usage

1. Put sample into evasion directory

For example
```
cp -r ../fuzzer/atheris_fuzzer/fuzzing/solution/test/*.input ./evasion
```

or you can config the `EVASION_DIR` in config.py

2. Config your running WAF with WAF validator and your running web validator in `config.py`

3. Run centrifuge task with centrifuge.py

```
python centrifuge.py
```

4. HTTP request data will store in `MINI_EVASION_DIR`. And the corresponding http request sample will store in `MINI_SAMPLE_DIR`
