from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets

from authentication.forms import UserSignupForm, UserSigninForm
from authentication.serializer import UserSerializer
from authentication.tokens import activation_token
from pharmacies import settings
from pharmacies.permission import IsAdmin
from shop.models import Category, Product


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


def signup(req):
    if req.method == "POST":
        form = UserSignupForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            site = get_current_site(req)
            mail_subject = "Confirmation message"
            message = render_to_string('authentication/activate_mail.html', {
                "user": user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            messages.success(req, "Thanks for your registration! A confirmation link has been sent to your mail")
    else:
        form = UserSignupForm()
    return render(req, 'authentication/users_signup.html', {'form': form})


def activate(req, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except(TypeError, ValueError):
        user = None
    if user and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(req, 'Your account activated! Now login')
        return redirect("authentication:login")
    else:
        messages.error(req, "Activation link is invalid")


def signin(request):
    if request.method == "POST":
        form = UserSigninForm(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            redirect_url = request.GET.get('next', 'shop:home')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserSigninForm()
    return render(request, 'authentication/users_signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('authentication:login')


"""
API with permissions
"""


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
