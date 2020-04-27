import unittest

from django.test import LiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from selenium import webdriver

from shop.forms import *
from shop.models import *

"""
Models tests
"""


class ContactModelTest(TestCase):
    def create_contact(self, name="Test", email="test@mail.com", subject="Text", message="Text"):
        return Contact.objects.create(name=name, email=email, subject=subject, message=message)

    def test_contact_creation(self):
        w = self.create_contact()
        self.assertTrue(isinstance(w, Contact))
        fields = w.id, w.name, w.email, w.subject, w.message
        self.assertEqual(w.__unicode__(), fields)


class PharmacyModelTest(TestCase):
    def create_pharmacy(self, name="Farmacia", image="farmacia.png", x=50, y=0, slot4hMinWeek=5, location="Bergamo",
                        description="Text"):
        user = User.objects.create(username='TestUser')
        return Pharmacy.objects.create(owner=user, name=name, image=image, x=x, y=y, slot4hMinWeek=slot4hMinWeek,
                                       location=location, description=description)

    def test_pharmacy_creation(self):
        w = self.create_pharmacy()
        self.assertTrue(isinstance(w, Pharmacy))
        fields = w.id, w.owner, w.name
        self.assertEqual(w.__unicode__(), fields)


class CategoryModelTest(TestCase):
    def create_category(self, name="Antinfiammatorio", description="Text"):
        return Category.objects.create(name=name, description=description)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        fields = w.id, w.name, w.description
        self.assertEqual(w.__unicode__(), fields)


class ProductModelTest(TestCase):
    def create_product(self, name="Oki", image="pharmacy.png", description="Text", brand="Brand", quantity=30, price=20,
                       shipping_fee=10):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        return Product.objects.create(name=name, category=categoria, pharmacy=farmacia, image=image,
                                      description=description, brand=brand, quantity=quantity, price=price,
                                      shipping_fee=shipping_fee, slug=slugify(1).__str__())

    def test_product_creation(self):
        w = self.create_product()
        self.assertTrue(isinstance(w, Product))
        fields = w.id, w.name, w.description
        self.assertEqual(w.__unicode__(), fields)


class ReviewModelTest(TestCase):
    def create_review(self, review="Ottimo"):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        prodotto = Product.objects.create(name="Tachipirina", category=categoria, pharmacy=farmacia, image="image.png",
                                          description="Text", brand="Brand", quantity=10, price=2, shipping_fee=1,
                                          slug=slugify(1).__str__())
        return Review.objects.create(review=review, user=user, product=prodotto)

    def test_review_creation(self):
        w = self.create_review()
        self.assertTrue(isinstance(w, Review))
        fields = w.id, w.review
        self.assertEqual(w.__unicode__(), fields)


class BuyerModelTest(TestCase):

    def create_buyer(self, full_name="Mario", phone=123, city="Bergamo", address="via Vittoria 20"):
        return Buyer.objects.create(full_name=full_name, phone=phone, city=city, address=address)

    def test_buyer_creation(self):
        w = self.create_buyer()
        self.assertTrue(isinstance(w, Buyer))
        fields = w.id, w.full_name, w.phone
        self.assertEqual(w.__unicode__(), fields)


"""
Forms tests
"""


class ContactFormTest(TestCase):
    def test_valid_form(self):
        data = {'name': "Test", 'email': "test@mail.com", 'subject': "Text", 'message': "Text"}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Mail without @
        data = {'name': "Test", 'email': "testmail.com", 'subject': "Text", 'message': "Text"}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())


# TODO Test SellProductForm
"""
class SellProductForm(TestCase):

    def test_valid_form(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text", slug=slugify("Antinfiammatorio").__str__())
        data = {'pharmacy': farmacia, 'name': "Oki", 'image': "image.png", 'category': categoria, 'description': "Text",
                'Brand': "Brand", 'quantity': 10, 'price': 20, 'shipping_fee': 5, 'slug':slugify(1).__str__()}
        form = SellProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text", slug=slugify("Antinfiammatorio").__str__())
        data = {'pharmacy': farmacia, 'name': "Oki", 'image': "image.png", 'category': categoria, 'description': "Text",
                'Brand': "Brand", 'quantity': 10, 'price': 20, 'shipping_fee': 5, 'slug':slugify(1).__str__()}
        form = SellProductForm(data=data)
        self.assertFalse(form.is_valid())
"""


class BuyerDeliveryFormTest(TestCase):
    def test_valid_form(self):
        data = {'full_name': "Test", 'phone': 123, 'city': "Bergamo", 'address': "Text"}
        form = BuyerDeliveryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'full_name': "Test", 'phone': 123, 'city': "CittàNonPresente", 'address': "Text"}
        form = BuyerDeliveryForm(data=data)
        self.assertFalse(form.is_valid())


class ReviewFormTest(TestCase):
    def test_valid_form(self):
        data = {'review': "Text"}
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # No data passed
        form = ReviewForm()
        self.assertFalse(form.is_valid())


"""
Views tests
"""


class ViewTest(TestCase):
    def test_homepage(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_about(self):
        url = reverse('shop:about')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_contact(self):
        url = reverse('shop:contact')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_pharmacy_list(self):
        url = reverse('shop:pharmacies_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_pharmacies_detail(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        url = reverse('shop:pharmacies_detail', args=(farmacia.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_categories(self):
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        url = reverse('shop:categories', args=(categoria.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_products_list(self):
        url = reverse('shop:products_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_products_detail(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        prodotto = Product.objects.create(name="Tachipirina", category=categoria, pharmacy=farmacia, image="image.png",
                                          description="Text", brand="Brand", quantity=10, price=2, shipping_fee=1,
                                          slug=slugify(1).__str__())
        url = reverse('shop:products_detail', args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # TODO Test Search
    """
    def test_search(self):
        url = reverse('shop:search') # Search
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    """

    def test_sell_product(self):
        url = reverse('shop:sell_product')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_buy_items(self):
        url = reverse('shop:buy_items')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_cart(self):
        url = reverse('shop:cart')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_reset_cart(self):
        url = reverse('shop:reset_cart')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_payment(self):
        url = reverse('shop:payment')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_checkout(self):
        url = reverse('shop:checkout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_add_cart(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        prodotto = Product.objects.create(name="Tachipirina", category=categoria, pharmacy=farmacia, image="image.png",
                                          description="Text", brand="Brand", quantity=10, price=2, shipping_fee=1,
                                          slug=slugify(1).__str__())
        url = reverse('shop:add_cart', args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_add_review(self):
        user = User.objects.create(username='TestUser')
        farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                           slot4hMinWeek=5, location="Bergamo", description="Text")
        categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                            slug=slugify("Antinfiammatorio").__str__())
        prodotto = Product.objects.create(name="Tachipirina", category=categoria, pharmacy=farmacia, image="image.png",
                                          description="Text", brand="Brand", quantity=10, price=2, shipping_fee=1,
                                          slug=slugify(1).__str__())
        url = reverse('shop:add_review', args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect


"""
Views tests (Uses Selenium), two command prompt necessary
"""


class ContactViewSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        last_height = self.driver.execute_script("return document.body.scrollHeight")

    def test_selenium_contact(self):
        self.driver.get("http://localhost:8000/shop/contact")
        self.driver.find_element_by_id('id_name').send_keys("Gino")
        self.driver.find_element_by_id('id_email').send_keys("gino@mail.com")
        self.driver.find_element_by_id('id_subject').send_keys("Text")
        self.driver.find_element_by_id('id_message').send_keys("Text")
        self.driver.find_element_by_id('submit').click()  # Submit button
        self.assertIn("http://localhost:8000/shop/contact", self.driver.current_url)

    def tearDown(self):
        self.driver.quit


if __name__ == '__main__':
    unittest.main()
