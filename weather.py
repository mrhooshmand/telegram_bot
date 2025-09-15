import requests


def get_weather(city='mashhad'):
    url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        "key": 'b74cbe49d41b4dbcb9743658253008',
        "q": city,
        "aqi": "yes"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {"data": data, "text": format_weather(data)}
    else:
        print(f"Error: {response.status_code} - {response.text}")


def format_weather(data):
    if not data:
        return "داده‌ای موجود نیست."

    current = data.get('current', {})
    location = data.get('location', {})

    air_quality = current.get('air_quality', {})
    aqi_index = air_quality.get('us-epa-index')

    aqi_text_map = {
        1: "خوب",
        2: "قابل قبول",
        3: "ناسالم برای گروه‌های حساس",
        4: "ناسالم",
        5: "خیلی ناسالم",
        6: "خطرناک"
    }

    condition_fa_map = {
        "Sunny": "آفتابی",
        "Clear": "صاف",
        "Partly cloudy": "نیمه ابری",
        "Cloudy": "ابری",
        "Overcast": "کامل ابری",
        "Mist": "مه",
        "Patchy rain possible": "بارش پراکنده احتمالی",
        "Patchy snow possible": "برف پراکنده احتمالی",
        "Patchy sleet possible": "تگرگ پراکنده احتمالی",
        "Patchy freezing drizzle possible": "بارش پراکنده باران یخ‌زده احتمالی",
        "Thundery outbreaks possible": "رعد و برق احتمالی",
        "Blowing snow": "برف‌کوبی",
        "Blizzard": "طوفان برفی",
        "Fog": "مه",
        "Freezing fog": "مه یخ‌زده",
        "Patchy light drizzle": "باران ریز پراکنده",
        "Light drizzle": "باران ریز",
        "Freezing drizzle": "باران یخ‌زده",
        "Heavy freezing drizzle": "باران یخ‌زده شدید",
        "Patchy light rain": "باران سبک پراکنده",
        "Light rain": "باران سبک",
        "Moderate rain at times": "باران متوسط گاهی",
        "Moderate rain": "باران متوسط",
        "Heavy rain at times": "باران شدید گاهی",
        "Heavy rain": "باران شدید",
        "Light freezing rain": "باران یخ‌زده سبک",
        "Moderate or heavy freezing rain": "باران یخ‌زده متوسط یا شدید",
        "Light sleet": "تگرگ سبک",
        "Moderate or heavy sleet": "تگرگ متوسط یا شدید",
        "Patchy light snow": "برف سبک پراکنده",
        "Light snow": "برف سبک",
        "Patchy moderate snow": "برف متوسط پراکنده",
        "Moderate snow": "برف متوسط",
        "Patchy heavy snow": "برف سنگین پراکنده",
        "Heavy snow": "برف سنگین",
        "Ice pellets": "تگرگ یخ‌زده",
        "Light rain shower": "باران رگباری سبک",
        "Moderate or heavy rain shower": "باران رگباری متوسط یا شدید",
        "Torrential rain shower": "باران سیل‌آسا",
        "Light sleet showers": "رگبار تگرگ سبک",
        "Moderate or heavy sleet showers": "رگبار تگرگ متوسط یا شدید",
        "Light snow showers": "رگبار برف سبک",
        "Moderate or heavy snow showers": "رگبار برف متوسط یا شدید",
        "Light showers of ice pellets": "رگبار تگرگ یخ‌زده سبک",
        "Moderate or heavy showers of ice pellets": "رگبار تگرگ یخ‌زده متوسط یا شدید",
        "Patchy light rain with thunder": "باران سبک پراکنده همراه رعد و برق",
        "Moderate or heavy rain with thunder": "باران متوسط یا شدید همراه رعد و برق",
        "Patchy light snow with thunder": "برف سبک پراکنده همراه رعد و برق",
        "Moderate or heavy snow with thunder": "برف متوسط یا شدید همراه رعد و برق",
    }

    lines = []
    lines.append("روزت شاد و عالی 🌈\n")

    city = location.get('name', 'نامشخص')

    lines.append(f"🌤 وضعیت آب و هوا در {city} \n")

    if temp := current.get('temp_c'):
        lines.append(f"🌡️ دمای فعلی: {temp} °C")

    if feelslike := current.get('feelslike_c'):
        if feelslike >= 30:
            icon = "🥵"
        elif feelslike <= 10:
            icon = "🥶"
        elif 15 <= feelslike <= 25:
            icon = "😍"
        else:
            icon = "🌡️"
        lines.append(f"{icon} دمای محسوس: {feelslike} °C")

    if condition := current.get('condition', {}).get('text'):
        condition_fa = condition_fa_map.get(condition, condition)
        lines.append(f"⛅ وضعیت: {condition_fa}")
    if wind := current.get('wind_kph'):
        lines.append(f"💨 سرعت باد: {wind} km/h")
    if humidity := current.get('humidity'):
        lines.append(f"💧 رطوبت: {humidity}%")
    if uv := current.get('uv'):
        lines.append(f"🌈 اشعه فرابنفش: {uv}")
    if pressure := current.get('pressure_mb'):
        lines.append(f"🌫️ فشار هوا: {pressure} mb")
    if vis := current.get('vis_km'):
        lines.append(f"👁️ دید افقی: {vis} km")
    if cloud := current.get('cloud'):
        lines.append(f"☁️ میزان ابر: {cloud}%")

    if aqi_index:
        lines.append(f"\n📊 شاخص کیفیت هوا")
        for idx in range(1, 7):
            check = "✅" if idx == aqi_index else "☐"
            lines.append(f"{check} {idx} — {aqi_text_map.get(idx)}")

    return "\n".join(lines)
