# World Clock App 🌍

A real-time world clock application built with Streamlit that allows users to:
- View local time and weather information for any location worldwide
- Convert time between different cities
- Interactive map interface for location selection
- Get detailed weather information including temperature, humidity, and wind speed

## Features

- 🗺️ Interactive World Map
- 🔍 Location Search functionality
- ⏰ Real-time clock display
- 🌡️ Weather information display
- 🕒 Time zone conversion tool
- 📅 Calendar integration
- 🌍 Geolocation services

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kkaranismm/world-clock-app.git
cd world-clock-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Required Dependencies

Create a `requirements.txt` file with the following content:
```
streamlit
datetime
geopy
pytz
requests
timezonefinder
streamlit-folium
folium
```

## Configuration

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace the API_KEY variable in the code with your key:
```python
API_KEY = "your_api_key_here"
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run world_clock_app_new.py
```

2. The application will open in your default web browser

## Features Guide

### Main Map Interface
- Click anywhere on the map to get local time and weather information
- Use the search box to find specific locations

### Time Conversion Tool
- Enter source and target cities
- Select time and date
- Click "Convert Time" to see the converted time

### Weather Information
- Temperature in Celsius
- Weather description
- Humidity percentage
- Wind speed
- Sunrise and sunset times

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Mapping functionality powered by [Folium](https://python-visualization.github.io/folium/)
- Developed by Karandeep Singh
