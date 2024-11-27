from django.test import TestCase
from shop.forms import CategoryCreateForm


class CategoryCreateFormTestCase(TestCase):
    def test_field_label(self):
        form = CategoryCreateForm()
        # self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'категория')
        self.assertTrue(form.fields['name'].label, 'категория')

    def test_form_valid(self):
        form_data = {'name': 'Phones'}
        form = CategoryCreateForm(data=form_data)
        CategoryCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def test_form_not_valid(self):
    #     form_data = {'name': ''}
    #     form = CategoryCreateForm(data=form_data)
    #     CategoryCreateForm(data=form_data)
    #     self.assertTrue(form.is_valid())