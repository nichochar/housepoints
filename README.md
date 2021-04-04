# HP House Points App

This is a small application that allows admins to add/remove points to 4 harry potter houses (Gryffindor, Slything, Ravenclaw and Hufflepuff).
It is built using python3 + [flask](https://flask.palletsprojects.com/en/1.1.x/) (web framework) + [google appengine](https://cloud.google.com/appengine) (runtime) + [firestore](https://cloud.google.com/firestore) (database).

![](static/app_screenshot.png)


# Deployment:

This is only possible if you are an owner of the google project (only myself at this point). You'll need to have installed the [gcloud command line tool](https://cloud.google.com/sdk/gcloud).
```
$ gcloud app deploy
```

# Local development
If you want to run the server locally, all you need is python3 and pip. Note that the local development talks to the production database right now, which is not ideal.

1. Create a python virtualenv with the right dependencies (`pip install virtualenv` if you don't have virtualenv)
2. pip install the requirements
3. run the local server

### Commands

```
$ virtualenv venv                   # create a virtualenv called "venv"
$ source venv/bin/activate          # activate it
$ pip install -r requirements.txt   # install the requirements in it
$ python main.py                    # run the server in it
```
