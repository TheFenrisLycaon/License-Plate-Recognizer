# AST

## Steps

- Run ```python2 utils\mjpg_serve_2.py``` to start the video server.
- Run ```ngrok http 127.0.0.1:5000``` to start the ngrok server.
- Run the main script as ```python3 main.py```
- Run ```python3 app.py``` to test out the Flask app only

## Change IP

- Change IP at [here](templates\index.html) line 18
- Change IP at [here](utils\mjpg_serve_2.py) line 84
