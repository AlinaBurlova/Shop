from http.client import responses

from django.test import TestCase
from django.urls import reverse


class CategoryListTestCase(TestCase):
    # Проверка корректности пути
    def test_view_url_exist_location(self):
        response = self.client.get('/products/categories/')
        self.assertEqual(response.status_code, 200)

    # Проверка корректности имени маршрута
    def test_view_url_reverse_by_name(self):
        response = self.client.get(reverse('shop:categories'))
        self.assertEqual(response.status_code, 200)

    # Проверка наличия объекта контекста
    def test_view_set_categories_in_context(self):
        response = self.client.get(reverse('shop:categories'))
        # self.assertTrue('categories' in response.context)
        self.assertIn('categories', response.context)

    # Проверка корректности имени шаблона
    def test_view_correct_template(self):
        response = self.client.get(reverse('shop:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/admin/categories.html')



