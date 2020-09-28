### What it is
Downloads docs from a goole drive folder and renders them as markdown

### Instructions

0. Go to your folder and grab the id from the url. Put the id in a `id.txt`

1. Go to https://developers.google.com/docs/api/quickstart/python and do step 1 to get the credentials.json file (select "desktop app" if it asks)

2. Put credentials.json in the working directory

3. Go to https://console.developers.google.com/ and add the drive api to the project you just created

4. `virtualenv venv`

5. `. venv/bin/activate`

6. `pip install -r requirements.txt`

7. `./render`
