import requests
from requests.structures import CaseInsensitiveDict

email = "email@mail.com"

# json post curl
url = "https://reqbin.com/echo/post/json"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
data = '{"login":'+email+',"password":"password112233"}'

resp = requests.post(url, headers=headers, data=data)
print("Data:", data)
print("Status:", resp.status_code)