from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Package
from django.views.generic import DetailView
from .forms import SignUpForm, ForgotPasswordForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from app.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .forms import NewPassword, FilterForm

from django.views.generic import ListView

from django.contrib import messages

from django.db.models import Q

class indexView(ListView):

    model = Package
    template_name = 'index.html'
    print('in index view right now !!')
    paginate_by = 20


    def get_queryset(self):
        name = self.request.GET.get('name_search')
        duration = self.request.GET.get('duration_search')
        location = self.request.GET.get('location_search')
        minprice = self.request.GET.get('minprice_search')
        maxprice = self.request.GET.get('maxprice_search')

        #ZERO
        if (not name) and (not duration) and (not location) and not (maxprice and minprice):
            print('all none')
            return Package.objects.all()

        #ONE
        elif not name and not duration and not location and (maxprice and minprice):
            print('only maxprice and minprice')
            packagelist = Package.objects.filter(Q(price__gt = minprice), Q(price__lt = maxprice))
            return packagelist

        #TWO
        elif not name and not duration and location and not (maxprice and minprice):
            print('only location')
            packagelist = Package.objects.filter(Q(location__icontains=location))
            return packagelist

        #THREE
        elif not name and not duration and location and (maxprice and minprice):
            print('location and price')
            packagelist = Package.objects.filter(Q(location__icontains=location), Q(price__gt = minprice), Q(price__lt = maxprice))
            return packagelist

        #FOUR
        elif not name and duration and not location and not (maxprice and minprice):
            print('only duration')
            packagelist = Package.objects.filter(Q(duration__icontains=duration))
            return packagelist

        #FIVE
        elif not name and duration and not location and (maxprice and minprice):
            print('duration and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(price__gt = minprice), Q(price__lt = maxprice))
            return packagelist

        #SIX
        elif not name and duration and location and not (maxprice and minprice):
            print('duration and location')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location))
            return packagelist

        #SEVEN
        elif not name and duration and location and (maxprice and minprice):
            print('duration and location and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            return packagelist

        #EIGHT
        elif name and not duration and not location and not (maxprice and minprice):
            print('only name')
            packagelist = Package.objects.filter(Q(name__contains=name))
            return packagelist

        #NINE
        elif name and not duration and not location and (maxprice and minprice):
            print('name and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(price__gt=minprice), Q(price__lt=maxprice))
            return packagelist

        #TEN
        elif name and not duration and location and not (minprice and minprice):
            print('name and location')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location))
            return packagelist

        #ELEVEN
        elif name and not duration and location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            return packagelist

        #TWELVE
        elif name and duration and not location and not (minprice and maxprice):
            print('name and duration')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration))
            return packagelist

        #THIRTEEN
        elif name and duration and not location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            return packagelist

        #FOURTEEN
        elif name and duration and location and not (maxprice and maxprice):
            print('name and duration and location')
            packagelist = Package.objects.filter(Q(name__contains=name),Q(duration__icontains=duration),
                                                 Q(location__icontains=location))
            return packagelist

        #FIFTEEN
        elif name and duration and location and (maxprice and minprice):
            print('name and duration and location and price')
            packagelist = Package.objects.filter(Q(name__contains=name),Q(duration__icontains=duration),
                                                 Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            return packagelist



    def post(self, request):
        print("post method called")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                subject, message, to=[to_email]

            )
            email.send()
            return render(request, 'gmail_confirm.html')
        print('form invalid !!')
        return render(request, 'index.html')




class packageDetail(DetailView):
    model = Package
    template_name = 'detail.html'





class loginView(View):
    success_url = reverse_lazy('app:index')


    def get(self, request):
        return self.http_method_not_allowed(request)


    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            request.session['login_error'] = 'Username and password doesn\'t match'
        return redirect(self.success_url)


class logoutView(View):
    success_url = reverse_lazy('app:index')


    def get(self, request):
        logout(request)
        return redirect(self.success_url)




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'index.html')
    else:
        return render(request, 'account_activation_invalid.html')




class resetPassword(View):

    def get(self, request, uidb64, token):
        form = NewPassword()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):

            return render(request, 'newpasswordcreate.html', {'form': form})
        else:
            return render(request, 'account_activation_invalid.html')


    def post(self, request, uidb64, token):
        form = NewPassword(request.POST)

        if form.is_valid():
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            user.set_password(form.cleaned_data['password1'])
            user.save()
            return render(request, 'success.html')

        else:
            #print(form.errors['__all__'])

            messages.error(
                self.request, 'Password do not match. Please try again')
            return render(request, 'newpasswordcreate.html',{'form': NewPassword()})



class forgotPasswordFormView(View):
    template_name= 'pwdresetform.html'

    def get(self, request, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        userobj = User()
        form = ForgotPasswordForm(request.POST)
        subject = 'Activate Your MySite Account'

        if form.is_valid():
            username_from_form = form.cleaned_data['username']
            to_email = form.cleaned_data['email']
            user = User.objects.get(username=username_from_form)
            primarykey = user.id
            current_site = get_current_site(request)
            subject = 'Passwor Reset !!'
            message = render_to_string('newpasswordlink.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(primarykey)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
        return render(request, 'sendmail.html')



