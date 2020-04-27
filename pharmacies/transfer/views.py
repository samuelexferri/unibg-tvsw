import random
from math import sqrt

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from shop.models import Category, Product, Pharmacy
from transfer.forms import ProductForm


def homepage(request):
    products_all = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True).order_by('-created')
    featured_products = Product.objects.filter(featured=True)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'shop/base.html',
                  {'products_all': products_all, 'categories': categories, 'product': products,
                   'featured_products': featured_products})


def transfer(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            category = form['category'].value()
            quantity = form['quantity'].value()

            listaProducts = Product.objects.all().filter(category=category)  # Prodotti filtrati per categoria

            # Caso quantità non disponibile
            count = 0
            for p in listaProducts:
                count += p.quantity

            if count < int(quantity):
                messages.error(request, 'There is not enough products in all pharmacies')
                return redirect('transfer:transfer')
            else:
                messages.success(request, 'Your transfers request has been sent!')

                # Random GPS (Posizione iniziale cliente)
                x = random.randint(0, 100)
                y = random.randint(0, 100)

                doppia = algorithm_transfer(request, category, quantity, x, y)  # Chiamata algorithm_transfer()

                listIdPharmUsate = []
                for i in doppia[0]:
                    listIdPharmUsate.append(Pharmacy.objects.get(id=i).__str__())

                listQuantityPharmUsate = doppia[1]
                return render(request, 'transfer/transfer_done.html',
                              {'lid': listIdPharmUsate, 'lq': listQuantityPharmUsate, 'tot': quantity, 'x': x, 'y': y})
        else:
            messages.error(request, 'Error! Try again')
            return redirect('transfer:transfer')
    else:
        form = ProductForm()
    return render(request, "transfer/transfer.html", {'form': form})


def algorithm_transfer(request, category, quantity, x, y):
    listaProducts = Product.objects.all().filter(category=category)  # Prodotti filtrati per categoria

    listIdPharmUsate = []
    listQuantityPharmUsate = []

    while int(quantity) > 0:
        quintupla = findGreedy(listaProducts, x, y)  # Chiamata findGreedy() a ogni iterazione

        # Il cliente si è spostato presso la farmacia (nuova posizione)
        x = quintupla[2]
        y = quintupla[3]

        listIdPharmUsate.append(quintupla[0])

        if int(quantity) > quintupla[1]:
            listQuantityPharmUsate.append(quintupla[1])
        else:
            listQuantityPharmUsate.append(quantity)  # Ultima farmacia ne prende solo una parte

        quantity = int(quantity) - quintupla[1]  # Decremento la quantità richiesta

        # Popping (Escludere farmacia già scelta)
        listaProductsPoppata = []
        i = 0

        for p in listaProducts:
            if i != quintupla[4]:
                listaProductsPoppata.append(p)
            i += 1
        # END FOR
        listaProducts = listaProductsPoppata

    # END WHILE

    doppia = [listIdPharmUsate, listQuantityPharmUsate]
    return doppia


def findGreedy(listaProducts, x, y):
    sceltaGolosa = []  # Vettore pesi

    # Pesiamo quantità disponibile e distanza
    for prod in listaProducts:
        distanzapitagora = (x - prod.pharmacy.x) * (x - prod.pharmacy.x) + (y - prod.pharmacy.y) * (y - prod.pharmacy.y)

        # Stessa posizione della farmacia
        if distanzapitagora == 0:
            distanzapitagora = 0.01

        weigth = float(prod.quantity) / sqrt(distanzapitagora)
        sceltaGolosa.append(weigth)
    # END FOR

    # Massimizziamo il peso
    idPharmScelta = 0
    quantityScelta = 0
    xScelto = 0
    yScelto = 0
    indiceScelto = 0

    i = 0

    for prod in listaProducts:
        if i == 0:  # Inizializza con il primo prodotto
            pesoScelta = sceltaGolosa[i]

            idPharmScelta = prod.pharmacy.id
            quantityScelta = prod.quantity
            xScelto = prod.pharmacy.x
            yScelto = prod.pharmacy.y
            indiceScelto = i
        elif sceltaGolosa[i] > pesoScelta:
            pesoScelta = sceltaGolosa[i]  # Sovrascrivo il massimo massimo peso

            idPharmScelta = prod.pharmacy.id
            quantityScelta = prod.quantity
            xScelto = prod.pharmacy.x
            yScelto = prod.pharmacy.y
            indiceScelto = i

        i += 1  # Passo al prossimo prodotto

    # END FOR

    quintupla = [idPharmScelta, quantityScelta, xScelto, yScelto, indiceScelto]

    return quintupla
