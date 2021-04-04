# HP House Points App

This is a small application that allows admins to add/remove points to 4 harry potter houses (Gryffindor, Slything, Ravenclaw and Hufflepuff).
It is built using python3 + flask (web framework) + google appengine (runtime) + firestore (database).

# Deployment:
This is only possible if you are an owner of the google project. You'll need to have installed the [gcloud command line tool](https://cloud.google.com/sdk/gcloud).
```
$ gcloud app deploy
```

# Local development
If you want to run the server locally, all you need is python3. Note that the local development talks to the production database right now, which is not ideal.

1. Create a python virtualenv with the right dependencies (`pip install virtualenv` if you don't have virtualenv)
2. pip install the requirements
3. run the local server

### Commands

```
$ virtualenv venv  # you can use any name, I usually use "venv"
$ source venv/bin/activate  # activate it
$ pip install -r requirements.txt
$ python main.py
```
