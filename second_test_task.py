import requests
from bs4 import BeautifulSoup
import json


class EbayScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Failed to fetch page from Ebay")

    @staticmethod
    def extract_images(soup: BeautifulSoup):
        button_tags = soup.find_all("button", {"class": "ux-image-grid-item"})
        image_urls = []
        for btn in button_tags:
            img_tag = btn.find("img")

            if img_tag and "src" in img_tag.attrs:
                image_urls.append(img_tag["src"])

            if img_tag and "data-src" in img_tag.attrs:
                image_urls.append(img_tag["data-src"])

        return image_urls

    def parse_data(self, html):
        soup = BeautifulSoup(html, "html.parser")

        name_elem = soup.select_one(".x-item-title__mainTitle")
        name = (
            name_elem.find(
                "span", {"class": "ux-textspans ux-textspans--BOLD"}
            ).text.strip()
            if name_elem
            else ""
        )

        image_urls = self.extract_images(soup)

        price_elem = soup.select_one(".x-price-primary .ux-textspans")
        price = price_elem.text.strip() if price_elem else ""

        seller_elem = soup.select_one(".x-sellercard-atf__info__about-seller")
        seller = seller_elem["title"] if seller_elem else ""

        shipping_price_elem = soup.select_one(".ux-labels-values__values-content")
        shipping_price = shipping_price_elem.text.strip() if shipping_price_elem else ""

        data = {
            "name": name,
            "image_urls": image_urls,
            "product_url": self.url,
            "price": price,
            "seller": seller,
            "shipping_price": shipping_price,
        }

        return data

    def save_to_json(self, data, filename="product_data.json"):
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def display_data(self):
        html = self.fetch_page()
        data = self.parse_data(html)
        print(json.dumps(data, indent=4))
        self.save_to_json(data)


if __name__ == "__main__":
    url = "https://www.ebay.com/itm/156290961370?epid=21057814646&itmmeta=01J2BGDH4VESYF9RHSMF2SNNDG&hash=item2463aacfda:g:R2QAAOSwz15mewVJ&amdata=enc%3AAQAJAAAA8C6cqfdggF2ZX7hZJ3%2FTmkjJpfIqTT0mJ0GDfd1h7yfUbNhuoRlulNk9aE7o9Ei%2BAsw8dTjKNJ5PoLd4yKHsBZGpda5H2%2BMXMdyU4iZ43XWxUY66J5%2FeO%2FhJK8EAU3CdHZH6ghrZPVtCvJL%2B%2B5j5oQjHVk6WU7kmgulVCER1lVHcxNCy9x%2BmkNueVSLyjKmzFN2mAOAJmOR%2BdxffjO1vp2PHz5ltMHrgZVCCCrlaAw5KYFls9P0dgVMayq1sOP8SK7J5%2BCiqlPDNlYBPTDz8C3eOWhcQCnDvq0qfW2YePSd8FcnyC6GsS149d%2B7uU0KfJA%3D%3D%7Ctkp%3ABFBMwJK28JJk"  # замініть YOUR_PRODUCT_ID на реальний ID продукту
    scraper = EbayScraper(url)
    scraper.display_data()
