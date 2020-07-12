from django.urls import path,include
from store.views import store,checkout,product_detail,register,index2
from store.views import addcomment,addtocart,cart
from django.contrib.auth.views import LoginView

urlpatterns = [
        #Leave as empty string for base url
	path('', store, name="store"),
	path('product/addcomment/<int:id>', addcomment, name='addcomment'),
	path('addtocart/<int:id>', addtocart, name="add-to-cart"),
	path("register",register,name="register"),
	path("login",LoginView.as_view(template_name="registration/login.html"), name='login'),
	path('category/<int:id>',index2,name = "category"),
	path('product/<int:id>/', product_detail, name="product"),
	path('cart/', cart, name="cart"),
	path("",include("django.contrib.auth.urls")),
]