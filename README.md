1. `easy_install-2.7 virtualenv`
2. `cd <folder>`
3. `virtualenv --no-site-packages .`
4. `source bin/activate`
5. create and open a new file called requirements.txt

```
Flask>=0.8
twilio>=3.3.6
pyserial
logging
```

6. `bin/pip install -r requirements.txt`
7. `python run.py`
