#!/usr/bin/python
import os
import signal
import subprocess
import sys
import time

import cv2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

capture = None
global server


# Class that sets up HTTP Server and Converts - We need not modify this
class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # rtsplink = self.path[1:]
        print(rtsplink)
        try:
            self.send_response(200)
            self.send_header(
                "Content-type", "multipart/x-mixed-replace; boundary=--jpgboundary"
            )
            self.end_headers()
            capture = cv2.VideoCapture(rtsplink)
            print("client connected")
            while capture.isOpened():
                try:
                    rc, img = capture.read()
                    if rc == True:
                        imgRGB = img
                        # cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                        # imgRGB = cv2.resize(imgRGB,(1060,460))
                        imgRGB = cv2.resize(imgRGB, (640, 360))
                        r, buf = cv2.imencode(".jpg", imgRGB)
                        self.wfile.write("--jpgboundary\r\n")
                        self.send_header("Content-type", "image/jpeg")
                        self.send_header("Content-length", str(len(buf)))
                        self.end_headers()
                        self.wfile.write(bytearray(buf))
                        self.wfile.write("\r\n")
                        # time.sleep(0.005)
                    else:
                        continue
                except Exception as e:  # KeyboardInterrupt:
                    print("Exception in Capturing", e)
                    break
            capture.release()
            return
        except Exception as e:
            print("Client Disconnected", e)
            return


def killProcess(port):
    try:
        command = "netstat -tnp | grep " + str(port)  # linux
        # command = "netstat -aon | findstr " + str(port)
        print("Command : ", command)
        c = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = c.communicate()
        # Getting process id of the existing HTTP Server process
        pid = int(stdout.decode().strip().split(" ")[-1].split("/")[0])
        print(pid)
        os.kill(pid, signal.SIGTERM)
        print("process killed")
    except Exception as e:
        print("All Existing HTTP Servers killed. Killing Process Exception - ", str(e))
    # Sleep for 2 seconds is necessary for HTTP Servers to restart again
    time.sleep(2)


def main(rtsp):
    global rtsplink
    global capture
    rtsplink = rtsp
    # While loop just in case rtsp link returns error
    while 1:

        # Starting new HTTP Server for our stream
        try:
            # killProcess(9090)  # Killing existing HTTP servers to start a new one
            server = HTTPServer(("192.168.244.43", int(9090)), CamHandler)
            print("Server Started")
            server.serve_forever()
        except Exception as e:
            # capture.release()
            # server.socket.close()
            print("Exception in Main", e)
        # killProcess(9090)


if __name__ == "__main__":
    try:
        # main("http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg")  #
        main(
            "rtsp://admin:v1ps@123@202.61.120.78:5544/Streaming/Channels/101"
        )  # ("http://182.65.247.87:8082/AST")
    except Exception as e:
        print("Exception in calling main..", e)
