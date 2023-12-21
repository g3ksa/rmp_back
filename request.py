import requests

url = "http://localhost:5000/uploadfile/"
files = {"image": ("image.jpg", open("image.jpg", "rb"), "image/jpeg")}
response = requests.post(url, files=files)

print(response.json())
