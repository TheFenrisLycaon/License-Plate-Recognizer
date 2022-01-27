import urllib.parse
import urllib.request
from datetime import datetime

import private.secrets as sec


def sms(apikey, numbers, sender, message):
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


api = sec.LOCAL
resp = sms(api, "919123415629", "Specy", "Testing...")
print(resp)
