import urllib2
import requests

url = 'http://192.168.43.193:9876/Service1.svc/post'
files = {'file': open('report.xls', 'rb')}

r = requests.post(url, files=files)
r.text