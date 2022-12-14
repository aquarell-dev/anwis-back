import io
import math
from typing import List, Tuple
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

from china.models import Project, Product, ProductInfo

uppercase = string.ascii_uppercase


class ChinaService:
    def __init__(self):
        self._last_cell = 0
        self._current_quantity = 0
        self._current_size = ''

    def _get_scales(self, orig_w: int, orig_h: int, n: int, y_offset: int) -> Tuple[int, int]:
        """
        Get the scales and maintain the aspect ratio.

        How the alg works:
            1. We calculate the so-called des_h(desired height) which is essentially just (cell height x n - 2y_offset)
            2. Then we get the k, which is just des_h divided by original height.
            3. We gotta get the new width value and simple proportion suits us.
            4. Then we just like calc the x_k just like we did with the y_k
            5. Returns you tuple of x_scale, y_scale

        :param orig_w - original width of the image:
        :param orig_h - original height of the image:
        :param n - height of a cell:
        :param y_offset - offset by y axis:
        :return tuple of x_scale, y_scale:
        """
        des_h = self._cell_height * n - y_offset * 2
        new_w = des_h * orig_w / orig_h

        return math.floor(new_w), math.floor(des_h)

    def _get_resized_image_data(self, im: Image, bound_width_height):
        # get the image and resize it
        im.thumbnail(bound_width_height, Image.ANTIALIAS)  # ANTIALIAS is important if shrinking

        # stuff the image data into a bytestream that excel can read
        im_bytes = io.BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes

    _cell_width = 565
    _cell_height = 85

    _default_size = 5

    def form_excel(self, id: int, request: Request):
        name = f'order{id}.xlsx'

        path = os.path.join(settings.BASE_DIR, 'media', 'documents', name)

        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()

        titles = ['??????', '??????', '??????', '??????/???', '??????']

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

        worksheet.merge_range('A1:E1', '??????', merge_title_format)

        worksheet.set_column('A:A', 80)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:E', 32)

        worksheet.set_row(1, 40)

        for idx, title in enumerate(titles):
            worksheet.write(f'{uppercase[idx]}2', title, bg_purple_format)

        order = get_object_or_404(Project.objects.all(), id=id)

        articles = [product.product.article for product in order.products.all()]

        products: List[List[ProductInfo]] = [order.products.filter(product__article=article)
                                             for article in list(set(articles))]

        start = 3

        for product_qty_list in products:
            merge_cells_count = len(product_qty_list) if len(
                product_qty_list) >= self._default_size else self._default_size

            for i in range(start - 1, start + merge_cells_count - 1):
                worksheet.set_row(i, 65)

            worksheet.merge_range(f'A{start}:A{start + merge_cells_count - 1}', '', merge_title_format)

            cells_left_unfilled = self._default_size - len(product_qty_list)

            for idx, product_qty in enumerate(product_qty_list):
                worksheet.write(
                    f'B{start + idx}',
                    str(product_qty.quantity),
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )

                worksheet.write(
                    f'C{start + idx}',
                    str(product_qty.product.size),
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )

                self._current_quantity = str(product_qty.quantity)
                self._current_size = str(product_qty.product.size)
                self._last_cell = start + idx

            if cells_left_unfilled == 4:
                worksheet.merge_range(
                    f'B{self._last_cell}:B{self._last_cell + 4}',
                    str(self._current_quantity),
                    merge_title_format
                )
                worksheet.merge_range(
                    f'C{self._last_cell}:C{self._last_cell + 4}',
                    str(self._current_size),
                    merge_title_format
                )
            elif cells_left_unfilled == 1:
                worksheet.write(
                    f'B{self._last_cell + 1}',
                    '',
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )
                worksheet.write(
                    f'C{self._last_cell + 1}',
                    '',
                    workbook.add_format({
                        **centered_and_border,
                        'font_size': 18,
                    })
                )
            elif cells_left_unfilled > 1:
                print(f'merging B{self._last_cell + 1}:C{self._last_cell + cells_left_unfilled}')
                worksheet.merge_range(f'B{self._last_cell + 1}:C{self._last_cell + cells_left_unfilled}', '', merge_title_format)

            if product_qty_list[0].product.photo:
                url = request.build_absolute_uri(product_qty_list[0].product.photo.photo.url)

                response = requests.get(url)
                img = Image.open(io.BytesIO(response.content))

                w, h = self._get_scales(
                    *img.size, merge_cells_count, 20
                )

                image_data = self._get_resized_image_data(img, (w, h))

                worksheet.insert_image(
                    f'A{start}',
                    url,
                    {'image_data': image_data, 'y_offset': 12}
                )

            start += merge_cells_count

        worksheet.set_row(start - 1, 65)
        worksheet.set_row(start, 65)
        worksheet.write(f'A{start}', '???? ????????????????', delivery_n_total_format)
        worksheet.write(f'B{start}', '', delivery_n_total_format)
        worksheet.write(f'A{start + 1}', 'TOTAL', delivery_n_total_format)
        worksheet.write(f'B{start + 1}', str(order.total_quantity), delivery_n_total_format)
        worksheet.write(f'C{start}', '', delivery_n_total_format)
        worksheet.write(f'C{start + 1}', '', delivery_n_total_format)

        for col in ['D', 'E']:
            for x in range(3, start + 2):
                worksheet.write(f'{col}{x}', '', merge_title_format)

        workbook.close()

        with open(path, 'rb') as f:
            order.excel = File(f, name=os.path.basename(f.name))
            order.save()

        return request.build_absolute_uri(f'media/documents/order{id}.xlsx/')
