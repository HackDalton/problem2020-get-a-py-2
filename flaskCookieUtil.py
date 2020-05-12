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


key = b'\xce\x11s\xbcZ\xc1\xa4\x08\x1fX\xf5A!\xa1\xe68'

decoded = decode_flask_cookie(
    key, "eyJpZCI6M30.Xrn2PQ.oyV0iTyu3XiLOZpPJmRHWdVvMmE")

print(decoded)

encoded = encode_flask_cookie(key, {'id': 1})
print(encoded)
