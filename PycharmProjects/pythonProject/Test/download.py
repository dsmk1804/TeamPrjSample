import requests

url = 'https://bit.ly/fruits_300_data'
response = requests.get(url)
with open('fruits_300.npy', 'wb') as f:
    f.write(response.content)
