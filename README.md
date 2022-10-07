Python modules to be installed:

1. flask
2. requests
3. pickle

Setup: 

Unix Bash (Linux, Mac, etc.):

export FLASK_APP=main
flask run

Windows CMD:

set FLASK_APP=main
flask run

Windows PowerShell:

$env:FLASK_APP = "main"
flask run


Copy the url which will look something like 'http://127.0.0.1:5000' 
The 'from' field has auto complete but sadly we were not able to do the same for 'To', So you may want to ensure that the stop exists in database by cross checking it with 'From' auto complete

The request may take a while to complete as the code has to go through 9,00,000 rows of data
