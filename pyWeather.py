import sys  # to access command line arguments
import requests # to make HTTP requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QComboBox
)
from PySide6.QtCore import Qt
# Pyside6 for GUI
import os # to access env vars
from dotenv import load_dotenv # to load env vars from .env file
import datetime # to work with timestamps

load_dotenv() # Load env vars from .env file

# Function to fetch weather data from the API
def get_weather(city, state, country_code, api_key):
    query = f"{city},{state},{country_code}" if state else f"{city},{country_code}"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    # code above is to get the data from the API with the city name, state/province, country, and the API key & convert it to json

    # if response successful, extract the data needed
    if response.status_code == 200:
        weather_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),  # Cap first letter of each word
            "wind_speed": data["wind"]["speed"],
            "sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S'),
            "sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S'),
            "city": data["name"],
            "country": data["sys"]["country"],
            "pressure": data["main"]["pressure"],
            "cloudiness": data["clouds"]["all"]
        }
        return weather_data, None
    else:
        error_message = data.get("message", "Unknown error")
        return None, error_message # if successful, return the data, else return the error message

# Function to fetch hourly weather data from the API
def get_hourly_weather(city, state, country_code, api_key):
    query = f"{city},{state},{country_code}" if state else f"{city},{country_code}"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={query}&units=imperial&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        hourly_weather = []
        for entry in data["list"]:
            timestamp = datetime.datetime.fromtimestamp(entry["dt"]).strftime('%Y-%m-%d %H:%M:%S')
            temperature = entry["main"]["temp"]
            description = entry["weather"][0]["description"].title()
            hourly_weather.append({"timestamp": timestamp, "temperature": temperature, "description": description})
        return hourly_weather, None
    else:
        error_message = data.get("message", "Unknown error")
        return None, error_message
    # if successful, return the hourly weather extracted data, else return the error message

# Main Weather App GUI using the Constructor of the QWidget class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.display_units = "imperial"  # Default Imperial
        self.hourly_weather = []
        self.current_page = 0

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 800, 400)
        # set window title, position and size

        layout = QVBoxLayout() # create a vertical layout

        # City input
        city_layout = QHBoxLayout()
        city_label = QLabel("Enter City Name:")
        self.city_edit = QLineEdit()
        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_edit)

        # State/Province input
        state_layout = QHBoxLayout()
        state_label = QLabel("Enter State/Province (Optional):")
        self.state_edit = QLineEdit()
        state_layout.addWidget(state_label)
        state_layout.addWidget(self.state_edit)

        # Country input
        country_layout = QHBoxLayout()
        country_label = QLabel("Select Country:")
        self.country_combobox = QComboBox()
        self.populate_country_combobox()
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_combobox)

        # Weather display
        self.weather_display = QTextEdit()
        self.weather_display.setReadOnly(True)

        # Buttons & Layout
        button_layout = QHBoxLayout()
        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.get_weather_clicked)
        self.hourly_weather_button = QPushButton("Show Hourly Weather")
        self.hourly_weather_button.clicked.connect(self.show_hourly_weather)
        button_layout.addWidget(self.get_weather_button)
        button_layout.addWidget(self.hourly_weather_button)

        # Previous & Next buttons (initially hidden)
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_hours)
        self.prev_button.hide()
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_hours)
        self.next_button.hide()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Unit button
        self.unit_button = QPushButton("Switch Units")
        self.unit_button.clicked.connect(self.switch_units)
        button_layout.addWidget(self.unit_button)

        # Add layouts to main layout
        layout.addLayout(city_layout)
        layout.addLayout(state_layout)
        layout.addLayout(country_layout)
        layout.addWidget(self.weather_display)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # Function to populate the country dropdown list
    def populate_country_combobox(self):
        country_url = "https://restcountries.com/v2/all" # URL to fetch all countries
        response = requests.get(country_url)
        if response.status_code == 200:
            countries = response.json()
            for country in countries:
                self.country_combobox.addItem(country["name"])
        else:
            QMessageBox.warning(self, "Error", "Failed to fetch country data. Please try again later.")

    # Function to switch between imperial & metric units
    def switch_units(self):
        if self.display_units == "imperial":
            self.display_units = "metric"
            self.unit_button.setText("Switch to Imperial")
        else:
            self.display_units = "imperial"
            self.unit_button.setText("Switch to Metric")

        # Fetch data again to update the display
        self.get_weather_clicked()

    def get_weather_clicked(self):
        city = self.city_edit.text().strip()
        state = self.state_edit.text().strip()
        country = self.country_combobox.currentText().strip()

        if not city:
            QMessageBox.warning(self, "Warning", "Please enter a city name.")
            return

        api_key = os.getenv("API_KEY")
        if not api_key:
            QMessageBox.warning(self, "Error", "API key was not found. Ensure API_KEY is in .env file")
            return

        weather, error_message = get_weather(city, state, country, api_key)

        if weather:
            self.display_weather(weather)
        else:
            QMessageBox.warning(self, "Error", f"Failed to fetch weather data. Error: {error_message}")

    # Function to handle the Show Hourly Weather button & display the hourly weather
    def show_hourly_weather(self):
        city = self.city_edit.text().strip()
        state = self.state_edit.text().strip()
        country = self.country_combobox.currentText().strip()

        if not city:
            QMessageBox.warning(self, "Warning", "Please enter a city name.")
            return

        api_key = os.getenv("API_KEY")
        if not api_key:
            QMessageBox.warning(self, "Error", "API key was not found. Ensure API_KEY is in .env file")
            return

        self.hourly_weather, error_message = get_hourly_weather(city, state, country, api_key)

        if self.hourly_weather:
            self.current_page = 0
            self.display_hourly_weather()
            self.prev_button.show()  # Show the Previous button
            self.next_button.show()  # Show the Next button
        else:
            QMessageBox.warning(self, "Error", f"Failed to fetch hourly weather data. Error: {error_message}")

    def show_previous_hours(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_hourly_weather()

    def show_next_hours(self):
        if self.current_page < len(self.hourly_weather) // 5:
            self.current_page += 1
            self.display_hourly_weather()

    # Function to display hourly weather data
    def display_weather(self, weather):
        if self.display_units == "imperial":
            temperature_unit = "°F"
            wind_speed_unit = "mph"
            visibility_unit = "miles"
            pressure_unit = "hPa"
        else:
            temperature_unit = "°C"
            wind_speed_unit = "m/s"
            visibility_unit = "meters"
            pressure_unit = "hPa"

        temperature = weather['temperature']
        if self.display_units == "metric":
            temperature = (temperature - 32) * 5/9

        message = f"Weather in {weather['city']}, {weather['country']}:\n"
        message += f"Temperature: {temperature:.2f} {temperature_unit}\n"
        message += f"Humidity: {weather['humidity']}%\n"
        message += f"Description: {weather['description']}\n"
        message += f"Wind Speed: {weather['wind_speed']} {wind_speed_unit}\n"
        message += f"Pressure: {weather['pressure']} {pressure_unit}\n"
        message += f"Cloudiness: {weather['cloudiness']}%\n"
        message += f"Sunrise: {weather['sunrise']}\n"
        message += f"Sunset: {weather['sunset']}"
        self.weather_display.setText(message)

    def display_hourly_weather(self):
        message = "Hourly Weather for the Next 12 Hours:\n"
        start_index = self.current_page * 5
        end_index = min(start_index + 5, len(self.hourly_weather))

        for i, entry in enumerate(self.hourly_weather[start_index:end_index], start=1):
            message += f"Timestamp: {entry['timestamp']}, Temperature: {entry['temperature']}°F, Description: {entry['description']}\n"

        self.weather_display.setText(message)

# Main function to initialize app
def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())

# Entry point of the app. This is common in Python scripts to run the main function
if __name__ == "__main__":
    main()
