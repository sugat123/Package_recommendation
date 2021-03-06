from django.shortcuts import render, redirect, \
    get_object_or_404, HttpResponseRedirect, render_to_response
from django.urls import reverse_lazy
from django.views import View
from .models import Package, Search
from django.views.generic import DetailView
from .forms import SignUpForm, ForgotPasswordForm, SearchForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from app.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .forms import NewPassword

from django.db.models import Q

from history.mixins import ObjectViewMixin

from django.contrib import messages

from .recommendation import package_r

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def get_user_id(id):
    return id


class indexView(View):


    template_name = 'index.html'
    form = SignUpForm()


    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('name_search')
        duration = self.request.GET.get('duration_search')
        location = self.request.GET.get('location_search')
        minprice = self.request.GET.get('minprice_search')
        maxprice = self.request.GET.get('maxprice_search')

        searchbox = self.request.GET.get('searchform')
        print(searchbox,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

        if searchbox:
            print('gone to filter')
            return FilterPage().post(request)

        if request.user.id is not None:
            recommended_rating = package_r.rec_list(request.user.id)
            recommended_history = package_r.rec_list_history(request.user.id)

        packagelist = Package.objects.all()

        #ZERO
        if (not name) and (not duration) and (not location) and not (maxprice and minprice):
            print('all none')
           # return Package.objects.all()

        #ONE
        elif not name and not duration and not location and (maxprice and minprice):
            print('only maxprice and minprice')
            packagelist = Package.objects.filter(Q(price__gt = minprice), Q(price__lt = maxprice))
            #return packagelist

        #TWO
        elif not name and not duration and location and not (maxprice and minprice):
            print('only location')
            packagelist = Package.objects.filter(Q(location__icontains=location))
            #return packagelist

        #THREE
        elif not name and not duration and location and (maxprice and minprice):
            print('location and price')
            packagelist = Package.objects.filter(Q(location__icontains=location), Q(price__gt = minprice), Q(price__lt = maxprice))
            #return packagelist

        #FOUR
        elif not name and duration and not location and not (maxprice and minprice):
            print('only duration')
            packagelist = Package.objects.filter(Q(duration__icontains=duration))
            #return packagelist

        #FIVE
        elif not name and duration and not location and (maxprice and minprice):
            print('duration and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(price__gt = minprice), Q(price__lt = maxprice))
            #return packagelist

        #SIX
        elif not name and duration and location and not (maxprice and minprice):
            print('duration and location')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location))
            #return packagelist

        #SEVEN
        elif not name and duration and location and (maxprice and minprice):
            print('duration and location and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            #return packagelist

        #EIGHT
        elif name and not duration and not location and not (maxprice and minprice):
            print('only name')
            packagelist = Package.objects.filter(Q(name__contains=name))
            #return packagelist

        #NINE
        elif name and not duration and not location and (maxprice and minprice):
            print('name and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(price__gt=minprice), Q(price__lt=maxprice))
            #return packagelist

        #TEN
        elif name and not duration and location and not (minprice and minprice):
            print('name and location')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location))
            #return packagelist

        #ELEVEN
        elif name and not duration and location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            #return packagelist

        #TWELVE
        elif name and duration and not location and not (minprice and maxprice):
            print('name and duration')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration))
            #return packagelist

        #THIRTEEN
        elif name and duration and not location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
           # return packagelist

        #FOURTEEN
        elif name and duration and location and not (maxprice and maxprice):
            print('name and duration and location')
            packagelist = Package.objects.filter(Q(name__contains=name),Q(duration__icontains=duration),
                                                 Q(location__icontains=location))
            #return packagelist

        #FIFTEEN
        elif name and duration and location and (maxprice and minprice):
            print('name and duration and location and price')
            packagelist = Package.objects.filter(Q(name__contains=name),Q(duration__icontains=duration),
                                                 Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            #return packagelist


        try:
            paginator = Paginator(packagelist, 9)
            page = request.GET.get('page')
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)


        context = {

            'page_obj': items,
            'form': self.form,


        }

        if request.user.id is not None:
            context.update({'recommended' : Package.objects.filter(Q(id__in= recommended_rating)),
                            'recommended_history': Package.objects.filter(Q(id__in=recommended_history))})

        return render(request, self.template_name, context)


    def post(self, request):
        print("post method called")
        form = SignUpForm(request.POST)
        searchform = SearchForm(request.POST)
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



class FilterPage(View):
    template_name = 'filterpage.html'
    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('searchform')
        print(type(name))
        object_list = Package.objects.filter(Q(name__icontains=name))

        if name:
            try:
                # search = Search.objects.create(search_text = name)
                # search.save()
                paginator = Paginator(object_list, 9)
                page = request.GET.get('page')
                items = paginator.page(page)

            except PageNotAnInteger:
                items = paginator.page(1)
            context={
                'page_obj':items
            }
        else:
            try:
                last_search = Search.objects.all().order_by('-pk')
                print(last_search)
                object_list = Package.objects.filter(Q(name__icontains=last_search))
                paginator = Paginator(object_list, 9)
                page = request.GET.get('page')
                items = paginator.page(page)

            except PageNotAnInteger:
                items = paginator.page(1)
            context = {
                'page_obj': items
            }


        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('received post in filter')
        name = self.request.POST.get('searchform')
        print(name,'this is frm filter page')
        object_list = Package.objects.all()
        context = {'page_obj':object_list}
        print('from post')
        return render(request, self.template_name, context)





class packageDetail(ObjectViewMixin, DetailView):
    model = Package
    template_name = 'detail.html'
    pk_url_kwarg = 'pk'


    def get(self, request, *args, **kwargs):
        rating = self.request.GET.get('rating')
        id = kwargs['pk']

        if rating is not None:
            obj = Package.objects.get(id=id)
            obj.user_rating(request.user.id, rating)

        else:
            obj = Package.objects.get(id=id)
            return render(request, self.template_name, {'object': obj})

        return render(request, self.template_name , {'object': obj})


class CustomSearch(View):
    template_name = 'customfilter.html'

    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('name_search')
        duration = self.request.GET.get('duration_search')
        location = self.request.GET.get('location_search')
        minprice = self.request.GET.get('minprice_search')
        maxprice = self.request.GET.get('maxprice_search')


        print(name, 'this is from customsearch')


        if request.user.id is not None:
            recommended_rating = package_r.rec_list(request.user.id)
            recommended_history = package_r.rec_list_history(request.user.id)

        packagelist = Package.objects.all()

        # ZERO
        if (not name) and (not duration) and (not location) and not (maxprice and minprice):
            print('all none')
        # return Package.objects.all()

        # ONE
        elif not name and not duration and not location and (maxprice and minprice):
            print('only maxprice and minprice')
            packagelist = Package.objects.filter(Q(price__gt=minprice), Q(price__lt=maxprice))
            # return packagelist

        # TWO
        elif not name and not duration and location and not (maxprice and minprice):
            print('only location')
            packagelist = Package.objects.filter(Q(location__icontains=location))
            # return packagelist

        # THREE
        elif not name and not duration and location and (maxprice and minprice):
            print('location and price')
            packagelist = Package.objects.filter(Q(location__icontains=location), Q(price__gt=minprice),
                                                 Q(price__lt=maxprice))
            # return packagelist

        # FOUR
        elif not name and duration and not location and not (maxprice and minprice):
            print('only duration')
            packagelist = Package.objects.filter(Q(duration__icontains=duration))
            # return packagelist

        # FIVE
        elif not name and duration and not location and (maxprice and minprice):
            print('duration and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(price__gt=minprice),
                                                 Q(price__lt=maxprice))
            # return packagelist

        # SIX
        elif not name and duration and location and not (maxprice and minprice):
            print('duration and location')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location))
            # return packagelist

        # SEVEN
        elif not name and duration and location and (maxprice and minprice):
            print('duration and location and price')
            packagelist = Package.objects.filter(Q(duration__icontains=duration), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            # return packagelist

        # EIGHT
        elif name and not duration and not location and not (maxprice and minprice):
            print('only name')
            packagelist = Package.objects.filter(Q(name__contains=name))
            # return packagelist

        # NINE
        elif name and not duration and not location and (maxprice and minprice):
            print('name and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(price__gt=minprice), Q(price__lt=maxprice))
            # return packagelist

        # TEN
        elif name and not duration and location and not (minprice and minprice):
            print('name and location')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location))
            # return packagelist

        # ELEVEN
        elif name and not duration and location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            # return packagelist

        # TWELVE
        elif name and duration and not location and not (minprice and maxprice):
            print('name and duration')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration))
            # return packagelist

        # THIRTEEN
        elif name and duration and not location and (minprice and maxprice):
            print('name and duration and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
        # return packagelist

        # FOURTEEN
        elif name and duration and location and not (maxprice and maxprice):
            print('name and duration and location')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration),
                                                 Q(location__icontains=location))
            # return packagelist

        # FIFTEEN
        elif name and duration and location and (maxprice and minprice):
            print('name and duration and location and price')
            packagelist = Package.objects.filter(Q(name__contains=name), Q(duration__icontains=duration),
                                                 Q(location__icontains=location),
                                                 Q(price__gt=minprice), Q(price__lt=maxprice))
            # return packagelist

        try:
            paginator = Paginator(packagelist, 9)
            page = request.GET.get('page')
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)

        context = {

            'page_obj': items,


        }

        if request.user.id is not None:
            context.update({'recommended': Package.objects.filter(Q(id__in=recommended_rating)),
                            'recommended_history': Package.objects.filter(Q(id__in=recommended_history))})

        return render(request, self.template_name, context)


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
            messages.add_message(request, messages.WARNING, 'Username or Password Invalid. Please try again !!')
            template_name = 'loginerror.html'
            return render(request, template_name)





class logoutView(View):
    #success_url = reverse_lazy('app:index')

    template_name  ='loginerror.html'
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.INFO, 'Please login to continue...')
        return render(request, self.template_name)






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



def Like(request):
    item = get_object_or_404(Package, id = request.POST.get('like'))
    item.like.add(request.user.id)
    return HttpResponseRedirect(item.get_absoulte_url())



class LoginError(View):
    def get(self, request):
        messages.add_message(request, messages.ERROR, 'Username or Passoword Invalid !!')
        template_name = 'loginerror.html'
        return render(request, template_name)



def Search(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.POST['search_text']
            products = Package.objects.filter(name__contains=search_text)[:5]
        else:
            products = []
        return render_to_response('search.html', {'products' : products})



def Search_detail(request,package_id):
    objects = Package.objects.filter(id=package_id)
    return render(request,'Search_detail.html',{'objects':objects})




