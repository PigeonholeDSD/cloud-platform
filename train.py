# python3 train.py <data_dir> <new_model> <base_model>

import json
import os
import time
import uuid
import shutil
import os.path
import threading
import subprocess
from tempfile import mkdtemp
import db.device

_tasks: dict = {}
_stops: dict = {}


def notify(device: db.device.Device) -> None:
    if device.email:
        print(
            f'Sending email to {device.email}, notifying new model for {device.id}')


def __train(device: db.device.Device, algo_info: dict, stop: threading.Event) -> None:
    print(f'Starting training for {device.id}')
    new_model = os.path.join(mkdtemp(), 'model')
    algo = algo_info['name']
    entry_point = algo_info['entry_point']['train']
    proc = subprocess.Popen(
        [
            *entry_point, 
            device.calibration or '',
            new_model, 
            (
                device.model[algo]
                or db.device.get(uuid.UUID(int=0)).model[algo]
                or algo_info['base'].replace('$ALGO', 'algo')
            )
        ],
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
        device.model[algo] = new_model
        threading.Thread(target=notify, args=(device,)).start()
    else:
        print(f'Training for {device.id} failed returning {proc.returncode}')
    shutil.rmtree(os.path.dirname(new_model))


def _train(device: db.device.Device, algo_info: dict) -> None:
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
        args=(device, algo_info, _stops[device.id])
    )
    _tasks[device.id].start()


def train(device: db.device.Device, algo: str) -> None:
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    algo_info = algo_list[algo]
    for i in range(len(algo_info['entry_point']['train'])):
        algo_info['entry_point']['train'][i] = algo_info['entry_point']['train'][i].replace('$ALGO', 'algo')
    threading.Thread(target=_train, args=(device, algo_info,)).start()
