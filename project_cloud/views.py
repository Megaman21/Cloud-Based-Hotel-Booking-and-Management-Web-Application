from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
# from megamaninn.forms import SignUpForm
from megamaninn.models import Review, Room, Type, Booking
from datetime import date
import time


def index(request):
    template = loader.get_template('test.html')
    context = {

    }

    return HttpResponse(template.render(context, request))


def loginpage(request):
    if request.method == "GET":
        template = loader.get_template('login.html')
        context = {

        }
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            # return render(request, 'homepage.html')
            return redirect('home')
        else:
            return render(request, 'login.html')

    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template('homepage.html')
    context = {

    }

    return HttpResponse(template.render(context, request))


@login_required
def editpage(request):
    # template = loader.get_template('edit_profile.html')
    # context = {
    #
    # }
    #
    # return HttpResponse(template.render(context, request))
    if request.method == "GET":
        user = request.user
        return render(request, 'edit_profile.html')
    if request.method == "POST":
        # user=request.user
        user = request.user
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        image = request.FILES.get('image')
        if image is not None:
            user.profile.profile_pic = image
        if password is not None and password!="":
            user.set_password(password)
        user.first_name=firstname
        user.last_name=lastname
        user.email=email
        # user.profile.profile_pic=image
        # user.set_password(password)
        user.save()
        return redirect('profilepage')


def signuppage(request):
    if request.method == "GET":
        template = loader.get_template('signup.html')
        context = {

        }

        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES.get('image')
        username = email

        firstname = name.strip().split(' ')[0]
        lastname = ' '.join((name + ' ').split(' ')[1:]).strip()

        if username and password:
            user, created = User.objects.get_or_create(username=username, email=email, first_name=firstname,
                                                       last_name=lastname)

            if created:
             user.set_password(password)
             user.profile.profile_pic=image
             user.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'signup.html')


@login_required
def bookpage(request):

    if request.method=="GET":
     template = loader.get_template('booking.html')
     context = {

     }

     return HttpResponse(template.render(context, request))
    else:
        available_rooms=Room.objects.all().filter(available=True)
        checkin=request.POST['checkin_date']
        checkout=request.POST['checkout_date']
        print(checkin)
        x1, y1, z1 = checkin.split('-')
        x2, y2, z2 = checkout.split('-')
        f_date = date(int(x1),int(y1),int(z1))
        l_date = date(int(x2),int(y2),int(z2))
        delta = l_date - f_date
        days=delta.days
        roomtypes = Type.objects.all()
        images1 = []
        images2 = []
        price=[]


        for room in available_rooms:
            images1.append(room.type.images_set.first())
            images2.append(room.type.images_set.all()[0])
            price.append(room.type.price*days)
        rooms_data = zip(available_rooms,images1,images2,price)
        return render(request, 'searchresults.html',
                      {'rooms_data': rooms_data,'check_in':checkin,'check_out':checkout,'Days':days})



        # print(days)

@login_required
def reviewpage(request):
    # template = loader.get_template('review.htmls')
    # context = {
    #
    # }
    #
    # return HttpResponse(template.render(context, request))
    # reviews_all=Review.objects.all()
    user = request.user
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST['rating']
        description = request.POST['message']
        reviewx = Review(user_id=user, review=description, rating=rating)
        reviewx.save()
        return redirect('reviewpage')
    # if request.user.is_authenticated:
    else:
        reviews_all = Review.objects.all()
        return render(request, 'review.html',
                      {'reviews_all': reviews_all})

def bookroom(request):

    user=request.user
    id=request.POST['roomid']
    days = request.POST['days']
    checkin = request.POST['checkin']
    checkout = request.POST['checkout']
    x1, y1, z1 = checkin.split('-')
    x2, y2, z2 = checkout.split('-')
    f_date = date(int(x1), int(y1), int(z1))
    l_date = date(int(x2), int(y2), int(z2))
    # id = request.POST['roomid']
    room=Room.objects.get(room_no=id)
    p=room.type.price
    price=int(days)*p
    booking=Booking(start_date=f_date,end_date=l_date,room_no=room,user_id=user,price=price)
    booking.save()
    room.available=False
    room.save()
    return redirect('home')

# def doregister(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#
#         form.save()
#         return redirect('login.html')
#         # else:
#         #     form = SignUpForm()
#         #     arg = {'forms': form}
#         #     return render(request, 'signup.html', arg)
#     else:
#         form = SignUpForm()
#         args = {'forms': form}
#         return render(request, 'signup.html', args)
