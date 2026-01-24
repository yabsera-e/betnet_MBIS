from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from listing.models import Listing, City, SubCity
from .forms import AdsForm
from .models import Ads
from comment.models import Comment
from django.utils import timezone
from django.db.models import Count, Max
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncDay, TruncDate
import calendar
from django.contrib import messages
from supabase import create_client, Client
import os, uuid
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator


supabase: Client = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SEC'))
bucket_name = os.environ.get('SUPABASE_BUCKET')


@staff_member_required
def dashboard(request):
    # if not request.user.is_admin:
    #     return redirect('listings')
    # today = timezone.now().date()
    today = datetime.now()
    current_month = today.month

    total_users = CustomUser.objects.count()
    today_new_users = CustomUser.objects.filter(created_at=today).count()
    month_new_users = CustomUser.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    year_new_users = CustomUser.objects.filter(created_at__year=today.year).count()

    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())

    #  number of active users who logged in at least once in the last week
    active_users = CustomUser.objects.filter(is_active=True).annotate(max_login_date=Max('last_login')).filter(max_login_date__gte=start_of_week).count()

    # users chart
    user_counts = CustomUser.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    labels = [user_count['month'].strftime('%b') for user_count in user_counts]
    data = [user_count['count'] for user_count in user_counts]

    start_of_year = datetime(datetime.now().year, 1, 1)
    # end_of_year = datetime(datetime.now().year, 12, 31)

    user_counts = CustomUser.objects.filter(created_at__date__range=[start_of_year, today]).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    # print(user_counts)
    count_dict = {user_count['month'].date(): user_count['count'] for user_count in user_counts}
    print(count_dict)
    user_data = [count_dict.get(start_of_year.replace(month=i+1, day=1).date(), 0) for i in range(12)]
    user_labels = [calendar.month_abbr[i+1] for i in range(current_month)]

    # start_of_year = datetime.now() - timedelta(months=datetime.now().month())

    # listings chart
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    end_of_week = start_of_week + timedelta(days=6)
    all_days = [start_of_week + timedelta(days=i) for i in range(7)]
    listing_counts = Listing.objects.filter(created_at__date__range=[start_of_week, end_of_week]).annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    count_dict = {listing_count['day'].date(): listing_count['count'] for listing_count in listing_counts}


    pr_data = [count_dict.get(day.date(), 0) for day in all_days]
    pr_labels = [calendar.day_abbr[i] for i in range(7)]

    total_listings_count = Listing.objects.count()
    month_new_listings = Listing.objects.filter(created_at__year=today.year, created_at__month=today.month).count()

    context = {
        'total_users':total_users,
        'today_new_users':today_new_users,
        'month_new_users':month_new_users,
        'year_new_users':year_new_users,
        'active_users':active_users,
        'labels': user_labels,
        'user_data': user_data,
        'pr_labels': pr_labels,
        'pr_data':pr_data,
        'total_listings_count':total_listings_count,
        'month_new_listings':month_new_listings
    }
    return render(request,'admin/pages/dashboard.html', context)

@staff_member_required
def get_listings(request):
    listings = Listing.objects.all().order_by('-created_at')
    
    paginator = Paginator(listings, 10)  # Show 10 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'listings':page_obj,
        'page_obj': page_obj ,
    }
    return render(request,'admin/pages/listings.html', context)

@staff_member_required
def set_listing_status(request, id):
    listing = Listing.objects.filter(id=id).first()
    if listing:
        listing.admin_status = not listing.admin_status
        listing.save()

    return redirect('admin-listings')

@staff_member_required
def get_users(request):
    users = CustomUser.objects.all().order_by('-created_at')
    
    paginator = Paginator(users, 10)  # Show 10  per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'users':page_obj,
        'page_obj': page_obj ,
    }
    return render(request,'admin/pages/users.html', context)

@staff_member_required
def ban_unban_user(request, id):
    user = CustomUser.objects.filter(id=id).first()
    if user:
        user.is_active = not user.is_active
        user.save()
        messages.info(request, "success")
    else:
        messages.info(request, "user not found")
    return redirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def create_add(request):
    if request.method == 'POST':
        form = AdsForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            file = request.FILES.get('file')
            print('FILE ',file)
            expire_date = timezone.now().date() + timedelta(days=int(form.instance.duration))
            ad.expire_date = expire_date
            ad.user = request.user  # Assuming you have a user associated with the request
            file_name = f'ad_{uuid.uuid4()}{os.path.splitext(file.name)[1]}'
            ad.media_type = file.content_type
            upload_response = supabase.storage.from_(bucket_name).upload(file_name, file.read(), file_options={"content-type": file.content_type})
            if upload_response.status_code == 200:
                print('Upload successful:', upload_response)
                public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
                print(public_url)
                ad.file_path = public_url
                ad.save()
                messages.info(request, "ad posted")
            else:
                print('Upload failed:', upload_response['error'])

    form = AdsForm()
    ads = Ads.objects.all()
    context = {
        'ads':ads,
        'form':form
    }
    return render(request,'admin/pages/ads.html',context )

@staff_member_required
def set_ad_status(request, id):
    ad = Ads.objects.filter(id=id).first()
    if ad:
        ad.status = not ad.status
        ad.save()

    return redirect('admin-ads')

@staff_member_required
def get_cities(request):
    cities = City.objects.all().order_by('name')
    return render(request,'admin/pages/cities.html',{'cities':cities})  

@staff_member_required
def add_city(request):
    name = request.POST.get('name')
    City.objects.create(name=name)
    return redirect('admin-dashboard')

@staff_member_required
def get_subcitiies(request):
    subcities = SubCity.objects.all().order_by('name')
    return render(request,'admin/pages/subcities.html',{'subcities':subcities})  

@staff_member_required
def add_subcity(request):
    name = request.POST.get('name')
    SubCity.objects.create(name=name)
    return redirect('admin-dashboard')

@staff_member_required
def get_comments(request):
    comments = Comment.objects.all().order_by('-created_at')

    paginator = Paginator(comments, 7)  # Show 7 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'comments':page_obj,
        'page_obj': page_obj ,
    }
    return render(request,'admin/pages/comments.html',context)