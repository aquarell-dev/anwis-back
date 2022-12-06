import os
from datetime import datetime
from typing import List, Type, Union

import requests
from blabel import LabelWriter
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response

from acceptance.models import Acceptance, Product, ProductSpecification, AcceptanceCategory, Box, Reason
from acceptance.serializers import ProductSpecificationDetailedSerializer
from china.models import Order, ProductInfo
from common.services import fetch_leftovers
from documents.models import Document, Photo


def _does_entity_exist(model: Type[models.Model], **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def _does_russian_product_exist(**kwargs):
    return _does_entity_exist(Product, **kwargs)


def _does_acceptance_exist(**kwargs):
    return _does_entity_exist(Acceptance, **kwargs)


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
                acceptance.specifications.add(
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
                already_existing_objs = [spec.id for spec in acceptance.specifications.all()]
                acceptance.specifications.add(*already_existing_objs, new_specification.id)

            continue

        product, selfcost, quantity = _create_new_product(specification, order)

        acceptance.specifications.create(
            cost=selfcost,
            quantity=quantity,
            product=product
        )

    acceptance.save()


def create_acceptance_from_order(order: Order):
    four_digit_id = '0' * (4 - len(str(order.id))) + str(order.id)

    acceptance = Acceptance.objects.create(
        title=f'Приемка №{four_digit_id}',
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


def _is_article_russian(article: str):
    try:
        int(article)
    except ValueError:
        return False

    return True


def _get_products():
    product_ids = [product.article for product in Product.objects.all()]

    valid_wb_ids = []

    for product_id in product_ids:
        if _is_article_russian(product_id):
            valid_wb_ids.append(int(product_id))

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
    from acceptance.serializers import ProductCreateSerializer

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


def update_photos_from_wb(articles: list = None):
    if not articles:
        articles = [product.article for product in Product.objects.all() if _is_article_russian(str(product.article))]
    else:
        articles = [article for article in articles if _is_article_russian(str(article))]

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

        products_to_be_updated = Product.objects.filter(article=article)

        for product in products_to_be_updated:
            try:
                if product.photo:
                    product.photo.delete()
            except Photo.DoesNotExist:
                continue

        products_to_be_updated.update(photo=photo)


def _all_acceptances_w_this_box_finished(box_number: str):
    # Есть ли приемки, в которых есть эта коробка, при том, что это приемка еще не завершена
    return len(Box.objects.filter(
            box=box_number,
            archive=False
        )) < 1


def _box_in_this_specification_and_is_not_to_be_changed(specification: ProductSpecification, box: str, quantity: int):
    """
    Если коробка существует и она не собирается меняться, то мы просто пропускаем итерацию в цикле,
    чтоб не вылетала ошибка, что такая коробка с активной приемкой уже существует.
    :param specification:
    :param box:
    :param quantity:
    :return:
    """
    # Box.objects.filter()
    _box: Union[Box, None] = _does_entity_exist(Box, specification_id=specification.id, box=box)

    if not _box:
        return False

    print(box, _box.quantity, quantity, _box.quantity == quantity)

    return _box.quantity != quantity


def _patch_boxes(boxes: list, specification: ProductSpecification):
    for box in boxes:
        box_id = box.pop('id', None)
        box_number = str(box.pop('box', None))
        quantity = int(box.pop('quantity', None))

        acceptances_finished = _all_acceptances_w_this_box_finished(box_number)

        if not _box_in_this_specification_and_is_not_to_be_changed(specification, box_number, quantity):
            if not acceptances_finished:
                raise serializers.ValidationError(
                    {'status': 'error', 'message': f'Есть активная приемка с этой коробкой{box_number, box_id}'}
                )

        _box = _does_entity_exist(Box, id=int(box_id))

        if not _box:
            continue

        _box.box = box_number
        _box.quantity = quantity

        _box.save()


def _patch_reasons(reasons: list):
    if not isinstance(reasons, list):
        return

    for reason in reasons:
        reason_id = reason.pop('id', None)

        if reason_id:
            continue

        Reason.objects.filter(id=int(reason_id)).update(**reason)


def update_specification(instance: ProductSpecification, data: dict):
    boxes = data.pop('boxes', None)
    reasons = data.pop('reasons', None)

    if boxes:
        _patch_boxes(boxes, instance)

    if reasons:
        _patch_reasons(reasons)

    ProductSpecification.objects.filter(id=instance.id).update(**data)

    return instance


def update_multiple_specifications(request: Request):
    specifications = request.data.pop('specifications', None)

    if not specifications:
        return Response({'error': 'provide specs'}, status=400)

    response = []

    for specification in specifications:
        id = specification.pop('id', None)

        if not id:
            continue

        try:
            specification_instance = ProductSpecification.objects.get(id=int(id))
        except ProductSpecification.DoesNotExist:
            continue

        update_specification(specification_instance, specification)

        response.append({'id': specification_instance.id, 'status': 'updated'})

    return response


def _get_specification(context, **kwargs):
    instance = get_object_or_404(
        ProductSpecification.objects.all(),
        acceptance__status__status__in=['Новая Приемка', 'Упаковано', 'Упаковывается'],
        **kwargs
    )

    return Response(
        ProductSpecificationDetailedSerializer(instance=instance, context=context).data
    )


def get_specification_by_box(context, box_number: str):
    return _get_specification(
        context,
        boxes__box__iexact=str(box_number)
    )


def get_specification_by_barcode(context, barcode: str):
    return _get_specification(context, product__barcode__iexact=str(barcode))
