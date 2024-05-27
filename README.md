# pyWeather

pyWeather is a Python application designed to keep you informed about the latest weather conditions. Leveraging the OpenWeatherMap API, pyWeather fetches real-time weather data for any city worldwide and presents it in a user-friendly interface.

### Key Features

Real-time Weather Updates
Stay up-to-date with the current weather conditions for your chosen city. pyWeather fetches and displays crucial information such as temperature, humidity, wind speed, pressure, cloudiness, sunrise, and sunset.

### Hourly Weather Forecast

Plan your day effectively with the hourly weather forecast feature. Get detailed insights into the weather trends for the next 12 hours.

### Intuitive User Interface

Enjoy a seamless user experience with pyWeather's intuitive graphical interface built using PySide6. With input fields for city selection and interactive buttons for weather retrieval and unit switching, pyWeather caters to users of all skill levels.

### Unit Flexibility

Customize your weather experience by toggling between imperial and metric units. Whether you prefer Fahrenheit or Celsius, miles or kilometers, pyWeather adapts to your preferences effortlessly.

## Pre-requisites

1. Ensure you have Python 3 installed on your system
   (https://www.python.org/downloads/)

2. OpenWeatherMap API key
   (https://home.openweathermap.org/users/sign_up)

## Installation

1. Clone the repository and cd into the project directory

2. Install the required dependencies using the command
   'pip3 install PySide6 requests python-dotenv'

3. Ensure your API_KEY is stored in a .env file in the root directory of the project
   API_KEY=your_api_key_here

4. Run the script from the terminal using the command
   'python3 pyWeather.py'

## Usage

Once the script is running, follow the promptsfor which you want to fetch weather information. The script will then make a request to the OpenWeatherMap API and display the current weather conditions for the specified city.
