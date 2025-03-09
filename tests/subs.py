import subprocess
import time


app = subprocess.Popen(
    f"""conda activate arima && python ./utils/mjpg_serve_2.py""", shell=True
)

print(app.pid)
time.sleep(5)
app.terminate()
app.kill()
