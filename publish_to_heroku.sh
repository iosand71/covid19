jupyter nbconvert --template=nbextensions --to=html covid19-italia.ipynb
cp covid19-italia.html ~/Projects/iosand/public/
cd ~/Projects/iosand/
git add .
git commit -m "update covid report"
git push heroku master
