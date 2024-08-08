# django-couchDB

You must change in settings.py and generate_data.py this line:

client = CouchDB("admin", "admin", url='http://127.0.0.1:5984', connect=True)

you must put the couchdb credentials for the connection.

Run generate_data.py 

Then use python manage.py runserver