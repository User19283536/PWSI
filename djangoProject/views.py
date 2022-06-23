from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from djangoProject.models import Product, Offers, Order, UserAddresses
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil import parser
from django.core.mail import send_mail

def home_page(request):
    return render(request, 'index.html')



def offers(request):
    queryset = Offers.objects.all()

    context={
        'offers': queryset,
    }
    return render(request, 'discover.html', context)


def ogloszenie(request):

        return render(request, 'ogloszenie.html')


def about(request):
    return render(request, 'about.html')

def kontakt(request):
    return render(request, 'kontakt.html')

def logowanie(request):
    return render(request, 'registration/login.html')

def rejestracja(request):

    return render(request, 'registration/register.html')

def wylogowany(request):
    return render(request, 'registration/logged_out.html')

def zarejestrowany(request):
    konta = User.objects.all()
    first = request.POST.get("first")
    last = request.POST.get("last")
    e_mail = request.POST.get("email")
    uname = request.POST.get("username")
    password = request.POST.get("password")
    city1 = request.POST.get("city")
    street1 = request.POST.get("street")
    number1 = request.POST.get("number")
    zipcode1 = request.POST.get("zipcode")

    try:
        a = konta.get(email=e_mail).email
        return render(request, "index.html")
    except ObjectDoesNotExist:
        user = User.objects.create_user(uname, e_mail, password)
        user.first_name = first
        user.last_name = last
        user.save()

        adress = UserAddresses(
            u_id=user,
            city=city1,
            street=street1,
            number=number1,
            zipcode=zipcode1
        )
        adress.save()

        return render(request, "finalRegistered.html")

def finalZarejestrowany(request):
    return render(request, "registration/registered.html")

def orders(request):
    try:
        o_id = request.GET.get("o_id")
        offer = Offers.objects.all().get(id=o_id)
        address = UserAddresses.objects.all().get(u_id=request.user.id)
        context = {
            "offer": offer,
            "address": address,
        }
    except ObjectDoesNotExist:
        print("Błąd")

    return render(request, 'purchase.html', context)

def ordered(request):

    try:
        p_id = request.POST.get("offer")
        offer = Offers.objects.all().get(id=p_id)
        seller = User.objects.all().get(id=offer.seller_id.id)
        amount = int(request.POST.get("amount"))
        address = UserAddresses.objects.all().get(u_id=request.user.id)
        order = Order(
            o_id = offer,
            date = datetime.now(),
            buyer_id = request.user,
            pieces = amount,
            total = amount*offer.p_id.price,
            city = address.city,
            street = address.street,
            number = address.number,
            zipcode = address.zipcode
        )
        order.save()

        offer.available = offer.available - amount
        offer.save()

        send_mail(
            'Zakupiono twój przedmiot {}'.format(offer.p_id.name, amount),
            'Witaj sprzedawco! \nZamówiono przedmiot {} w łącznej ilości {} sztuk za całkowitą kwotę {} zł.\n'
            'Dane kupującego:\n'
            '{} {} \nul {} {}, {} {}'
            '\nDziękujemy za skorzystanie z naszych usług.\n'.format(offer.p_id.name, amount, amount * offer.p_id.price,
                                                                     request.user.last_name, request.user.first_name,
                                                                     address.street, address.number, address.city,
                                                                     address.zipcode),
            'taiprojekt2022@gmail.com',
            [seller.email],
            fail_silently=False,
        )

    except ObjectDoesNotExist:
        print("Błąd")

    send_mail(
        'Zakupiono przedmiot {} uzytkownika {}'.format(offer.p_id.name, seller.username),
        'Witaj {}!\nWłaśnie zakupiłeś przedmiot {} w łącznej ilości {} sztuk za całkowita kwotę {} zł.\nAdress dostawy:\nul. {} {}, {} {} \nDziękujemy za skorzystanie z naszych usług.\n'.format(
            request.user.first_name, offer.p_id.name, amount, amount * offer.p_id.price, address.street, address.number,
            address.city, address.zipcode),
        'taiprojekt2022@gmail.com',
        [request.user.email],
        fail_silently=False,
    )


    return render(request, "purchased.html")

def konto(request):
    if request.user.is_authenticated:
        uzytkownik = request.user
        adres = UserAddresses.objects.all().get(u_id=uzytkownik.id)
        context = {
            "user": uzytkownik,
            "address": adres
        }
        return render(request, "konto.html", context)
    else:
        return render(request, "index.html")

def zmien(request):
    uzytkownik = User.objects.all().get(id=request.user.id)
    uzytkownik.email = request.POST.get("email")
    uzytkownik.first_name = request.POST.get("first_name")
    uzytkownik.last_name = request.POST.get("last_name")
    uzytkownik.username = request.POST.get("username")
    uzytkownik.save()
    adres = UserAddresses.objects.all().get(u_id=uzytkownik.id)
    adres.city = request.POST.get("city")
    adres.street = request.POST.get("street")
    adres.number = request.POST.get("number")
    adres.zipcode = request.POST.get("zipcode")
    adres.save()
    return render(request, "kontoPotwierdzenie.html")

def offerAdded(request):
    title1 = request.POST.get("title")
    price1 = request.POST.get("price")
    amount1 = request.POST.get("amount")
    description1 = request.POST.get("description")
    path1 = request.POST.get("path")

    item = Product(
        name=title1,
        price=price1,
        description=description1,
        path=path1
    )
    item.save()

    offer = Offers.objects.create(
        p_id=item,
        seller_id=request.user,
        date=datetime.now(),
        available=amount1
    )
    offer.save()

    return render(request, "index.html")