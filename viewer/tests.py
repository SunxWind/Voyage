import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest import skip

from Voyage.settings import BASE_DIR
from viewer.models import City, Airport, Hotel, Trip, PurchasedTrip
from viewer.forms import TripPurchaseForm, TripForm


class TripFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        City.objects.create(name='Prague', country='Czech Republic', continent='Europe')

        City.objects.create(name='Beijing', country='China', continent='Asia')

        City.objects.create(name='Cairo', country='Egypt', continent='Africa')

        Hotel.objects.create(name='Aquapalace Hotel',
                             description='Some description',
                             city=City.objects.get(name='Prague')
                             )

        Hotel.objects.create(name='Celebrity International Grand Hotel',
                             description='Some description',
                             city=City.objects.get(name='Beijing')
                             )

        Hotel.objects.create(name='Waldorf Astoria Cairo Heliopolis Hotel',
                             description='Some description',
                             city=City.objects.get(name='Cairo')
                             )

        Airport.objects.create(name='Prague International Airport (PRG)',
                               city=City.objects.get(name='Prague')
                               )

        Airport.objects.create(name='Beijing Capital International Airport (PEK)',
                               city=City.objects.get(name='Beijing')
                               )

        Airport.objects.create(name='Beijing Daxing International Airport (PKX)',
                               city=City.objects.get(name='Beijing')
                               )

        Airport.objects.create(name='Cairo International Airport (CAI)',
                               city=City.objects.get(name='Cairo')
                               )

    # @skip('Skip')
    def test_trip_form_is_valid(self):

        form = TripForm(
            data={
                'code': 'euru001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-02-06',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertTrue(form.is_valid())

    def test_trip_form_code_length_is_invalid(self):

        form = TripForm(
            data={
                'code': 'eur001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-02-06',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_letters_code_is_invalid(self):

        form = TripForm(
            data={
                'code': 'eu0r001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-02-06',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_digits_code_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru0g1',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-02-06',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_departure_date_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-01-18',
                'return_date': '2025-01-31',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_return_date_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-01-18',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_return_date_earlier_depart_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-18',
                'return_date': '2025-02-01',
                'duration': '5',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_form_duration_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru001',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-02-01',
                'return_date': '2025-02-10',
                'duration': '11',
                'service_standard': 'BB',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'promoted': '1',
                'adult_places': '5',
                'child_places': '8',
                'description': 'some description. some description. some description',
                'short_description': 'some description. some description. some description',
                'image': SimpleUploadedFile(name='Beijing.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing-card.jpg'), 'rb').read(), content_type='image/jpeg'),
                'image_small': SimpleUploadedFile(name='Beijing-card.jpg', content=open(
                    os.path.join(BASE_DIR, 'media/images/Beijing.jpg'), 'rb').read(), content_type='image/jpeg')
            }
        )
        self.assertFalse(form.is_valid())


class TripPurchaseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        City.objects.create(name='Prague', country='Czech Republic', continent='Europe')

        City.objects.create(name='Beijing', country='China', continent='Asia')

        Hotel.objects.create(name='Celebrity International Grand Hotel',
                             description='Some description',
                             city=City.objects.get(name='Beijing')
                             )

        Airport.objects.create(name='Prague International Airport (PRG)',
                               city=City.objects.get(name='Prague')
                               )

        Airport.objects.create(name='Beijing Capital International Airport (PEK)',
                               city=City.objects.get(name='Beijing')
                               )

        Trip.objects.create(
            code='EUCN001',
            where_from=City.objects.get(name='Prague'),
            airport_depart=Airport.objects.get(name='Prague International Airport (PRG)'),
            where_to=City.objects.get(name='Beijing'),
            airport_arrive=Airport.objects.get(name='Beijing Capital International Airport (PEK)'),
            where_to_hotel=Hotel.objects.get(name='Celebrity International Grand Hotel'),
            departure_date='2025-02-01',
            return_date='2025-02-08',
            duration=7,
            service_standard='AI',
            adult_price=20000.00,
            child_price=18000.00,
            promoted=True,
            adult_places=5,
            child_places=8,
            description='Some description. Some description. Some description.',
            short_description='Some description. Some description. Some description.',
            image=None,
            image_small=None
        )

    # @skip('Skip')
    def test_trip_purchase_form_is_valid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '1995-01-12',
                'email': 'rudolfvychodil@email.cz',
                'phone_number': '+420353252161',
                'amount_adult': '2',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertTrue(form.is_valid())

    def test_trip_purchase_form_email_is_invalid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '1995-01-12',
                'email': '@email.cz',
                'phone_number': '+420353252161',
                'amount_adult': '2',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_purchase_form_phone_number_is_invalid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '1995-01-12',
                'email': 'rudolfvychodil@email.cz',
                'phone_number': '252161',
                'amount_adult': '2',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_purchase_form_birth_date_is_invalid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '2030-01-12',
                'email': 'rudolfvychodil@email.cz',
                'phone_number': '+420353252161',
                'amount_adult': '2',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_purchase_form_birth_date_child_is_invalid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '2011-01-12',
                'email': 'rudolfvychodil@email.cz',
                'phone_number': '+420353252161',
                'amount_adult': '2',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertFalse(form.is_valid())

    def test_trip_purchase_form_no_adults_is_invalid(self):

        form = TripPurchaseForm(
            data={
                'trip': '1',
                'firstname': 'Rudolf',
                'lastname': 'Vychodil',
                'birth_date': '1995-01-12',
                'email': 'rudolfvychodil@email.cz',
                'phone_number': '+420353252161',
                'amount_adult': '0',
                'amount_child': '2',
                'adult_price': '20000.00',
                'child_price': '18000.00',
                'total_adult_price': '40000.00',
                'total_child_price': '36000.00',
                'total_price': '76000.00'
            }
        )
        self.assertFalse(form.is_valid())
