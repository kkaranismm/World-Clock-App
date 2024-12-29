import streamlit as st
from datetime import datetime, date
from geopy.geocoders import Nominatim
from pytz import timezone
import pytz
import requests
from timezonefinder import TimezoneFinder
from streamlit_folium import st_folium
import folium

# OpenWeatherMap API Key
API_KEY = "     "   # Enter Your API Key Here

# Streamlit Page Configuration
st.set_page_config(
    page_title="World Clock App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to Get Current Time
def get_country_time(lat, lon):
    try:
        geolocator = Nominatim(user_agent="world_clock_app")
        location = geolocator.reverse((lat, lon), language="en")
        address = location.raw.get("address", {})

        country = address.get("country", None)
        city = address.get("city", address.get("town", address.get("village", "Unknown")))
        country_code = address.get("country_code", None)

        if not country or not country_code:
            return "No country detected", "Unknown", "Invalid Location"

        country_code = country_code.upper()
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)

        if tz_name:
            tz = timezone(tz_name)
            local_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            return country, city, local_time
        return country, city, "Timezone unavailable"
    except Exception as e:
        return "Unknown", "Unknown", f"Error: {str(e)}"

# Function to Fetch Weather Data
def fetch_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "Temperature": f"{data['main']['temp']} °C",
                "Weather": data['weather'][0]['description'].capitalize(),
                "Humidity": f"{data['main']['humidity']}%",
                "Wind Speed": f"{data['wind']['speed']} m/s",
                "Sunrise": datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                "Sunset": datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            }
            return weather
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching weather: {str(e)}")
        return None

# Function to search location
def search_location(query):
    try:
        geolocator = Nominatim(user_agent="world_clock_app")
        location = geolocator.geocode(query)
        if location:
            return {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address
            }
        return None
    except Exception as e:
        st.error(f"Error searching location: {str(e)}")
        return None

# Title and Description
st.title("🌍 World Clock App")
st.write("Search for any location or click on the map to get local time and weather information.")

# Add search box
search_query = st.text_input("🔍 Search for a location", "")
if search_query:
    location_data = search_location(search_query)
    if location_data:
        st.session_state['current_location'] = {
            'latitude': location_data['latitude'],
            'longitude': location_data['longitude']
        }
    else:
        st.error("Location not found. Please try a different search term.")

# Sidebar: Time Conversion Tool
st.sidebar.header("🕒 Time Conversion Tool")

source_city = st.sidebar.text_input("Enter Source City (e.g., New York)")
target_city = st.sidebar.text_input("Enter Target City (e.g., Tokyo)")
input_time = st.sidebar.time_input("Select Time")
input_date = st.sidebar.date_input("Select Date")

# Initialize session state with default location (Chandigarh)
if 'current_location' not in st.session_state:
    st.session_state['current_location'] = {'latitude': 30.7333, 'longitude': 76.7794}  # Chandigarh coordinates

# Initialize Map
m = folium.Map(
    location=[st.session_state['current_location']['latitude'], 
              st.session_state['current_location']['longitude']], 
    zoom_start=4, 
    tiles="OpenStreetMap"
)

# Add marker for current location
folium.Marker(
    location=[st.session_state['current_location']['latitude'], 
              st.session_state['current_location']['longitude']],
    popup="Selected Location",
    icon=folium.Icon(color="green")
).add_to(m)

# Display the Map
output = st_folium(m, width=1200, height=500)

# Process Location (either clicked or current)
if output and output.get("last_clicked") is not None:
    lat, lon = output["last_clicked"]["lat"], output["last_clicked"]["lng"]
else:
    lat = st.session_state['current_location']['latitude']
    lon = st.session_state['current_location']['longitude']

# Get Country and Time
country, city, local_time = get_country_time(lat, lon)

# Display Results
if country == "No country detected":
    st.error("⚠️ The location is not a valid country.")
else:
    st.success(f"🌍 **Country**: {country}")
    st.info(f"🏠 **City**: {city}")
    st.info(f"🕐 **Local Time**: {local_time}")

    # Fetch and Display Weather
    weather = fetch_weather(lat, lon)
    if weather:
        st.info("☀️ **Weather Information:**")
        for key, value in weather.items():
            st.write(f"**{key}:** {value}")

    # Display Calendar
    st.info(f"📅 **Date for {city}, {country}:** {date.today()}")

# Time Conversion Logic
if "converted_time" not in st.session_state:
    st.session_state.converted_time = None
if "conversion_error" not in st.session_state:
    st.session_state.conversion_error = None

if st.sidebar.button("Convert Time"):
    try:
        st.session_state.conversion_error = None
        geolocator = Nominatim(user_agent="world_clock_app")
        tf = TimezoneFinder()

        source_location = geolocator.geocode(source_city)
        if not source_location:
            st.session_state.conversion_error = f"Could not find the source city: {source_city}"
            raise ValueError("Source city not found")

        target_location = geolocator.geocode(target_city)
        if not target_location:
            st.session_state.conversion_error = f"Could not find the target city: {target_city}"
            raise ValueError("Target city not found")

        source_tz_name = tf.timezone_at(lng=source_location.longitude, lat=source_location.latitude)
        target_tz_name = tf.timezone_at(lng=target_location.longitude, lat=target_location.latitude)

        if not source_tz_name or not target_tz_name:
            st.session_state.conversion_error = "Could not determine the timezone for one of the cities."
            raise ValueError("Timezone not found")

        source_tz = timezone(source_tz_name)
        target_tz = timezone(target_tz_name)
        dt = datetime.combine(input_date, input_time)
        source_time = source_tz.localize(dt)

        target_time = source_time.astimezone(target_tz)
        st.session_state.converted_time = f"Time in {target_city}: {target_time.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        st.session_state.conversion_error = f"Error: {str(e)}"

# Display the conversion result
if st.session_state.converted_time:
    st.sidebar.success(st.session_state.converted_time)

if st.session_state.conversion_error:
    st.sidebar.error(st.session_state.conversion_error)

# Footer
st.markdown("---")
st.markdown("**Developed by CO21332 & CO21330 using Streamlit and Folium**")