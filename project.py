import streamlit as st
import requests

# CONFIGURATION 
OPENWEATHER_API_KEY = "6bd986a6faf666be6ee62bc31842f609"  # OpenWeatherMap API key

# DATA SETUP 
city_data = {
    "San Francisco, CA": {
        "coords": (37.7749, -122.4194),
        "dishes": [
            ("Sourdough Bread", "Boudin Bakery"),
            ("Cioppino", "Sotto Mare"),
            ("Mission Burrito", "La Taqueria")
        ]
    },
    "Los Angeles, CA": {
        "coords": (34.0522, -118.2437),
        "dishes": [
            ("Korean BBQ", "Kang Ho Dong Baekjeong"),
            ("In-N-Out Burger", "In-N-Out"),
            ("Avocado Toast", "Sqirl")
        ]
    },
    "New York City, NY": {
        "coords": (40.7128, -74.0060),
        "dishes": [
            ("New York-Style Pizza", "Joe's Pizza"),
            ("Bagels with Lox", "Russ & Daughters"),
            ("Cheesecake", "Junior's")
        ]
    },
    "Austin, TX": {
        "coords": (30.2672, -97.7431),
        "dishes": [
            ("Barbecue Brisket", "Franklin Barbecue"),
            ("Breakfast Tacos", "Veracruz All Natural"),
            ("Kolaches", "Brewster's Bakery")
        ]
    },
    "Chicago, IL": {
        "coords": (41.8781, -87.6298),
        "dishes": [
            ("Deep Dish Pizza", "Lou Malnati's"),
            ("Italian Beef Sandwich", "Al's Beef"),
            ("Chicago-Style Hot Dog", "Portillo's")
        ]
    }
}

# FUNCTIONS

def get_weather_openweathermap(lat, lon, api_key):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"],
            "weather_code": data["weather"][0]["id"]
        }
        return weather
    except Exception as e:
        st.error(f"Weather API error: {e}")
        return None

def suggest_dining(weather):
    temp = weather.get("temperature", 25)
    wind = weather.get("wind_speed", 0)
    code = weather.get("weather_code", 800)
    # Rain codes: 500-531, Thunderstorm: 200-232, Snow: 600-622
    if 200 <= code <= 622 or temp < 10 or temp > 35 or wind > 10:
        return "Indoor"
    return "Outdoor"

def foodie_narrative(city, dining, dishes):
    meals = ["Breakfast", "Lunch", "Dinner"]
    narrative = f"### {city} Foodie Tour Suggestion ({dining} Dining)\n"
    for meal, (dish, place) in zip(meals, dishes):
        if dining == "Outdoor":
            narrative += f"- **{meal}:** Enjoy **{dish}** at **{place}**, perfect for a lovely outdoor experience.\n"
        else:
            narrative += f"- **{meal}:** Savor **{dish}** at **{place}**, great for a cozy indoor meal.\n"
    return narrative

#STREAMLIT UI

st.title("USA Foodie Tour Planner with Live Weather")

city_names = list(city_data.keys())
selected_city = st.selectbox("Choose a city for your foodie adventure:", city_names)

if st.button("Plan My Foodie Tour"):
    city_info = city_data[selected_city]
    lat, lon = city_info["coords"]
    dishes = city_info["dishes"]

    weather = get_weather_openweathermap(lat, lon, OPENWEATHER_API_KEY)
    st.subheader(f"City: {selected_city}")
    if weather:
        st.write(f"**Weather:** {weather['temperature']}°C, {weather['description']}, Wind {weather['wind_speed']} m/s")
        dining_suggestion = suggest_dining(weather)
        st.write(f"**Dining Suggestion:** {dining_suggestion} dining")
        st.write("**Iconic Dishes & Top Restaurants:**")
        for dish, place in dishes:
            st.write(f"- {dish} at {place}")
        st.markdown(foodie_narrative(selected_city, dining_suggestion, dishes))
    else:
        st.error("Weather data unavailable for this city.")
