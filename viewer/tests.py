from pathlib import Path
import io, os
from PIL import Image
import tempfile

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest import skip

from Voyage.settings import BASE_DIR
from viewer.forms import TripPurchaseForm, TripForm
from viewer.models import City, Airport, Hotel, Trip, PurchasedTrip


class ExampleTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: spustí se jednou na začátku a nastaví (vytvoří) testovací data.")

    def setUp(self):
        print("setUp: spustí se před každým testem")

    def test_false(self):
        print("Testovací metoda: test_false")
        result = False
        self.assertFalse(result)

    def test_add(self):
        print("Testovací metoda: test_add")
        result = 1 + 4
        self.assertEqual(result, 5)


class TripFormTest(TestCase):
    """
    def __init__(self):
        super().__init__()
    test_image_path = (Path(__file__).resolve().parent.parent / "media/images/Beijing.jpg")
    test_small_image_path = (Path(__file__).resolve().parent.parent / "media/images/Beijing-card.jpg")
    """

    """
    def generate_img_file(self, file_name):

        file = io.BytesIO()
        image = Image.new('RGBA', size=(275, 200), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = f'{file_name}.png'
        file.seek(0)

        return file
    """

    @classmethod
    def setUpTestData(cls):

        City.objects.create(name='Prague',
                            country='Czech Republic',
                            continent='Europe'
                            )

        City.objects.create(name='Beijing',
                            country='China',
                            continent='Asia'
                            )

        City.objects.create(name='Cairo',
                            country='Egypt',
                            continent='Africa'
                            )

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
                'departure_date': '2025-01-20',
                'return_date': '2025-01-31',
                'duration': '5',
                'type': 'BB',
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
                'departure_date': '2025-01-20',
                'return_date': '2025-01-31',
                'duration': '5',
                'type': 'BB',
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
                'departure_date': '2025-01-20',
                'return_date': '2025-01-31',
                'duration': '5',
                'type': 'BB',
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

    def test_trip_form_digital_code_is_invalid(self):

        form = TripForm(
            data={
                'code': 'euru0g1',
                'where_from': '1',
                'airport_depart': '1',
                'where_to': '2',
                'airport_arrive': '2',
                'where_to_hotel': '2',
                'departure_date': '2025-01-20',
                'return_date': '2025-01-31',
                'duration': '5',
                'type': 'BB',
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
                'type': 'BB',
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
                'type': 'BB',
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
                'type': 'BB',
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
                'type': 'BB',
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

