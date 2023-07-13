from django.shortcuts import render, redirect, HttpResponse
from .models import Crackers, carosel, similarCrackers,CartItem,Address,Orders
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


from django.shortcuts import render
from django.core.mail import send_mail

def home(request):
    crackers = Crackers.objects.all()
    slide = carosel.objects.all()
    print(crackers)

    if request.user.is_authenticated and not request.session.get('welcome_email_sent', False):
        user = request.user.username
        email = request.user.email
        msg = "Welcome to firecrackers!"
        send_mail("Hi " + user, msg, 'your_email@gmail.com', [email])
        request.session['welcome_email_sent'] = True

    print(crackers)
    if request.user.is_staff:
        yes = "yes"
        return render(request, "home.html", {"crackers": crackers, "yes": yes})

    return render(request, "home.html", {"crackers": crackers, "slide": slide})

def order(request):
    user=request.user.username
    orderss=Orders.objects.filter(username=user)
    return render(request, 'order.html',{"order":orderss})
def productselect(request, productselect):
    if similarCrackers.objects.filter(name__name=productselect).exists():
        obj = similarCrackers.objects.filter(name__name=productselect)
        print(obj)
        return render(request, "productlist.html", {"productlist": obj})
    else:
        return HttpResponse("<center><h1>NO PRODUCTS</h1></center>")
    
def similarcrackers(request):
    crackers = Crackers.objects.all()
    li = [cracker.name for cracker in crackers]
    if request.method == 'POST':
        name = request.POST.get("cracker_type")
        image = request.FILES.get("image")
        similarname = request.POST.get("similar_name")
        actual_price = request.POST.get("actual_price")
        discount_price = request.POST.get("discount_price")
        content = request.POST.get("content")
        
        if similarCrackers.objects.filter(similarname=similarname).exists():
            error_message = "Similar cracker with the same name already exists."
            return render(request, "similarcrackers.html", {"error_message": error_message, "obj": li})
        else:
            cracker = Crackers.objects.get(name=name)
            crac = similarCrackers(name=cracker, image=image, similarname=similarname, actual_price=actual_price, discount_price=discount_price, content=content)
            crac.save()
            success = "Successfully added."
            return render(request, "similarcrackersupload.html", {"obj": li, "success": success})

    return render(request, "similarcrackersupload.html", {"obj": li})



def admins(request):
    return render(request,"admin.html")
def bannerupdate(request):
    if request.method == 'POST':
        for key in request.FILES:
            image = request.FILES[key]
            carosel_obj = carosel.objects.get(id=key)
            carosel_obj.slideimage = image
            carosel_obj.save()
        return redirect('bannerupdate')  # Redirect to the same page after updating the images

    obj=carosel.objects.all()
    return render(request,"bannerupdate.html",{"banners":obj})
def uploadcrackers(request):
    obj=Crackers.objects.all()
    if request.method == 'POST':
        name = request.POST.get("crackerName")
        image = request.FILES.get("crackerImage")
        
        if Crackers.objects.filter(name=name).exists():
            error_message = "Cracker with the same name already exists."
            return render(request, "crakersupload.html", {"error_message": error_message})

        cracker = Crackers(name=name, image=image)
        cracker.save()

    crackers = Crackers.objects.all()
    return render(request, "crakersupload.html", {"cracker": crackers})

def logout_view(request):
    logout(request)
    return redirect('home')

# ###############################################   ADD TO CART###########################
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_discount = request.POST.get('product_discount')
        image = request.POST.get('image')
        image1=image[7:]
# Slicing the image value

        print("****")
        print(image1)
        username=request.POST.get('username')

        # Create a new cart item instance
        cart_item = CartItem(
            product_id=product_id,
            product_name=product_name,
            product_price=product_price,
            product_discount=product_discount,
            image=image1,
            username=username
        )

        # Save the cart item to the database or session, depending on your implementation
        cart_item.save()

        return redirect('mycart')  # Redirect to the cart page

    return redirect('home')

def mycart_view(request):
    user = request.user.username
    id = request.user.id
    print(user)

    context = {}  # Initialize the context variable

    if CartItem.objects.filter(username=user).exists():
        obj = CartItem.objects.filter(username=user)
        add = Address.objects.filter(User=user)
        context['cart_items'] = obj
        context['add'] = add
        return render(request, 'my-cart.html', context)
    elif Address.objects.filter(User=user).exists():
        add = Address.objects.filter(User=user)
        context['add'] = add
        return render(request, 'my-cart.html', context)
    else:
        error = "NO PRODUCT"
        return HttpResponse("<center><h1>NO PRODUCTS</h1></center>")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Address !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def address(request):
    user=request.user.username
    if request.method == 'POST':
        
        name = request.POST.get('name')
        state = request.POST.get('state')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')

        # Create a new Contact object
        contact = Address(
            name=name,
            state=state,
            email=email,
            whatsapp=whatsapp,
            mobile=mobile,
            address=address,
            landmark=landmark,
            pincode=pincode,
            User=user
        )
        contact.save()
        return redirect("mycart")
        # Redirect to a success page or do further processing

    return render(request, 'address.html')



def confirm_order(request):
    user = request.user.username
    

    try:
        address = Address.objects.get(User=user)
    except Address.DoesNotExist:
        # Handle the case where the address does not exist for the user
        return HttpResponse("Address not found for the user.")

    if request.method == 'POST':
        user=request.user.username
        quantity = request.POST.get('quantity')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_discount = request.POST.get('product_discount')
        image = request.POST.get('image')
        total_amount = request.POST.get("total")
        image1=image[7:]
            # Create a new order in the Orders model
        if product_name:
            order = Orders(
            username=user,
            quantitity=quantity,
            product_name=product_name,
            product_price=product_price,
            product_discount=product_discount,
            image=image1,
            )
            order.save()

            # Delete the cart item
            CartItem.objects.filter(product_name=product_name).delete()
            add = Address.objects.get(User=user)
            email=add.email
            context = {
                'user': user,
                'product_name': product_name,
                'total_amount': total_amount,
                'address': address,
            }
            email_content = render_to_string('email_templates/order_conformation.html', context)
            send_mail(
                subject='Order Confirmation',
                message='',
                html_message=email_content,
                from_email='your_email@gmail.com',
                recipient_list=[email]
            )
            orderss=Orders.objects.filter(username=user)
            return render(request, 'order.html',{"order":orderss})
        else:
            return HttpResponse("Invalid POST data")

    return HttpResponse("Method not allowed")

# pdf
