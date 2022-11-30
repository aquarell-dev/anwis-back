import requests
from django.core.files.storage import default_storage

_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}


def fetch_leftovers(nms: list):
    nm_string = ';'.join(nms)
    response = requests.get(
        f'https://card.wb.ru/cards/basket?spp=27&regions=80,68,64,83,4,38,33,70,82,69,86,30,40,48,1,22,66,'
        f'31&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,7,3,6,18,'
        f'21&sppFixGeo=4&dest=-1029256,-72181,-1144811,12358288&nm={nm_string}',
        headers=_headers
    )

    return response.json()


def save_to_default_storage(file):
    f = default_storage.save(file.name, file)

    return default_storage.url(f)


def check_required_keys(dictionary: dict, required_keys: list) -> list:
    missing_keys = []

    for key in required_keys:
        try:
            dictionary[key]
        except KeyError:
            missing_keys.append(key)

    return missing_keys