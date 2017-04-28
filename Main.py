from user import HoughCircle.py
import urllib2
import requests
from PIL import Image

#Get image from the camera. Then make changes to HoughCircle class to take in the image.
houghCircle = HoughCircle('houghImage.jpg')

#Get the cropped image from the identified circle
circle = houghCircle.circles[0]
iris = houghCircle.cimg.crop((circle[0] - circle[2], circle[1] - circle[2], circle[0] + circle[2], circle[1] + circle[2]))
iris.save("iris.jpg")

url = 'http://192.168.43.193:9876/Service1.svc/UploadImage/post'
files = {'file': open('iris.jpg', 'rb')}

r = requests.post(url, files=files)
r.text
