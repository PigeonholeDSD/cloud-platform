# python3 train.py <data_dir> <new_model> <base_model>

import time
import shutil
import os.path
import threading
import subprocess
from tempfile import mkdtemp
import db.device
import db.model

_tasks = {}
_stops = {}


def notify(device: db.device.Device) -> None:
    print(
        f'Sending email to {device.email}, notifying new model for {device.id}')


def __train(device: db.device.Device, stop: threading.Event) -> None:
    print(f'Starting training for {device.id}')
    new_model = os.path.join(mkdtemp(), 'model')
    proc = subprocess.Popen(
        ['/usr/bin/env', 'python3', 'train.py', device.calibration,
            new_model, device.model or db.model.getBase()],
        cwd='algo'
    )
    while not stop.is_set():
        try:
            if proc.wait(5) is not None:
                break
        except subprocess.TimeoutExpired:
            pass
    else:
        print(f'Terminating running train process of {device.id}')
        while proc.poll() is None:
            proc.terminate()
            time.sleep(1)
            proc.kill()
    if proc.returncode == 0:
        print(f'Finished training for {device.id}')
        device.model = new_model
        threading.Thread(target=notify, args=(device)).start()
    else:
        print(f'Training for {device.id} failed returning {proc.returncode}')
    shutil.rmtree(os.path.dirname(new_model))


def _train(device: db.device.Device) -> None:
    if device.id in _tasks:
        while _tasks[device.id].is_alive():
            print(
                f'Training for {device.id} is still running! Terminating first...')
            _stops[device.id].set()
            time.sleep(5)
    _stops[device.id] = threading.Event()
    _tasks[device.id] = threading.Thread(
        name=str(device.id),
        target=__train,
        args=(device, _stops[device.id])
    ).start()


def train(device: db.device.Device) -> None:
    threading.Thread(target=_train, args=(device)).start()
