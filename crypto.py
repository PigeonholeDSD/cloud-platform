
import os
import os.path
import time
import hmac
import uuid
import shutil
import hashlib
import tarfile
from tempfile import mkdtemp
from flask import current_app
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
import error


def cloud_key() -> SigningKey:
    try:
        if 'CLOUD_KEY' in current_app.config:
            return current_app.config['CLOUD_KEY']
    except RuntimeError:
        pass
    try:
        if not os.path.isfile('cloud.key'):
            print('warning: generated cloud key')
            key = SigningKey.generate()
            with open('cloud.key', 'wb') as f:
                f.write(key.encode())
            with open('cloud.pub', 'wb') as f:
                f.write(key.verify_key.encode())
        with open('cloud.key', 'rb') as f:
            return SigningKey(f.read())
    except:
        print('fatal: Error loading CLOUD_KEY')
        exit(2)


def sign(data: str) -> str:
    return cloud_key().sign(data.encode(), encoder=HexEncoder).signature.decode()


def verify(data: str, sig: str, pub: str = None) -> bool:
    if pub:
        verify_key = VerifyKey(pub.encode(), encoder=HexEncoder)
    else:
        verify_key = cloud_key().verify_key
    try:
        verify_key.verify(data.encode(), HexEncoder().decode(sig.encode()))
        return True
    except:
        return False


def hash_file(file: str) -> str:
    h = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sign_file(file: str) -> str:
    return sign(hash_file(file))


def timestamp(_time: int = 0) -> str:
    t = str(int(_time if _time else time.time()))
    sig = hmac.new(cloud_key().encode(), t.encode(), hashlib.sha1).hexdigest()
    return t+':'+sig


def check_ticket(ticket: str, devid: uuid.UUID) -> None:
    try:
        t, tsig, sig, pubkey, cert = ticket.split(':')
        ts = t+':'+tsig
        if timestamp(int(t)) != ts:
            raise error.NotLoggedIn('Invalid timestamp in device ticket')
        if int(t)+current_app.config['TICKET_LIFETIME'] < time.time():
            raise error.NotLoggedIn('Timestamp expired')
        if not verify(ts, sig, pubkey):
            raise error.NotLoggedIn('Invalid timestamp signature')
        if not verify(pubkey+str(devid), cert):
            raise error.NotLoggedIn('Invalid pubkey')
    except error.DSDException as e:
        raise e
    except Exception:
        raise error.NotLoggedIn('Invalid device ticket')


def check_file(file: str, sig: str, devid: uuid.UUID) -> None:
    try:
        sig, pubkey, cert = sig.split(':')
        hash = hash_file(file)
        if not verify(hash, sig, pubkey):
            raise error.SignatureError('Invalid file signautre')
        if not verify(pubkey+str(devid), cert):
            raise error.SignatureError('Invalid file pubkey')
    except error.DSDException as e:
        raise e
    except Exception:
        raise error.SignatureError('Invalid signature')


def sign_device(devid: uuid.UUID):
    tmp_dir = mkdtemp()
    with open(os.path.join(tmp_dir, 'id'), 'w') as f:
        f.write(str(devid))
    device_key = SigningKey.generate()
    with open(os.path.join(tmp_dir, 'device.key'), 'wb') as f:
        f.write(device_key.encode())
    device_pubkey = device_key.verify_key.encode(HexEncoder).decode()
    device_cert = sign(device_pubkey+str(devid))
    with open(os.path.join(tmp_dir, 'device.crt'), 'w') as f:
        f.write(device_pubkey+':'+device_cert)
    with tarfile.open(str(devid)+'.tar', "w") as tar:
        tar.add(name=os.path.join(tmp_dir, 'id'), arcname='id')
        tar.add(name=os.path.join(tmp_dir, 'device.key'), arcname='device.key')
        tar.add(name=os.path.join(tmp_dir, 'device.crt'), arcname='device.crt')
        tar.add(name='cloud.pub', arcname='ca.pub')
    shutil.rmtree(tmp_dir)
