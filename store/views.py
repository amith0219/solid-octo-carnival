from django.shortcuts import render,get_object_or_404,redirect
from store.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from .forms import CommentForm,CartForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.urls import reverse,reverse_lazy
# Create your views here.


def store(request):
     products = Product.objects.all()
     category = Category.objects.all()
     context = {'products':products, 'category':category}
     return render(request, 'store/store.html', context)


def index2(request, id):
     cat = Category.objects.all()
     post = Product.objects.filter(category_id = id)
     return render(request,"store/store.html",context = {"products":post, "category":cat})



def cart(request):
     curent_user = request.user
     shopcart = Cart.objects.filter(user_id=curent_user.id)
     total=0
     for rs in shopcart:
          total += rs.product.price * rs.quantity
     context = {'shopcart': shopcart,'total': total,}
     return render(request, 'store/cart.html', context)




# class ProductDetailView(DetailView):
#     model = Product
#     queryset = Product.objects.all()
#     template_name = "store/product.html"

def product_detail(request, id):
     category = Category.objects.all()
     product = Product.objects.get(pk=id)
     comments = Comment.objects.filter(product_id=id,status='New')
     context = {'product':product, 'category':category,'comments':comments,}
     return render(request,'store/product.html',context)



def checkout(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = OrderItem.objects.get_or_create(user=customer, ordered=False)
          items = order.orderitem_set.all()
     else:
          items = []
          order = {"get_cart_total":0}

     context = {'items':items, 'order':order}
     return render(request, 'store/checkout.html', context)




def register(request):    
     if request.method == 'POST':
         form = UserRegisterForm(request.POST)
         if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              messages.success(request, f'Your account has been created! You are now able to log in')
              return redirect('login')
     else:
          form = UserRegisterForm()
     return render(request, 'registration/register.html', {'form': form})



def addcomment(request, id):
     url = request.META.get('HTTP_REFERER')
     if request.method == 'POST':
          form = CommentForm(request.POST)
          if form.is_valid():
               data = Comment()
               data.subject = form.cleaned_data['subject']
               data.comment = form.cleaned_data['comment']
               data.rate = form.cleaned_data['rate']
               data.product_id=id
               current_user = request.user
               data.user_id=current_user.id 
               data.save()
               messages.success(request, "Your Ratings has been submitted!")
               return HttpResponseRedirect(url)
     return HttpResponseRedirect(url)


@login_required(login_url="login")
def addtocart(request,id):
     url = request.META.get('HTTP_REFERER')
     current_user = request.user
     product = Product.objects.get(pk=id)

     checkinproduct = Cart.objects.filter(product_id=id, user_id=current_user.id)
     if checkinproduct:
          control = 1
     else:
          control = 0
     if request.method == 'POST':
          form = CartForm(request.POST)
          if form.is_valid():
               if control==1:
                    data = Cart.objects.get(product_id=id, user_id=current_user.id)
                    data.quantity += form.cleaned_data['quantity']
                    data.save()
               else:
                    data = Cart()
                    data.user_id = current_user.id
                    data.product_id = id
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
          messages.success(request, "Product is added to your Cart!!")
          return HttpResponseRedirect(url)
     else:
          if control == 1:
               data = Cart.objects.get(product_id=id, user_id=current_user.id)
               data.quantity += 1
               data.save()
          else:
               data = Cart()
               data.user_id = current_user.id
               data.product_id = id
               data.quantity = 1
               data.save()
          messages.success(request, "Product is added to your Cart!!")
          return HttpResponseRedirect(url)