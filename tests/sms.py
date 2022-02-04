#!/usr/bin/env python

import urllib.parse
import urllib.request

from private import secrets


def sendSMSGET(apikey, numbers, sender, message):
    params = {
        "apikey": apikey,
        "numbers": numbers,
        "message": message,
        "sender": sender,
    }
    f = urllib.request.urlopen(
        "https://api.textlocal.in/send/?" + urllib.parse.urlencode(params)
    )
    return (f.read(), f.code)


def sendSMSPOST(apikey, numbers, sender, message):
    data = urllib.parse.urlencode(
        {"apikey": apikey, "numbers": numbers, "message": message, "sender": sender}
    )
    data = data.encode("utf-8")
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


resp, code = sendSMSGET(secrets.LOCAL, "919123415629", "ARIMA", "Testing ...")
print(resp, code)
resp = sendSMSPOST(
    secrets.LOCAL,
    "919123415629",
    "ARIMA",
    'Dear Customer, Your Vehicle %%|VehicleNumber^{"inputtype" : "text", "maxlength" : "11"}%% is being serviced now.\
    Check out the live video at %%|videolink^{"inputtype" : "text", "maxlength" : "69"}%%',
)

print(resp, code)
