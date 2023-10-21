from django.urls import path
from django.urls import re_path as url
from payment.views import *
#Example
urlpatterns = [
    path('cardstories', PaymentCardStoreList.as_view()),
    path('cardstore/<int:id>', PaymentCardStoreChange.as_view()),

    path('payment-3dsinit', Payment3DInit.as_view()),
    path('payment-3dpayment',Payment3DComplete.as_view()),
]
