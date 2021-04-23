# Gate Annotation Service

A service for collaborative document annotation. Project plan can be found here:

[https://docs.google.com/document/d/1NDV17vQKugBOffT56NANtxEiRU0EuJ6MzdKhfC5rAII](https://docs.google.com/document/d/1NDV17vQKugBOffT56NANtxEiRU0EuJ6MzdKhfC5rAII)


## Django settings files

Django settings are located in `annotation_tool/setttings` folder. The app will use `base.py` setting by default
and this must be overridden depending on use.

### Secret

A `secret.py` should be created to hold settings that should not be made public by tracking through version
control. The format of the file should be as follows:

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+rh5#u6=19q90g$)e%ca&wpfjsju*5*=9b#ah2b&dlwpkx%4$o'

```

## Backend Testing

## Integration testing

cypress




