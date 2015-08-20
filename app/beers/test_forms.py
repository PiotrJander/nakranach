from django.test import TestCase
from app.beers.forms import CreateBeerForm
from app.beers.models import Style, Brewery, Beer


class TestCreateBeerForm(TestCase):
    def test_the_form_can_be_instantiated(self):
        CreateBeerForm()

    def test_form_valid_with_create_new_brewery_and_valid_data(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_create_new_brewery_and_blank_brewery_name(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': '',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_with_create_new_brewery_and_blank_brewery_country(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form_with_create_new_brewery_saves(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data)
        form.save()

        self.assertTrue(Beer.objects.filter(name='Matysiowe'))

    def test_form_valid_with_not_create_new_brewery_and_valid_data(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': brewery.id,
            'style': style.id,
            'ibu': '',
            'abv': '',
            # 'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_not_create_new_brewery_and_blank_brewery(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form_with_not_create_new_brewery_saves(self):
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': brewery.id,
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data)
        form.save()

        self.assertTrue(Beer.objects.filter(name='Matysiowe'))
