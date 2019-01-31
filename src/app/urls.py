from django.conf.urls import url
from .views import indexView, packageDetail, loginView, resetPassword,\
    activate, logoutView, forgotPasswordFormView, Like, LoginError, Search_detail, Search
from history.views import HistoryView, DeleteHistory


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
    url('history/', HistoryView.as_view(), name= 'history'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteHistory.as_view(), name= 'deletehistory'),

    url(r'^like/$', Like, name='like_item_detail'),

    url(r'^login/error/$', LoginError.as_view(), name='loginerror'),

    url(r'^search/$', Search, name='search'),
    url(r'^search/(?P<package_id>[0-9]+)/$', Search_detail),

   # url(r'^test/$', test.as_view(), name = 'test'),

]
