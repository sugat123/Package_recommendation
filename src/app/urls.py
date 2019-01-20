from django.conf.urls import url
from .views import indexView, packageDetail, loginView, resetPassword,\
    activate, logoutView, forgotPasswordFormView


app_name = 'app'
urlpatterns = [
    url(r'^$', indexView.as_view(), name= 'index'),
    url(r'^(?P<pk>\d+)/$', packageDetail.as_view(), name= 'detail'),

    url('login', loginView.as_view(), name = 'login'),
    url(r'^logout/$', logoutView.as_view(), name='logout'),

    url(r'^passwordreset/', forgotPasswordFormView.as_view(), name='pwd_reset'),
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        resetPassword.as_view(), name='reset_password'),
    url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
        name='activate'),

]
# from django.urls import path, include, re_path
# from .views import indexView, packageDetail, login, resetPassword, signup, test, activate
#
