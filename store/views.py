from django.shortcuts import render,redirect

from store.forms import SignUpForm,SignInForm

from django.contrib.auth.models import User

from store.models import Product,Brand,Size,Basket,BasketItems,Colour,AgeBetween,Order,Category

from django.contrib.auth import authenticate,login,logout

from django.views.generic import View

# Create your views here.



class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("account created")

            return redirect("register")
        
        return render(request,"register.html",{"form":form_instance})
    
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"signin.html",{"form":form_instance}) 
       
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)   

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            password=data.get("password")

            user_object=authenticate(request,username=uname,password=password)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("login success")

                return redirect("index")

        print("failed to login")       
        return render(request,"signin.html",{"form":form_instance}) 
    

class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"index.html",{"data":qs})
    

class ProductDetailsView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"product_details.html",{"data":qs})
    
class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        size_name=request.POST.get("size")

        colour_name=request.POST.get("colour")

        age_name=request.POST.get("age-group")

        qty=request.POST.get("qty")

        print(size_name,colour_name,qty,product_obj)


        basket_instance=Basket.objects.get(owner=request.user)

        age_object=AgeBetween.objects.get(age_group=age_name)

        size_obj=Size.objects.get(name=size_name)

        colour_obj=Colour.objects.get(name=colour_name)

        BasketItems.objects.create(
            product_object=product_obj,
            basket_object=basket_instance,
            quantity=qty,
            colour_object=colour_obj,
            size_object=size_obj,
            agebetween_object=age_object


        )

        print("cart added succesfully")

        return redirect("cart-summary")

class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})

class BasketItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItems.objects.get(id=id).delete()

        return redirect("cart-summary")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")     

class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    
    
    def post(self,request,*args,**kwargs):

        print(request.user)

        name=request.POST.get("username")

        phone=request.POST.get("phone")

        email=request.POST.get("email")

        address=request.POST.get("address")

        paymentmode=request.POST.get("paymentmode")

        print(name,phone,email,address,paymentmode)

        user_obj=request.user

        basketitems_obj=request.user.cart.cartitems.filter(is_order_placed=False)

        if paymentmode == "cod":

            order_obj=Order.objects.create(
                user_object=user_obj,
                phone=phone,
                email=email,
                delivery_address=address,
                
                )
            
            for bi in basketitems_obj:

                order_obj.basketitems_object.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()


        return redirect("index")

class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order-summary.html",{"data":qs})


class CategoryListView(View):

    def get(self,request,*args,**kwargs):

        categorylist=Category.objects.all()

        return render(request,"base.html",{"catelist":categorylist})
    

#url:localhost:8000/category/{id}/products


class CategoryProductsView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        cate_obj=Category.objects.get(id=id)

        product_obj=Product.objects.filter(category_object=cate_obj)
         

        return render(request,"categorylist.html"  ,{"cateproduct":product_obj})
    
    


