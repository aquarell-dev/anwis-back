from acceptance.models import Acceptance, Product, ProductSpecification
from china.models import Order, ProductInfo


def does_product_exist(**kwargs):
    try:
        return Product.objects.get(**kwargs)
    except Product.DoesNotExist:
        return None


def _calculate_self_cost(info: ProductInfo, order: Order):
    delivery = order.dollar_to_rub * (order.real_total_delivery + order.dollar_to_rub)
    cost_wout_delivery = info.price_rub + info.additional_expenses
    selfcost = delivery + float(cost_wout_delivery)
    return selfcost


def _get_or_create_specification_by_product_id(product: Product, cost, quantity):
    try:
        return ProductSpecification.objects.get(product_id=product.id)
    except Product.DoesNotExist:
        return ProductSpecification.objects.create(
            product=product,
            cost=cost,
            quantity=quantity
        )


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
        title=info.product.title
    )

    return russian_product, selfcost, info.quantity


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

    unique_data = [(product_specification, product_specification.product.article, product_specification.product.size)
                   for product_specification in order.products.all()]

    for specification, article, size in unique_data:
        product = does_product_exist(linked_china_product_article=article, linked_china_product_size=size)
        if product:
            product.last_cost = _calculate_self_cost(specification, order)
            product.save()

            acceptance.products.add(
                _get_or_create_specification_by_product_id(
                    product,
                    _calculate_self_cost(specification, order),
                    specification.quantity
                )
            )

            continue

        product, selfcost, quantity = _create_new_product(specification, order)
        acceptance.products.create(
            cost=selfcost,
            quantity=quantity,
            product=product
        )

    acceptance.save()

    return acceptance


def update_acceptance_from_order(acceptance: Acceptance, order: Order):
    acceptance.cargo_number = order.cargo_number
    acceptance.cargo_volume = order.cargo_volume
    acceptance.cargo_weight = order.cargo_weight
    acceptance.arrived_in_moscow = order.real_in_moscow_date
    acceptance.shipped_from_china = order.shipping_from_china_date

    return acceptance
