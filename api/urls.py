from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

#router.register("basketitems",views.BasketItemViewSet,basename="basketitems")
#router.register("basket",views.BasketView,basename="basket")

urlpatterns=[

    path("register/",views.UserCreationView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path("categorycreate/",views.CategoryCreateView.as_view()),
    path("categorylist/",views.CategoryListView.as_view()),
    path("category/<int:pk>/",views.CategoryUpdateRetriveDeleteView.as_view()),
    path("brandcreate/",views.BrandCreateView.as_view()),
    path("brandlist/",views.BrandListView.as_view()),
    path("brand/<int:pk>/",views.BrandUpdateRetriveDeleteView.as_view()),
    path("productcreate/",views.ProductCreateView.as_view()),
    path("productlist/",views.ProductListView.as_view()),
    path("product/<int:pk>/",views.ProductUpdateRetriveDeleteView.as_view()),
    path("basket/",views.BasketView.as_view()),
    path("basketname/",views.BasketNameView.as_view()),



]+router.urls