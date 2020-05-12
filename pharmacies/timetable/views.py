import logging
import math
import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework import viewsets

from pharmacies import settings
from pharmacies.permission import IsAdminOrReadOnly
from shop.models import Category, Product, Pharmacy
from timetable.models import Timetable
from timetable.serializer import TimetableSerializer

logger = logging.getLogger("mylogger")


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


def view(request):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    array = [1, 2, 3, 4, 5, 6]
    slots = Timetable.objects.order_by("day", "slot4h")
    return render(
        request,
        "timetable/timetable.html",
        {"slots": slots, "days": days, "array": array},
    )


def calculate(request):
    count = Pharmacy.objects.all().count()

    if not request.user.is_superuser:
        messages.info(
            request,
            "You have to logged as admin in first to calculate the timetable",
        )
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
    elif count < 3:
        messages.error(
            request,
            "Three pharmacies are needed in order to calculate the timetable",
        )
        return redirect("timetable:view_timetable")
    else:
        algorithm_timetable(request)  # Chiamata algorithm_timetable()
        messages.success(request, "Timetable calculated!")
        return redirect("timetable:view_timetable")


def algorithm_timetable(request):
    # Vettori paralleli
    items_farmacie = Pharmacy.objects.all()

    item_slot_min = []

    for f in items_farmacie:
        item_slot_min.append(f.get_slot_4h_min_week())

    summ_slot_min = sum(item_slot_min)

    Timetable.objects.all().delete()  # Svuotare le istanze di Timetable

    if summ_slot_min == 42:  # CASO: SE ABBIAMO ESATTAMENTE 42 SLOT DA RIEMPIRE
        k = list(range(0, 42))
        i = 0
        for farm in items_farmacie:  # Per ogni farmacia
            slotmin = item_slot_min[i]

            for j in range(slotmin):  # Per ogni suo slot
                s = int(random.choice(k))
                insert(s, farm)
                k.remove(s)
            # END FOR
            i = i + 1
        # END FOR
    # END IF

    elif (
        summ_slot_min > 42
    ):  # CASO: SE ABBIAMO PIU DI 42, AVREMO DELLE SOVRAPPOSIZIONI
        i = 0
        contatore = 0
        k = list(range(0, 42))

        for farm in items_farmacie:  # Per ogni farmacia
            slotmin = item_slot_min[i]

            for j in range(slotmin):  # Per ogni suo slot
                if (
                    contatore < 42
                ):  # PRIMA EFFETTUO I RIEMPIMENTI OBBLIGATORI, POI QUELLI PER SOVRAPPOSIZIONI
                    s = int(random.choice(k))
                    insert(s, farm)
                    k.remove(s)
                    contatore = contatore + 1

                else:
                    ctt = 0
                    listrnd = list(range(1, 11))
                    while len(listrnd) > 0 and ctt == 0:

                        p = random.choice(listrnd)
                        if p == 1:
                            number_list = [0, 6, 12, 18, 24, 30, 36]
                            w = 1
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)
                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)
                            listrnd.remove(1)
                        elif p == 2:
                            number_list = [1, 7, 13, 19, 25, 31, 37]
                            w = 2
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)
                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)
                            listrnd.remove(2)

                        elif 3 <= p < 6:
                            number_list = [2, 8, 14, 20, 26, 32, 38]
                            w = 3
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)
                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)
                            listrnd.remove(3)
                            listrnd.remove(4)
                            listrnd.remove(5)

                        elif 6 <= p < 9:
                            number_list = [3, 9, 15, 21, 27, 33, 39]
                            w = 4
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)
                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)
                            listrnd.remove(6)
                            listrnd.remove(7)
                            listrnd.remove(8)

                        elif p == 9:
                            number_list = [4, 10, 16, 22, 28, 34, 40]
                            w = 5
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)
                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)
                            listrnd.remove(9)

                        else:
                            number_list = [5, 11, 17, 23, 29, 35, 41]
                            w = 6
                            ct = 0
                            while ct == 0 and len(number_list) > 0:
                                s = random.choice(number_list)
                                g = calcola_giorno(s)

                                tupla = Timetable.objects.filter(
                                    pharmacy=farm.id, day=g, slot4h=w
                                )
                                if len(tupla) == 0:
                                    ct = 1
                                    insert(s, farm)
                                    ctt = 1
                                number_list.remove(s)

                            listrnd.remove(10)
            # END FOR
            i = i + 1
        # END FOR

    else:  # CASO: SE ABBIAMO MENO DI 42 SLOT, DEVO FORZARE ALCUNE/TUTTE LE FARMACIE A TENERE APERTO PIU DEGLI SLOT MINIMI
        k = list(range(0, 42))

        i = 0
        for farm in items_farmacie:  # Per ogni farmacia
            slotmin = item_slot_min[i]

            for j in range(slotmin):  # Per ogni suo slot
                s = int(random.choice(k))
                insert(s, farm)
                k.remove(s)

            # END FOR
            i = i + 1
        # END FOR

        while len(k) > 0:
            x = random.choice(k)

            if x < 10:
                items_farmacie_ordered = Pharmacy.objects.all().order_by(
                    "-slot4hMinWeek"
                )[0]
                insert(k[0], items_farmacie_ordered)
                k.pop(0)

            elif 10 <= x < 40:
                items_farmacie_ordered = Pharmacy.objects.all().order_by(
                    "-slot4hMinWeek"
                )[1]
                insert(k[0], items_farmacie_ordered)
                k.pop(0)

            else:
                items_farmacie_ordered = Pharmacy.objects.all().order_by(
                    "-slot4hMinWeek"
                )[2]
                insert(k[0], items_farmacie_ordered)
                k.pop(0)
        # END WHILE


def calcola_giorno(p):
    giorno = math.trunc(p // 6) + 1

    # Scelta del giorno della settimana
    if giorno == 1:
        g = "Monday"
    elif giorno == 2:
        g = "Tuesday"
    elif giorno == 3:
        g = "Wednesday"
    elif giorno == 4:
        g = "Thursday"
    elif giorno == 5:
        g = "Friday"
    elif giorno == 6:
        g = "Saturday"
    else:
        g = "Sunday"
    return g


def insert(t, farmacia):
    g = calcola_giorno(t)

    # Scelta dello slot
    if t == 0 or t == 6 or t == 12 or t == 18 or t == 24 or t == 30 or t == 36:
        slot = 1
    elif (
        t == 1 or t == 7 or t == 13 or t == 19 or t == 25 or t == 31 or t == 37
    ):
        slot = 2
    elif (
        t == 2 or t == 8 or t == 14 or t == 20 or t == 26 or t == 32 or t == 38
    ):
        slot = 3
    elif (
        t == 3 or t == 9 or t == 15 or t == 21 or t == 27 or t == 33 or t == 39
    ):
        slot = 4
    elif (
        t == 4
        or t == 10
        or t == 16
        or t == 22
        or t == 28
        or t == 34
        or t == 40
    ):
        slot = 5
    else:
        slot = 6

    t = Pharmacy.objects.get(id=farmacia.id)

    logger.info("Insert in database (Timetable)")
    p = Timetable(day=g, slot4h=slot, pharmacy=t)
    p.save()


"""
API with permissions
"""


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminOrReadOnly]
