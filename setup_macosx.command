#!/bin/bash

cd bill_creator
rm -rf venv
/usr/local/git/bin/git pull 
virtualenv venv
source venv/bin/activate
pip install -r requirement.txt
