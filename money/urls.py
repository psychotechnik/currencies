from django.conf.urls import patterns, include, url
from money.views import (CurrencyList, CurrencyCreate, CurrencyDetail,
                         CurrencyDelete, CurrencyUpdate)
from money.views import (TemplateDelete, TemplateUpdate, TemplateDetail,
                         TemplateCreate, TemplateList)
from money.views import (WalletList, WalletCreate, WalletDetail, WalletUpdate,
                         WalletDelete)
from money.views import (TransactionList, TransactionCreate,
                         TransactionDetail, TransactionUpdate,
                         TransactionDelete)

currency_urlpatterns = patterns('',
    url(r'^$', CurrencyList.as_view(), name='list'),
    url(r'^create/$', CurrencyCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CurrencyDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', CurrencyUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', CurrencyDelete.as_view(), name='delete'),
)

template_urlpatterns = patterns('',
    url(r'^$', TemplateList.as_view(), name='list'),
    url(r'^create/$', TemplateCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', TemplateDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', TemplateUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', TemplateDelete.as_view(), name='delete'),
)

transaction_urlpatterns = patterns('',
    url(r'^$', TransactionList.as_view(), name='list'),
    url(r'^create/$', TransactionCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', TransactionDetail.as_view(), name='detail'),
# Transaction has only create and delete methods!!!
#    url(r'^(?P<pk>\d+)/update/$', TransactionUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', TransactionDelete.as_view(), name='delete'),
)

wallet_urlpatterns = patterns('',
    url(r'^$', WalletList.as_view(), name='list'),
    url(r'^create/$', WalletCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', WalletDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', WalletUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', WalletDelete.as_view(), name='delete'),
)

urlpatterns = patterns('',
    url(r'^currency/', include(currency_urlpatterns, namespace='currency')),
    url(r'^template/', include(template_urlpatterns, namespace='template')),
    url(r'^wallet/', include(wallet_urlpatterns, namespace='wallet')),
    url(r'^transaction/', include(transaction_urlpatterns,
        namespace='transaction')),
)
