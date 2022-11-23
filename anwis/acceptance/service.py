import os
from datetime import datetime
from typing import List
from django.core.files.temp import NamedTemporaryFile

import requests

from acceptance.models import Acceptance, Product, ProductSpecification, AcceptanceCategory
from acceptance.serializers import ProductCreateSerializer
from china.models import Order, ProductInfo

from blabel import LabelWriter

from common.services import fetch_leftovers, save_to_default_storage

from django.core.files import File

from documents.models import Document, Photo


def _does_russian_product_exist(**kwargs):
    try:
        return Product.objects.get(**kwargs)
    except Product.DoesNotExist:
        return None


def _does_acceptance_exist(**kwargs):
    try:
        return Acceptance.objects.get(**kwargs)
    except Product.DoesNotExist:
        return None


def _calculate_self_cost(info: ProductInfo, order: Order):
    delivery = ((order.dollar_to_rub * order.real_total_delivery) + order.delivery_expenses) / order.total_quantity
    cost_wout_delivery = info.price_rub + info.additional_expenses  # = 111
    selfcost = delivery + float(cost_wout_delivery)
    return round(selfcost)


def _get_specification_by_product_id(product: Product):
    try:
        return ProductSpecification.objects.get(product_id=product.id)
    except Product.DoesNotExist:
        return None


def _create_new_product(info: ProductInfo, order: Order) -> tuple:
    selfcost = _calculate_self_cost(info, order)

    russian_product = Product.objects.create(
        photo=info.product.photo,
        linked_china_product_size=info.product.size,
        linked_china_product_article=info.product.article,
        article=info.product.article,
        size=info.product.size,
        color=info.product.color,
        brand=info.product.brand,
        last_cost=selfcost,
        title=info.product.title,
        category=AcceptanceCategory.objects.get_or_create(category=info.product.category.category)[0]
    )

    return russian_product, selfcost, info.quantity


def _patch_or_add_missing_products(order: Order, acceptance: Acceptance):
    for specification in order.products.all():
        product = _does_russian_product_exist(
            linked_china_product_article=specification.product.article,
            linked_china_product_size=specification.product.size,
        )

        if product:
            product.last_cost = _calculate_self_cost(specification, order)
            category = specification.product.category
            if category:
                product.category = AcceptanceCategory.objects.get_or_create(category=category.category)[0]
            product.save()

            new_specification = _get_specification_by_product_id(product)

            selfcost = _calculate_self_cost(specification, order)

            if not new_specification:
                acceptance.products.add(
                    ProductSpecification.objects.create(
                        product=product,
                        cost=selfcost,
                        quantity=specification.quantity
                    )
                )
            else:
                new_specification.quantity = specification.quantity
                new_specification.cost = selfcost
                new_specification.save()
                already_existing_objs = [spec.id for spec in acceptance.products.all()]
                acceptance.products.add(*already_existing_objs, new_specification.id)

            continue

        product, selfcost, quantity = _create_new_product(specification, order)

        acceptance.products.create(
            cost=selfcost,
            quantity=quantity,
            product=product
        )

    acceptance.save()


def create_acceptance_from_order(order: Order):
    four_digit_id = '0' * (4 - len(str(order.id))) + str(order.id)

    acceptance = Acceptance.objects.create(
        title=f'Приемка {four_digit_id}',
        cargo_number=order.cargo_number,
        cargo_volume=order.cargo_volume,
        cargo_weight=order.cargo_weight,
        arrived_in_moscow=order.real_in_moscow_date,
        shipped_from_china=order.shipping_from_china_date,
        from_order=order.id
    )

    _patch_or_add_missing_products(order, acceptance)

    return acceptance


def update_acceptance_from_order(acceptance: Acceptance, order: Order):
    acceptance.cargo_number = order.cargo_number
    acceptance.cargo_volume = order.cargo_volume
    acceptance.cargo_weight = order.cargo_weight
    acceptance.arrived_in_moscow = order.real_in_moscow_date
    acceptance.shipped_from_china = order.shipping_from_china_date

    _patch_or_add_missing_products(order, acceptance)

    return acceptance


def create_label(data: dict):
    adult_category = str(data.pop('category')).lower() == 'товары для взрослых'

    default_label_path = os.path.join(os.getcwd(), 'acceptance', 'labels', 'label_template.html')
    default_styles = (os.path.join(os.getcwd(), 'acceptance', 'labels', 'style.css'),)

    adult_label_path = os.path.join(os.getcwd(), 'acceptance', 'labels', 'adult_label_template.html')
    adult_styles = (os.path.join(os.getcwd(), 'acceptance', 'labels', 'adult_styles.css'),)

    label_writer = LabelWriter(
        default_label_path if not adult_category else adult_label_path,
        default_stylesheets=default_styles if not adult_category else adult_styles,
        encoding='utf-8'
    )

    quantity = data.pop('quantity')

    size = data.pop('size')

    records = [
        dict(
            **data,
            current_date=datetime.now().strftime('YY/MM/DD'),
            size=size if str(size) != '0' else '-'
        )
        for _ in range(int(quantity))
    ]

    temp = os.path.join(os.getcwd(), 'media', 'documents', 'temp')

    file_path = os.path.join(temp, 'labels.pdf')

    label_writer.write_labels(
        records,
        target=file_path,
    )

    with open(file_path, 'rb') as f:
        document = Document.objects.create(
            title='pdf',
            document=File(f, name=os.path.basename(f.name))
        )

    return document.document.url


def _get_total_quantity(sizes: dict, product_size: str) -> int:
    total = 0

    for size in sizes:
        if size['origName'] == product_size:
            for stock in size['stocks']:
                total += stock['qty']

    return total


def _get_products():
    product_ids = [product.article for product in Product.objects.all()]

    valid_wb_ids = []

    for product_id in product_ids:
        try:
            valid_wb_ids.append(int(product_id))
        except ValueError:
            pass

    valid_wb_ids = list(map(str, valid_wb_ids))

    return fetch_leftovers(valid_wb_ids)['data']['products']


def update_leftovers():
    products = _get_products()

    for product in products:
        russian_products = Product.objects.filter(article=product['id'])

        for p in russian_products:
            p.total_left = _get_total_quantity(product['sizes'], p.size)
            p.save()


def update_colors():
    products = _get_products()

    for product in products:
        russian_products = Product.objects.filter(article=product['id'])

        for p in russian_products:
            p.color = ', '.join([color['name'] for color in product['colors']])
            p.save()


def update_multiple_categories(data: dict):
    products = data.get('products', None)
    category = data.get('category', None)

    if not products:
        return 0

    Product.objects.filter(id__in=list(map(int, products))).update(category_id=int(category))

    return 1


def create_multiple_products(products: List[dict]):
    for product in products:
        serializer = ProductCreateSerializer(data=product)

        if serializer.is_valid():
            serializer.save()


baskets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def _get_photo_probable_urls(article: str):
    if len(article) == 9:
        return [
            f'https://basket-{"0" + str(basket) if len(str(basket)) == 1 else basket}.wb.ru/vol{article[:4:]}/part{article[:6:]}/{article}/images/c516x688/1.jpg'
            for basket in baskets
        ]
    elif len(article) == 8:
        return [
            f'https://basket-{"0" + str(basket) if len(str(basket)) == 1 else basket}.wb.ru/vol{article[:3:]}/part{article[:5:]}/{article}/images/c516x688/1.jpg'
            for basket in baskets
        ]


def _get_photo_response(urls: list) -> requests.Response:
    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            return response


def update_photos_from_wb(articles: list):
    articles = list(set(list(map(str, articles))))

    urls = [
        (_get_photo_response(_get_photo_probable_urls(article)), article)
        for article in articles
    ]

    for response, article in urls:
        img_temp = NamedTemporaryFile()
        img_temp.write(response.content)
        img_temp.flush()

        title = f'Auto Fetched for {article}'

        photo = Photo.objects.create(
            title=title,
        )

        photo.photo.save(os.path.basename(img_temp.name), File(img_temp), save=True)

        Product.objects.filter(article=article).update(photo=photo)
