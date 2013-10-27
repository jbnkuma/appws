import pycurl

def md5_request(self):

    try:
        url = "http://192.168.0.21:8000" + "login"
        request = pycurl.Curl()
        request.setopt(request.URL, url)
        request.setopt(request.POSTFIELDS, 'ip=' + str(server))
        request.setopt(request.TIMEOUT,2)
        request.perform()

    except:
        pass