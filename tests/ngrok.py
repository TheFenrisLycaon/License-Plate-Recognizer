import os
import json
from flask import Flask
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)


@app.route("/")
def hello():
    return "Hello Geeks!! from Google Colab"


if __name__ == "__main__":
    app.run()

    # os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    # with open('tunnels.json') as data_file:
    #     datajson = json.load(data_file)

    # msg = "ngrok URL's: \n"
    # for i in datajson['tunnels']:
    #   msg = msg + i['public_url'] + '\n'

    # print(msg)
