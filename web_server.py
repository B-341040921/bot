from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
  return "a"

def run_web_server():
  app.run(host='74.220.48.0/24', port=8080) # Render server IP, change Oct 27

def keep_alive():
  t = Thread(target=run_web_server)
  t.start()
