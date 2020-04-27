from django.test import TestCase
from django.utils.text import slugify

from shop.models import *
from transfer.views import *


# Transfer(request) si occupa di chiamare l'algoritmo.
# Tuttavia prima fa il controllo sulla quantità e poi:
# Se quantità insufficiente -> Stampa a video 'There is not enough products in all pharmacies' e NON chiama l'algoritmo
# Se quantità sufficiente   -> Chiama l'algoritmo e stampa a video: 'Your transfers request has been sent!'

# CASO 1: Basta una farmacia per soddisfare la richiesta che è la più vicina
class TransferTest1(TestCase):
    def test_algorithm_Transfer1(self):
        xScelta = 0
        yScelta = 0
        quantitaScelta = 40
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=10, y=10,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=20, y=20,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=50, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=75, y=75,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=40,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=0,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=0,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia1.id])
        self.assertEqual(doppia[1], [40])


# CASO 2: NON va dalla prima farmacia nonostante sia la più vicina ma da tutte le altre che sono più lontane visto
# che andare dalla prima porterebbe solo 1 prodotto
class TransferTest2(TestCase):
    def test_algorithm_Transfer2(self):
        xScelta = 0
        yScelta = 0
        quantitaScelta = 70
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=10, y=10,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=20, y=20,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=30, y=35,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=45, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=1,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=30,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=40,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia2.id, farmacia3.id, farmacia4.id])
        self.assertEqual(doppia[1], [30, 20, 20])


# CASO 3: La scelta ottima locale porta ad una scelta ottima globale in quanto non utilizza la farmacia3 che non sarebbe
# stata in grado di soddisfare la quantità richiesta e sarebbe stata necessaria anche la farmacia4
class TransferTest3(TestCase):
    def test_algorithm_Transfer3(self):
        xScelta = 0
        yScelta = 0
        quantitaScelta = 50
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=10, y=10,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=20, y=20,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=30, y=35,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=45, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=10,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=5,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia1.id, farmacia2.id, farmacia4.id])
        self.assertEqual(doppia[1], [20, 10, 20])


# CASO 4: La scelta ottima locale porta ad una scelta NON ottima globale in quanto utilizza la farmacia3 che non è
# stata in grado di soddisfare la quantità richiesta e quindi bisogna utilizzare anche la farmacia4
class TransferTest4(TestCase):
    def test_algorithm_Transfer4(self):
        xScelta = 0
        yScelta = 0
        quantitaScelta = 50
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=10, y=10,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=20, y=20,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=22, y=22,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=45, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=10,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=5,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia1.id, farmacia2.id, farmacia3.id, farmacia4.id])
        self.assertEqual(doppia[1], [20, 10, 5, 15])


# CASO 5: Scelta ambigua in quanto per la prima scelta presenta entrambi lo stesso vantaggio sia 1 che 2
# Sceglie la farmacia con indice minore in caso di parità di vantaggio
class TransferTest5(TestCase):
    def test_algorithm_Transfer5(self):
        xScelta = 50
        yScelta = 50
        quantitaScelta = 50
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=25, y=25,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=20, y=20,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=75, y=75,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=100, y=100,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=20,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia1.id, farmacia2.id, farmacia3.id])
        self.assertEqual(doppia[1], [20, 20, 10])


# CASO 6: Nonostante farmacia1 abbia 500 di quantità viene preferita farmacia2 perchè nettamente più vicina
# e solamente come seconda farmacia la farmacia1 viene scelta quando rimane nettamente quella con maggiore
# quantità
class TransferTest6(TestCase):
    def test_algorithm_Transfer6(self):
        xScelta = 50
        yScelta = 50
        quantitaScelta = 1000
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=0, y=0,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=65, y=65,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=22, y=22,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=45, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=500,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=201,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=290,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=10,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia2.id, farmacia1.id, farmacia3.id, farmacia4.id])
        self.assertEqual(doppia[1], [201, 500, 290, 9])


# CASO 6: Abbiamo cercato il trade-off e abbiamo constatato che giustamente per valori di:
# farmacia1 <= 669 si ha che la prima farmacia scelta è la farmacia2
# farmacia1 >= 670 si ha che la prima farmacia scelta è la farmacia1
class TransferTest7(TestCase):
    def test_algorithm_Transfer7(self):
        xScelta = 50
        yScelta = 50
        quantitaScelta = 1000
        categoriaScelta = Category.objects.create(name="Antinfiammatori", description="Text")

        user1 = User.objects.create(username='TestUser1')
        user2 = User.objects.create(username='TestUser2')
        user3 = User.objects.create(username='TestUser3')
        user4 = User.objects.create(username='TestUser4')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia1.png", x=0, y=0,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia2.png", x=65, y=65,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia3.png", x=22, y=22,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia4 = Pharmacy.objects.create(owner=user4, name="farmacia4", image="farmacia4.png", x=45, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        farmacia4.save()

        prodotto1 = Product.objects.create(name="prodotto1", category=categoriaScelta, pharmacy=farmacia1,
                                           image="prodotto1.png", description="Text", brand="brand", quantity=670,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto2 = Product.objects.create(name="prodotto2", category=categoriaScelta, pharmacy=farmacia2,
                                           image="prodotto2.png", description="Text", brand="brand", quantity=201,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto3 = Product.objects.create(name="prodotto3", category=categoriaScelta, pharmacy=farmacia3,
                                           image="prodotto3.png", description="Text", brand="brand", quantity=290,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())
        prodotto4 = Product.objects.create(name="prodotto4", category=categoriaScelta, pharmacy=farmacia4,
                                           image="prodotto4.png", description="Text", brand="brand", quantity=10,
                                           price=10, shipping_fee=2, slug=slugify(1).__str__())

        prodotto1.save()
        prodotto2.save()
        prodotto3.save()
        prodotto4.save()

        doppia = algorithm_transfer(self, categoriaScelta, quantitaScelta, xScelta, yScelta)
        # doppia[0] contiene la lista degli ID delle farmacie interessate
        # doppia[1] contiene la lista delle quantità presa da ogni farmacia
        self.assertEqual(doppia[0], [farmacia1.id, farmacia3.id, farmacia2.id])
        self.assertEqual(doppia[1], [670, 290, 40])
