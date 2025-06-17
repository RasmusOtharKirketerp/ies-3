
import requests
bearer_token = "AAAAAAAAAAAAAAAAAAAAAMpprAEAAAAAEDyK%2Fp%2Fg6mFfrcY6viqsnUjowc8%3DhuKZ5jZOmnowj5vXIJKQwu17EVJp3jji4eLvJS6v9yWNlY6hdq"

url = "https://api.twitter.com/2/tweets/search/recent"

headers = {"Authorization": f"Bearer {bearer_token}"}   

response = requests.request("GET", url, headers=headers)

print(response.text)