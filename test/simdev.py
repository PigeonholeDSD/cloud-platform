import os
import os.path
import sys
import uuid
import hashlib
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey

keydir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
with open(os.path.join(keydir, 'cloud.key'), 'rb') as f:
    cloud_key = SigningKey(f.read())
with open(os.path.join(keydir, 'cloud.pub'), 'rb') as f:
    ca = VerifyKey(f.read())


class SimDevice:
    def __init__(self, uuid: uuid.UUID = None):
        if not uuid:
            uuid = uuid.uuid4()
        self.uuid = str(uuid)
        self.key = SigningKey.generate()
        device_pubkey = self.key.verify_key.encode(HexEncoder).decode()
        device_cert = cloud_key.sign(
            (device_pubkey+self.uuid).encode(), encoder=HexEncoder).signature.decode()
        self.cert = device_pubkey+':'+device_cert

    def ticket(self, ts: str) -> str:
        return ts+':'+self.sign(ts)

    def sign(self, data: str) -> str:
        return self.key.sign(data.encode(), encoder=HexEncoder).signature+':'+self.cert

    def verify(self, data: str, sig: str) -> bool:
        try:
            ca.verify(data.encode(), HexEncoder().decode(sig))
            return True
        except:
            return False

    def sign_file(self, file: str) -> str:
        return self.sign(hash_file(file))

    def verify_file(self, file: str, sig: str) -> bool:
        return self.verify(hash_file(file), sig)


def hash_file(file: str) -> str:
    h = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
