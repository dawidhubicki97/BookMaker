"""bukmacher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url


from account.views import(
    
    customer_profile_view,
    logout_view,
    login_view,
)
from strona.views import(
    
    home_screen_view,
    
)
from bets.views import(
show_bets_view,
add_bet_view,
show_bets_to_admin,
enter_score,
show_coupons_view,
show_bets_view_category,
    )
from cart.views import(
    add_to_cart,
    add_coupon_view
    )
from pdfapp.views import(
GeneratePdf,
    )
urlpatterns = [
    path('', show_bets_view,name="home"),
    path('register/', customer_profile_view,name="register"),
    path('logout/', logout_view,name="logout"),
    path('admin/', admin.site.urls),
    path('login/', login_view,name="login"),
    path('addbet/', add_bet_view,name="addbet"),
    url(r'^add-to-cart/(?P<betid>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    path('addcoupon/', add_coupon_view,name="addcoupon"),
    path('betscores/', show_bets_to_admin,name="betscores"),
    url('enterscore/(?P<betid>[-\w]+)/$', enter_score,name="enterscore"),
    url(r'^pdf/$',GeneratePdf.as_view(),name="pdf"),
    path('coupons/', show_coupons_view,name="coupons"),
    url(r'^category/(?P<category>[-\w]+)/$', show_bets_view_category, name="category"),
]
