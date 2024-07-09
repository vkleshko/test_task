import requests
from tabulate import tabulate


class CountryInfo:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from API")

    def get_country_info(self):
        data = self.fetch_data()
        country_info = []
        for country in data:
            name = country.get("name", {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag_url = country.get("flags", {}).get("png", "N/A")
            country_info.append([name, capital, flag_url])
        return country_info

    def display_country_info(self):
        country_info = self.get_country_info()
        headers = ["Country Name", "Capital", "Flag URL"]
        print(tabulate(country_info, headers, tablefmt="grid"))


if __name__ == "__main__":
    ci = CountryInfo()
    ci.display_country_info()
