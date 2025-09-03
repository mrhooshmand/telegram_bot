import requests

def get_weather(city='mashhad'):
    url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        "key": 'b74cbe49d41b4dbcb9743658253008',
        "q": city,
        "aqi": "no"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")