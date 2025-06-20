import requests

url = "https://betting-tips-api.p.rapidapi.com/livescores/list"

headers = {
    "x-rapidapi-host": "betting-tips-api.p.rapidapi.com",
    "x-rapidapi-key": "ea8f9a518amsh15e9cc8c74f4f84p1f9145jsn060bea8736b2"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ Veri başarıyla alındı")
    print(data)
else:
    print(f"❌ Hata oluştu: {response.status_code}")

