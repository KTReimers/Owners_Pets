from flask import Flask
import logging #this is extra for deployment. to see traceback errors
logging.basicConfig(filename='errorLog.log', level=logging.ERROR)
app = Flask(__name__)
app.secret_key = "shhhhhh"