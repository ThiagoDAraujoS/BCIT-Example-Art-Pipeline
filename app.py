from flask import Flask
from App.ShowManager.Manager import Manager

manager: Manager = Manager()
app = Flask(__name__)
