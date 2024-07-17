from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework import authentication,permissions

from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView

from api.serializers import UserSerializer,CategorySerializers,BrandSerializers,ProductSerializers,BasketItemSerializers,BasketSerializers

from store.models import Category,Brand,Product,BasketItems,Basket

from rest_framework.viewsets import ModelViewSet

from api.permissions import OwnerOnly


class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)

class  CategoryCreateView(CreateAPIView):

    serializer_class=CategorySerializers

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]

class CategoryListView(ListAPIView):

    serializer_class=CategorySerializers

    queryset=Category.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class CategoryUpdateRetriveDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class=CategorySerializers

    queryset=Category.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]


class  BrandCreateView(CreateAPIView):

    serializer_class=BrandSerializers

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]

class BrandListView(ListAPIView):

    serializer_class=BrandSerializers

    queryset=Brand.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class BrandUpdateRetriveDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class=BrandSerializers

    queryset=Brand.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]

class  ProductCreateView(CreateAPIView):

    serializer_class=ProductSerializers

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]

class ProductListView(ListAPIView):

    serializer_class=ProductSerializers

    queryset=Product.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]


class ProductUpdateRetriveDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class=ProductSerializers

    queryset=Product.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

class BasketNameView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        serializer_instance=BasketSerializers(data=request.data)  # deserialization

        if serializer_instance.is_valid():

            serializer_instance.save(instance=self.request.user)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)



class BasketView(APIView):

     
     authentication_classes=[authentication.TokenAuthentication]

     permission_classes=[permissions.IsAuthenticated]

     def get(self,request,*args,**kwargs):
         
         basket_obj=BasketItems.objects.filter(basket_object=request.user)
         
         qs=BasketItems.objects.all(basket_obj)

         serializer_instance=BasketItemSerializers(qs,many=True) 

         return Response(data=serializer_instance.data)



       






