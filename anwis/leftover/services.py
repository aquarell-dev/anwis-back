from typing import List

import requests

from .types import TLeftOver, TLeftOverSpecification
from .models import LeftOver

_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}


class LeftOverService:
    def _fetch_leftovers(self, nms: list):
        nm_string = ';'.join(nms)
        response = requests.get(
            f'https://card.wb.ru/cards/basket?spp=27&regions=80,68,64,83,4,38,33,70,82,69,86,30,40,48,1,22,66,'
            f'31&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,7,3,6,18,'
            f'21&sppFixGeo=4&dest=-1029256,-72181,-1144811,12358288&nm={nm_string}',
            headers=_headers
        )

        return response.json()

    def _parse_leftover_specs(self, leftover: dict) -> List[TLeftOverSpecification]:
        leftover_specs = []

        for size in leftover['sizes']:
            total = 0

            for stock in size['stocks']:
                total += stock['qty']

            leftover_specs.append(TLeftOverSpecification(title=size['origName'], quantity=total))

        return leftover_specs

    def get_leftover(self, nm: str) -> TLeftOver:
        response = self._fetch_leftovers([nm])

        leftover = response['data']['products'][0]

        leftover_specs = self._parse_leftover_specs(leftover)

        return TLeftOver(
            title=leftover['name'],
            leftovers=leftover_specs
        )

    def update_leftovers(self, nms: list):
        response = self._fetch_leftovers(nms)

        products = response['data']['products']

        for leftover in LeftOver.objects.all():
            for product in products:
                if leftover.nm == str(product['id']):
                    leftover.products.all().delete()

                    detailed = self._parse_leftover_specs(product)

                    for detail in detailed:
                        leftover.products.create(title=detail.title, quantity=detail.quantity)
