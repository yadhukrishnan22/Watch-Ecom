"""
URL configuration for WatchEComm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from myapp import views

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.SignUpView.as_view(), name='sign-up' ),
    path('login/', views.SignInView.as_view(), name='sign-in'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('profile/<int:pk>/change/', views.UserProfileUpdateView.as_view(), name='profile-edit'),
    path('logout/', views.SignOutView.as_view(), name='sign-out'),
    path('product/<int:pk>/details/', views.ProductDetailsView.as_view(), name='product-details'),
    path('product/<int:pk>/varient/', views.ProductVarientView.as_view(), name='product-varient'),
    path('cart/<int:pk>/', views.AddToCart.as_view(), name='cart'),
    path('cart/list/', views.CartListView.as_view(), name='cart-list'),
    path('cart/<int:pk>/delete/', views.CartItemsDeleteView.as_view(), name='cartitem-delete'),
    path('delivery/', views.DeliveryDetailsView.as_view(), name='delivery-details'),
    path('checkout/', views.CheckOutView.as_view(), name='payment'),
    path('payment/verification/', views.PaymentVerificationView.as_view(), name = 'payment-verification'),
    path('order/summary/', views.MyPurchaseView.as_view(), name = 'purchase-view'),
    path('', views.PublicIndexView.as_view(), name='publicindex'),
    path('public/product/<int:pk>/details/', views.PublicProductDetailsView.as_view(), name='publicproduct-details'),
    path('public/product/<int:pk>/varient/', views.PublicProductVarientView.as_view(), name='publicproduct-varient'),
    path('test/', views.TestView.as_view()),
    path('product/reviews/<int:pk>/add/', views.ReviewCreateView.as_view(), name='reviews'),
    path('order/summary/pending/', views.MyPendingPaymentsView.as_view(), name='order-pending-payements')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
