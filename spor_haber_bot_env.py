import requests

url = "https://betting-tips-api.p.rapidapi.com/livescores/list"

headers = {
    "x-rapidapi-host": "betting-tips-api.p.rapidapi.com",
    "x-rapidapi-key": "ea8f9a518amsh15e9cc8c74f4f84p1f9145jsn060bea8736b2"
}

response = requests.get(url, headers=headers)

print("Durum Kodu:", response.status_code)
print("Cevap:", response.text)

