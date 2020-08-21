#!/bin/bash
#jupyter nbconvert --to notebook --execute covid19-italia.ipynb
#jupyter nbconvert --to notebook --execute covid19-piemonte.ipynb
#jupyter nbconvert --to notebook --execute covid19-lombardia.ipynb
#jupyter nbconvert --to notebook --execute covid19-internazionale.ipynb
jupyter nbconvert --template=nbextensions --to=plotlyhtml covid19-italia.ipynb
jupyter nbconvert --template=nbextensions --to=plotlyhtml covid19-piemonte.ipynb
jupyter nbconvert --template=nbextensions --to=plotlyhtml covid19-lombardia.ipynb
jupyter nbconvert --template=nbextensions --to=plotlyhtml covid19-internazionale.ipynb
cp covid19-*.html ../iosand71.github.io/
cd ../iosand71.github.io
git add .
git commit -m "update covid reports"
git push origin master
cd ../covid19
rm covid19-*.html
