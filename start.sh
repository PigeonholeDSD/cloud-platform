#!/bin/bash

service nginx start
gunicorn -b unix:/tmp/gunicorn.sock app:app
