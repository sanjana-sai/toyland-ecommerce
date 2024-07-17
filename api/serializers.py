from rest_framework.serializers import ModelSerializer

from store.models import Category,Brand,Product,BasketItems,Basket

from django.contrib.auth.models import User




class UserSerializer(ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","password","email"]

        read_only=["id"]

    def create(self,validated_data):      #method overridding creating a new  create method for password encrypt

        return User.objects.create_user(**validated_data)
    



class CategorySerializers(ModelSerializer):

    class Meta:

        model=Category

        fields="__all__"

        read_only_fields=[ "id","created_date","updated_date","is_active"]





class ProductSerializers(ModelSerializer):

    #category_object=CategorySerializers.StringRelatedField(read_only=True)

    class Meta:

        model=Product

        fields="__all__"



        read_only_fields=["id","created_date","updated_date","is_active"]


class BrandSerializers(ModelSerializer):

    class Meta:

        model=Brand

        fields="__all__"

        read_only_fields=["id","created_date","updated_date","is_active" ,]

        def create_basket(sender,instance,created,**kwargs):  

            if created:

                    Basket.objects.create(owner=instance)

                

class BasketSerializers(ModelSerializer):

    class Meta:

        model=Basket

        fieldS="__all__"

        
        


class BasketItemSerializers(ModelSerializer):


    class Meta:

        model=BasketItems

        fields="__all__"

        read_only_fields=["id","created_date","updated_date","is_active","is_order_placed"]
