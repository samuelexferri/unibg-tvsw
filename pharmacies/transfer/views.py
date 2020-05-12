import random
from math import sqrt

import icontract
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from shop.models import Category, Product, Pharmacy
from transfer.forms import ProductForm


def homepage(request):
    products_all = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True).order_by("-created")
    featured_products = Product.objects.filter(featured=True)
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products = paginator.get_page(page)
    return render(
        request,
        "shop/base.html",
        {
            "products_all": products_all,
            "categories": categories,
            "product": products,
            "featured_products": featured_products,
        },
    )


def transfer(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            category = form["category"].value()
            quantity = form["quantity"].value()

            lista_products = Product.objects.all().filter(
                category=category
            )  # Prodotti filtrati per categoria

            # Caso quantità non disponibile
            count = 0
            for p in lista_products:
                count += p.quantity

            if count < int(quantity):
                messages.error(
                    request, "There is not enough products in all pharmacies"
                )
                return redirect("transfer:transfer")
            else:
                messages.success(
                    request, "Your transfers request has been sent!"
                )

                # Random GPS (Posizione iniziale cliente)
                x = random.randint(0, 100)
                y = random.randint(0, 100)

                doppia = algorithm_transfer(
                    request, category, quantity, x, y
                )  # Chiamata algorithm_transfer()

                list_id_pharm_usate = []
                for i in doppia[0]:
                    list_id_pharm_usate.append(
                        Pharmacy.objects.get(id=i).__str__()
                    )

                list_quantity_pharm_usate = doppia[1]
                return render(
                    request,
                    "transfer/transfer_done.html",
                    {
                        "lid": list_id_pharm_usate,
                        "lq": list_quantity_pharm_usate,
                        "tot": quantity,
                        "x": x,
                        "y": y,
                    },
                )
        else:
            messages.error(request, "Error! Try again")
            return redirect("transfer:transfer")
    else:
        form = ProductForm()
    return render(request, "transfer/transfer.html", {"form": form})


@icontract.require(lambda quantity: quantity > 0, "quantity must be positive")
@icontract.require(lambda x: 0 <= x <= 100, "coordinate 0 <= x <= 100")
@icontract.require(lambda y: 0 <= y <= 100, "coordinate 0 <= y <= 100")
@icontract.require(
    lambda category: Product.objects.all().filter(category=category).count()
    >= 1,
    "at least one product of that category is required",
)
@icontract.ensure(lambda result: len(result[0]) == len(result[1]))
@icontract.ensure(lambda result, quantity: sum(result[1]) == quantity)
def algorithm_transfer(
    request, category: Category, quantity: int, x: int, y: int
):
    lista_products = list(
        Product.objects.all().filter(category=category)
    )  # Prodotti filtrati per categoria

    list_id_pharm_usate = []
    list_quantity_pharm_usate = []

    while int(quantity) > 0:
        if len(lista_products) == 0:
            raise Exception(
                "Non ci sono abbastanza prodotti"
            )  # In transfer() c'è un controllo precedente

        quintupla = find_greedy(
            lista_products, x, y
        )  # Chiamata findGreedy() a ogni iterazione

        # Il cliente si è spostato presso la farmacia (nuova posizione)
        x = quintupla[2]
        y = quintupla[3]

        list_id_pharm_usate.append(quintupla[0])

        if int(quantity) > quintupla[1]:
            list_quantity_pharm_usate.append(quintupla[1])
        else:
            list_quantity_pharm_usate.append(
                quantity
            )  # Ultima farmacia ne prende solo una parte

        quantity = (
            int(quantity) - quintupla[1]
        )  # Decremento la quantità richiesta

        # Popping (Escludere farmacia già scelta)
        lista_products_poppata = []
        i = 0

        for p in lista_products:
            if i != quintupla[4]:
                lista_products_poppata.append(p)
            i += 1
        # END FOR
        lista_products = lista_products_poppata

    # END WHILE

    doppia = [list_id_pharm_usate, list_quantity_pharm_usate]
    return doppia


@icontract.require(
    lambda lista_products: len(lista_products) > 0,
    "listaProducts must not be empty",
)
@icontract.require(lambda x: 0 <= x <= 100, "coordinate 0 <= x <= 100")
@icontract.require(lambda y: 0 <= y <= 100, "coordinate 0 <= y <= 100")
@icontract.ensure(
    lambda result: Pharmacy.objects.filter(id=result[0]).count() >= 1
)
@icontract.ensure(lambda result: result[1] >= 0)
@icontract.ensure(lambda result: 0 <= result[2] <= 100)
@icontract.ensure(lambda result: 0 <= result[3] <= 100)
def find_greedy(lista_products, x: int, y: int):
    scelta_golosa = []  # Vettore pesi

    # Pesiamo quantità disponibile e distanza
    for prod in lista_products:
        distanza_pitagora = (x - prod.pharmacy.x) * (x - prod.pharmacy.x) + (
            y - prod.pharmacy.y
        ) * (y - prod.pharmacy.y)

        # Stessa posizione della farmacia
        if distanza_pitagora == 0:
            distanza_pitagora = 0.01

        weigth = float(prod.quantity) / sqrt(distanza_pitagora)
        scelta_golosa.append(weigth)
    # END FOR

    # Massimizziamo il peso
    id_pharm_scelta = 0
    quantity_scelta = 0
    x_scelto = 0
    y_scelto = 0
    indice_scelto = 0

    i = 0

    peso_scelta = scelta_golosa[0]

    for prod in lista_products:
        if i == 0:  # Inizializza con il primo prodotto
            peso_scelta = scelta_golosa[i]

            id_pharm_scelta = prod.pharmacy.id
            quantity_scelta = prod.quantity
            x_scelto = prod.pharmacy.x
            y_scelto = prod.pharmacy.y
            indice_scelto = i
        elif scelta_golosa[i] > peso_scelta:
            peso_scelta = scelta_golosa[
                i
            ]  # Sovrascrivo il massimo massimo peso

            id_pharm_scelta = prod.pharmacy.id
            quantity_scelta = prod.quantity
            x_scelto = prod.pharmacy.x
            y_scelto = prod.pharmacy.y
            indice_scelto = i

        i += 1  # Passo al prossimo prodotto

    # END FOR

    quintupla = [
        id_pharm_scelta,
        quantity_scelta,
        x_scelto,
        y_scelto,
        indice_scelto,
    ]

    return quintupla
