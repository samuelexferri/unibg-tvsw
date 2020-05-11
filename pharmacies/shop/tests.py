import unittest
from unittest import mock

from django.core.files import File
from django.test import LiveServerTestCase
from django.test import TestCase
from django.test import tag
from django.urls import reverse
from django.utils.text import slugify
from parameterized import parameterized_class
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from shop.views import Payment, FakeCreditCard

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

from shop.forms import *
from shop.models import *

"""
Models tests
"""


class ContactModelTest(TestCase):
    def create_contact(
        self,
        name="Test",
        email="test@mail.com",
        subject="Text",
        message="Text",
    ):
        return Contact.objects.create(
            name=name, email=email, subject=subject, message=message
        )

    def test_contact_creation(self):
        w = self.create_contact()
        self.assertTrue(isinstance(w, Contact))
        fields = w.id, w.name, w.email, w.subject, w.message
        self.assertEqual(w.__unicode__(), fields)

    def test_contact_str(self):
        category = Contact.objects.create(
            name="Test", email="test@mail.com", subject="Text", message="Text"
        )
        self.assertEqual(str(category), category.name)


class PharmacyModelTest(TestCase):
    def create_pharmacy(
        self,
        name="Farmacia",
        image="farmacia.png",
        x=50,
        y=0,
        slot4hMinWeek=5,
        location="Bergamo",
        description="Text",
    ):
        user = User.objects.create(username="TestUser")
        return Pharmacy.objects.create(
            owner=user,
            name=name,
            image=image,
            x=x,
            y=y,
            slot4hMinWeek=slot4hMinWeek,
            location=location,
            description=description,
        )

    def test_pharmacy_creation(self):
        w = self.create_pharmacy()
        self.assertTrue(isinstance(w, Pharmacy))
        fields = w.id, w.owner, w.name
        self.assertEqual(w.__unicode__(), fields)

    def test_pharmacy_str(self):
        user = User.objects.create(username="TestUser")
        category = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=0,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        self.assertEqual(
            str(category), "[" + category.id.__str__() + "] " + category.name
        )


class CategoryModelTest(TestCase):
    def create_category(self, name="Antinfiammatorio", description="Text"):
        return Category.objects.create(name=name, description=description)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        fields = w.id, w.name, w.description
        self.assertEqual(w.__unicode__(), fields)

    def test_category_str(self):
        category = Category.objects.create(
            name="Antinfiammatorio", description="Text"
        )
        self.assertEqual(str(category), category.name)


class ProductModelTest(TestCase):
    def create_product(
        self,
        name="Oki",
        image="pharmacy.png",
        description="Text",
        brand="Brand",
        quantity=30,
        price=20,
        shipping_fee=10,
    ):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        return Product.objects.create(
            name=name,
            category=categoria,
            pharmacy=farmacia,
            image=image,
            description=description,
            brand=brand,
            quantity=quantity,
            price=price,
            shipping_fee=shipping_fee,
            slug=slugify(1).__str__(),
        )

    def test_product_creation(self):
        w = self.create_product()
        self.assertTrue(isinstance(w, Product))
        fields = w.id, w.name, w.description
        self.assertEqual(w.__unicode__(), fields)

    def test_product_str(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        category = Product.objects.create(
            category=categoria,
            pharmacy=farmacia,
            name="Oki",
            image="pharmacy.png",
            description="Text",
            brand="Brand",
            quantity=30,
            price=20,
            shipping_fee=10,
        )
        self.assertEqual(str(category), category.name)


class ReviewModelTest(TestCase):
    def create_review(self, review="Text"):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        prodotto = Product.objects.create(
            name="Tachipirina",
            category=categoria,
            pharmacy=farmacia,
            image="image.png",
            description="Text",
            brand="Brand",
            quantity=10,
            price=2,
            shipping_fee=1,
            slug=slugify(1).__str__(),
        )
        return Review.objects.create(
            review=review, user=user, product=prodotto
        )

    def test_review_creation(self):
        w = self.create_review()
        self.assertTrue(isinstance(w, Review))
        fields = w.id, w.review
        self.assertEqual(w.__unicode__(), fields)

    def test_review_str(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        prodotto = Product.objects.create(
            name="Tachipirina",
            category=categoria,
            pharmacy=farmacia,
            image="image.png",
            description="Text",
            brand="Brand",
            quantity=10,
            price=2,
            shipping_fee=1,
            slug=slugify(1).__str__(),
        )
        category = Review.objects.create(
            review="Text", user=user, product=prodotto
        )
        self.assertEqual(str(category), category.product.__str__())


class BuyerModelTest(TestCase):
    def create_buyer(
        self,
        full_name="Mario",
        phone=123,
        city="Bergamo",
        address="via Vittoria 20",
    ):
        return Buyer.objects.create(
            full_name=full_name, phone=phone, city=city, address=address
        )

    def test_buyer_creation(self):
        w = self.create_buyer()
        self.assertTrue(isinstance(w, Buyer))
        fields = w.id, w.full_name, w.phone
        self.assertEqual(w.__unicode__(), fields)

    def test_buyer_str(self):
        category = Buyer.objects.create(
            full_name="Mario",
            phone=123,
            city="Bergamo",
            address="via Vittoria 20",
        )
        self.assertEqual(str(category), category.full_name)


"""
Forms tests (Also parameterized)
"""


@parameterized_class(
    ("name", "email", "subject", "message", "expected_result"),
    [
        ("Test", "test@email.com", "Text", "Text", True),
        ("Test", "without.at", "Text", "Text", False),
        ("Test", "without@domain", "Text", "Text", False),
        ("", "test@email.com", "Text", "Text", False),
        (
            "LongNameLongNameLongNameLongNameLongNameLongNameLongNameLongName",
            "test@email.com",
            "Text",
            "Text",
            False,
        ),
    ],
)
class ContactFormTestParametrized(TestCase):
    def test_form(self):
        data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
        }
        form = ContactForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)


class ContactFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "name": "Test",
            "email": "test@mail.com",
            "subject": "Text",
            "message": "Text",
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "name": "Test",
            "email": "testmail.com",
            "subject": "Text",
            "message": "Text",
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())


# TODO SellProductFormTest

"""
class SellProductFormTest(TestCase):

    def test_valid_form(self):
        with open('media/products/oki.jpg', 'rb') as img:
            user = User.objects.create(username='TestUser')
            farmacia = Pharmacy.objects.create(owner=user, name="Farmacia", image="farmacia.png", x=50, y=50,
                                               slot4hMinWeek=5, location="Bergamo", description="Text").id
            categoria = Category.objects.create(name="Antinfiammatorio", description="Text",
                                                slug=slugify("Antinfiammatorio").__str__()).id

            data = {'pharmacy': farmacia, 'category': categoria, 'name': "Oki", 'image': "img", 'description': "Text",
                    'brand': "Brand", 'quantity': 10,
                    'price': 20.00, 'shipping_fee': 5.00, 'slug': slugify(1).__str__()}

            file_dict = {'file': SimpleUploadedFile(img.name, img.read())}

            form = SellProductForm(data=data, files=file_dict)

            self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # TODO
        return
"""


@parameterized_class(
    ("full_name", "phone", "city", "address", "expected_result"),
    [
        ("Test", 123, "Bergamo", "Text", True),
        ("Test", 123, "CityNotInChoices", "Text", False),
        ("Test", True, "Text", "Text", False),
    ],
)
class BuyerDeliveryFormTest(TestCase):
    def test_form(self):
        data = {
            "full_name": self.full_name,
            "phone": self.phone,
            "city": self.city,
            "address": self.address,
        }
        form = BuyerDeliveryForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)


class BuyerDeliveryFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "full_name": "Test",
            "phone": 123,
            "city": "Bergamo",
            "address": "Text",
        }
        form = BuyerDeliveryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "full_name": "Test",
            "phone": 123,
            "city": "CittàNonPresente",
            "address": "Text",
        }
        form = BuyerDeliveryForm(data=data)
        self.assertFalse(form.is_valid())


@parameterized_class(
    ("review", "expected_result"),
    [
        ("Text", True),
        ("", False),
        (
            "LongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReviewLongReview",
            False,
        ),
    ],
)
class ReviewFormTest(TestCase):
    def test_form(self):
        data = {"review": self.review}
        form = ReviewForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)


class ReviewFormTest(TestCase):
    def test_valid_form(self):
        data = {"review": "Text"}
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
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_about(self):
        url = reverse("shop:about")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_contact(self):
        url = reverse("shop:contact")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_pharmacy_list(self):
        url = reverse("shop:pharmacies_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_pharmacies_detail(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        url = reverse("shop:pharmacies_detail", args=(farmacia.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_categories(self):
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        url = reverse("shop:categories", args=(categoria.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_products_list(self):
        url = reverse("shop:products_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_products_detail(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        prodotto = Product.objects.create(
            name="Tachipirina",
            category=categoria,
            pharmacy=farmacia,
            image="image.png",
            description="Text",
            brand="Brand",
            quantity=10,
            price=2,
            shipping_fee=1,
            slug=slugify(1).__str__(),
        )
        url = reverse("shop:products_detail", args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_search(self):
        url = reverse("shop:search")  # Search
        resp = self.client.get(url + "?q=oki")
        self.assertEqual(resp.status_code, 200)

    def test_sell_product(self):
        url = reverse("shop:sell_product")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_buy_items(self):
        url = reverse("shop:buy_items")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_cart(self):
        url = reverse("shop:cart")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_reset_cart(self):
        url = reverse("shop:reset_cart")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_payment(self):
        url = reverse("shop:payment")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_checkout(self):
        url = reverse("shop:checkout")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_add_cart(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        prodotto = Product.objects.create(
            name="Tachipirina",
            category=categoria,
            pharmacy=farmacia,
            image="image.png",
            description="Text",
            brand="Brand",
            quantity=10,
            price=2,
            shipping_fee=1,
            slug=slugify(1).__str__(),
        )
        url = reverse("shop:add_cart", args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_add_review(self):
        user = User.objects.create(username="TestUser")
        farmacia = Pharmacy.objects.create(
            owner=user,
            name="Farmacia",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        categoria = Category.objects.create(
            name="Antinfiammatorio",
            description="Text",
            slug=slugify("Antinfiammatorio").__str__(),
        )
        prodotto = Product.objects.create(
            name="Tachipirina",
            category=categoria,
            pharmacy=farmacia,
            image="image.png",
            description="Text",
            brand="Brand",
            quantity=10,
            price=2,
            shipping_fee=1,
            slug=slugify(1).__str__(),
        )
        url = reverse("shop:add_review", args=(prodotto.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect


"""
Selenium, two command prompt necessary
"""
"""

@tag("selenium")
class ContactViewSeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )

    def test_selenium_contact(self):
        self.driver.get("http://localhost:8000/shop/contact")
        self.driver.find_element_by_id("id_name").send_keys("Gino")
        self.driver.find_element_by_id("id_email").send_keys("gino@mail.com")
        self.driver.find_element_by_id("id_subject").send_keys("Text")
        self.driver.find_element_by_id("id_message").send_keys("Text")
        self.driver.find_element_by_id("submit").click()  # Submit button
        self.assertIn(
            "http://localhost:8000/shop/contact", self.driver.current_url
        )

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
"""

"""
Mock tests
"""


class PaymentTestCase(unittest.TestCase):
    @mock.patch("shop.views.calculate_amount", autospec=True)
    def test_process_cc_with_credit(self, mock_calculate_amount):
        cc = FakeCreditCard(50)
        mock_calculate_amount.return_value = 25
        payment = Payment(1, cc)
        status = payment.process(self)
        self.assertEqual(status, "processed")

    @mock.patch("shop.views.calculate_amount", autospec=True)
    def test_process_cc_without_credit(self, mock_calculate_amount):
        cc = FakeCreditCard(50)
        mock_calculate_amount.return_value = 200
        payment = Payment(1, cc)
        status = payment.process(self)
        self.assertEqual(status, "cancelled")


class PharmacyModelTestMockFile(TestCase):
    def create_pharmacy_image(
        self,
        image,
        name="Farmacia",
        x=50,
        y=0,
        slot4hMinWeek=5,
        location="Bergamo",
        description="Text",
    ):
        user = User.objects.create(username="TestUser")
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = image
        return Pharmacy(
            owner=user,
            name=name,
            image=file_mock,
            x=x,
            y=y,
            slot4hMinWeek=slot4hMinWeek,
            location=location,
            description=description,
        )

    def test_pharmacy_creation_image(self):
        w = self.create_pharmacy_image("image.png")
        self.assertTrue(isinstance(w, Pharmacy))
        fields = w.id, w.owner, w.name
        self.assertEqual(w.__unicode__(), fields)
        self.assertEqual(w.image.name, "image.png")


if __name__ == "__main__":
    unittest.main()
