#!/bin/sh

echo "Create a Django app:" $1
python3 manage.py startapp $1
