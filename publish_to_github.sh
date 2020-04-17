#!/bin/bash
jupyter nbconvert --template=nbextensions --to=html covid19-italia.ipynb
cp covid19-italia.html ~/Projects/iosand71.github.io/
cd ~/Projects/iosand71.github.io
git add .
git commit -m "update covid report"
git push origin master
