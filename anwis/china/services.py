import io
from urllib.request import urlopen

import requests
import xlsxwriter
import string

from PIL import Image
from django.conf import settings
import os

from django.core.files import File
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from china.models import Order

uppercase = string.ascii_uppercase


class ChinaService:
    def form_excel(self, id: int, request: Request):
        name = f'order{id}.xlsx'

        path = os.path.join(settings.BASE_DIR, 'media', 'documents', name)

        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()

        titles = ['图片', '数量', '尺码', '单价/件', '金额']

        centered_and_border = {
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        }

        merge_title_format = workbook.add_format({
            **centered_and_border,
            'fg_color': 'white',
            'font_size': 26
        })

        bg_purple_format = workbook.add_format({
            **centered_and_border,
            'fg_color': 'purple',
            'color': 'white',
            'font_size': 10
        })
        delivery_n_total_format = workbook.add_format({
            **centered_and_border,
            'font_size': 20,
            'color': 'red'
        })

        worksheet.merge_range('A1:E1', '报价', merge_title_format)

        worksheet.set_column('A:A', 80)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:E', 32)

        worksheet.set_row(1, 40)

        for idx, title in enumerate(titles):
            worksheet.write(f'{uppercase[idx]}2', title, bg_purple_format)

        order = get_object_or_404(Order.objects.all(), id=id)

        articles = [product.product.article for product in order.products.all()]

        products = [order.products.filter(product__article=article) for article in list(set(articles))]

        last = len(order.products.all()) + 2

        worksheet.write(f'A{last+1}', 'за доставку', delivery_n_total_format)
        worksheet.write(f'A{last+2}', 'TOTAL', delivery_n_total_format)
        worksheet.write(f'B{last+2}', str(order.total_quantity), delivery_n_total_format)

        for i in range(2, last+2):
            worksheet.set_row(i, 75)

        index = 0

        for product_array in products:
            if product_array[0].product.photo:
                url = request.build_absolute_uri(product_array[0].product.photo.url)
                image_data = io.BytesIO(urlopen(url).read())

                response = requests.get(url)
                img = Image.open(io.BytesIO(response.content))
                w, h = img.size

                cell_width = 565
                cell_height = 100

                x_scale = cell_width / len(product_array) / w
                y_scale = cell_height * len(product_array) / h

                worksheet.insert_image(
                    f'A{index + 3}',
                    url,
                    {'image_data': image_data, 'x_scale': 0.7, 'y_scale': 0.7}
                )

            start = index + 3

            for product in product_array:
                index += 1
                worksheet.write(
                    f'B{index + 2}',
                    str(product.quantity),
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )
                worksheet.write(
                    f'C{index + 2}',
                    str(product.product.size),
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )

            worksheet.merge_range(f'A{start}:A{index+2}', '', merge_title_format)

        workbook.close()

        with open(path, 'rb') as f:
            order.excel = File(f, name=os.path.basename(f.name))
            order.save()

        return request.build_absolute_uri(f'media/documents/order{id}.xlsx/')
