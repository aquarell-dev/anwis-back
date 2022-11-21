from datetime import datetime
from typing import List
import pytz

from common.services import fetch_leftovers
from .types import TLeftOver, TLeftOverSpecification
from .models import LeftOver


def _parse_leftover_specs(leftover: dict) -> List[TLeftOverSpecification]:
    leftover_specs = []

    for size in leftover['sizes']:
        total = 0

        for stock in size['stocks']:
            total += stock['qty']

        leftover_specs.append(TLeftOverSpecification(title=size['origName'], quantity=total))

    return leftover_specs


def get_leftover(nm: str) -> TLeftOver:
    response = fetch_leftovers([nm])

    leftover = response['data']['products'][0]

    leftover_specs = _parse_leftover_specs(leftover)

    return TLeftOver(
        title=leftover['name'],
        leftovers=leftover_specs
    )


def update_leftovers(nms: list = None, buffer_update: bool = True):
    """
    If update_buffer set to True then it would update only buffer leftovers,
    otherwise it would update the current leftovers.
    If you don't specify nms explicitly => it'd take all the nms of all leftovers.

    :param nms:
    :param buffer_update:
    :return:
    """
    if not nms:
        nms = [leftover.nm for leftover in LeftOver.objects.all()]

    if buffer_update:
        print('update buffer')

    response = fetch_leftovers(nms)

    products = response['data']['products']

    for leftover in LeftOver.objects.all():

        total = 0

        for product in products:
            if leftover.nm == str(product['id']):
                if buffer_update:
                    leftover.buffer.all().delete()
                elif not buffer_update:
                    leftover.products.all().delete()

                detailed = _parse_leftover_specs(product)

                for detail in detailed:
                    total += detail.quantity
                    if buffer_update:
                        leftover.buffer.create(title=detail.title, quantity=detail.quantity)
                    elif not buffer_update:
                        leftover.products.create(title=detail.title, quantity=detail.quantity)

        if buffer_update:
            leftover.buffer_total = total
        elif not buffer_update:
            leftover.total = total

        if buffer_update:
            leftover.last_update = datetime.now(tz=pytz.timezone("Europe/Moscow"))

        leftover.save()
