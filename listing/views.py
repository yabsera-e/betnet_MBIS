from django.shortcuts import render,get_object_or_404, redirect
from .models import Listing, ListingMedia, City, SubCity
from comment.forms import CommentForm
from .forms import ListingForm, CitySelectForm, SubCitySelectForm
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from admindashboard.models import Ads
import uuid
import os
from django.core.paginator import Paginator
from supabase import create_client, Client
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

supabase: Client = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SEC'))
bucket_name = os.environ.get('SUPABASE_BUCKET')

def index(request):
    base_query = Listing.objects.prefetch_related('medias').filter(admin_status=True).order_by('-created_at')
    price = request.GET.get('price')
    city = request.GET.get('city')
    subcity = request.GET.get('subcity')
    bedrooms = request.GET.get('bedrooms')

    ads = cache.get('ads')
    if not ads:
        ads = Ads.objects.filter(position='main', status=True).order_by('created_at')
        cache.set('ads', ads, 60*60)
    
    cities = cache.get('cities')
    if not cities:
        cities = City.objects.all()
        cache.set('cities', cities, 60*60)

    subcities = cache.get('subcities')
    if not subcities:
        subcities = SubCity.objects.all()
        cache.set('subcities', subcities, 60*60)

    if price:
        base_query = base_query.filter(price__lte=price)
    if city:
        base_query = base_query.filter(city__name=city)
    if subcity:
        base_query = base_query.filter(sub_city__name=subcity)
    if bedrooms:
        if bedrooms != '5':
            base_query = base_query.filter(bedrooms=bedrooms)
        else:
            base_query = base_query.filter(bedrooms__gte=bedrooms)


    listings = base_query

    paginator = Paginator(listings, 12)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list.exists():
        messages.info(request, "No House Found 😔")


    comment_form = CommentForm()
    context = {
        "listings":page_obj,
        "page_obj":page_obj,
        "cities":cities,
        "subcities":subcities,
        "price_ranges":{
             '5000':'<=5000',
             '10000':'<=10000',
             '20000': '<=20000',
             '30000': '<=30000',
             '40000': '<=40000',
             '50000': '<=50000',
             '60000': '<=60000',
             '80000': '<=80000',
             '120000': '<=120000',
        },
        "bedrooms":{
             '0':'Studio',
             '1':'1 bedroom',
             '2': '2 bedrooms',
             '3': '3 bedrooms',
             '4': '4 bedrooms',
             '5': '5+ bedrooms',
        },
        "user":request.user,
        "ads":ads,
        "comment_form":comment_form
    }

    return render(request, 'listing/index.html', context)

@login_required
def my_listings(request):
    listings = Listing.objects.filter(user_id=request.user.id).order_by('-created_at') 

    ads = Ads.objects.filter(position='main', status=True).order_by('created_at')
    cities = City.objects.all()
    subcities = SubCity.objects.all()

    paginator = Paginator(listings, 8)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    if listings.count() < 1:
        messages.info(request, "You Have No House Listing, Click Post to create one!")
    context = {
        "listings":page_obj,
        "page_obj":page_obj,
        "cities": cities,
        "subcities":subcities,
        "price_ranges":{
             '5000':'<=5000',
             '10000':'<=10000',
             '20000': '<=20000',
             '30000': '<=30000',
             '40000': '<=40000',
             '50000': '<=50000',
             '60000': '<=60000',
             '80000': '<=80000',
             '120000': '<=120000',
        },
        "user":request.user,
        "ads":ads
    }
    return render(request,'listing/my_listings.html', context)


def listing_retrieve(request,id):
    listing = get_object_or_404(Listing, id=id)
    context = {
        "listing":listing
    }
    print(listing)
    return render(request, 'listing/detail.html', context)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save() 
            if request.FILES.getlist('media'):
                    for media_file in request.FILES.getlist('media'):
                        # media storage upload
                        # file_name = f'listing_{form.instance.id}_{uuid.uuid4()}{os.path.splitext(media_file.name)[1]}'
                        # file_path = f'listings/{file_name}'
                        # listing_media = ListingMedia()
                        # listing_media.listing = form.instance
                        # listing_media.media_type = media_file.content_type
                        # default_storage.save(file_path, media_file)
                        # file_url = f'{settings.MEDIA_URL}{file_path}'
                        # listing_media.file_path = file_url
                        # listing_media.save()

                        # supabase upload
                        file = media_file
                        file_ext = os.path.splitext(file.name)[1]
                        file_name = f'listing_{form.instance.id}_{uuid.uuid4()}{os.path.splitext(media_file.name)[1]}'
                        listing_media = ListingMedia()
                        listing_media.listing = form.instance
                        listing_media.media_type = media_file.content_type
                        upload_response = supabase.storage.from_(bucket_name).upload(file_name, file.read(), file_options={"content-type": f"image/{file_ext}"})
                        if upload_response.status_code == 200:
                            print('Upload successful:', upload_response)
                            public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
                            print(public_url)
                            listing_media.file_path = public_url
                            listing_media.file_name = file_name
                            listing_media.save()
                        else:
                            print('Upload failed:', upload_response['error'])


            listings = Listing.objects.all()
            context = {
                "listings":listings
            }
            return redirect("listings")
        return 
    form = ListingForm()
    context = {
        'form':form
    }
    return render(request, "listing/create.html",context)

@login_required
def set_status(request,id):
    listing = get_object_or_404(Listing, id=id,user_id=request.user.id)
    listing.status = not listing.status
    listing.save()
    url = reverse('listing_retrieve', kwargs={'id': listing.id})
    return redirect(url)

@login_required
def listing_update(request, id):
    listing = get_object_or_404(Listing, id=id)
    existing_medias = listing.medias.all()
    
    if request.method == 'POST':
        form = ListingForm(request.POST,instance=listing)
        delete_media_ids = request.POST.getlist('delete_media')
        if form.is_valid():
            form.save()
             ### 🔥 DELETE SELECTED OLD MEDIA ###
            for media_id in delete_media_ids:
                try:
                    media = ListingMedia.objects.get(id=media_id, listing=listing)
                    # Delete from Supabase
                    supabase.storage.from_(bucket_name).remove(media.file_name)
                    media.delete()
                except ListingMedia.DoesNotExist:
                    pass

            ### 🔄 UPLOAD NEW MEDIA ###
            for media_file in request.FILES.getlist('media'):
                file_ext = os.path.splitext(media_file.name)[1]
                file_name = f'listing_{listing.id}_{uuid.uuid4()}{file_ext}'
                upload_response = supabase.storage.from_(bucket_name).upload(file_name, media_file.read(), file_options={"content-type": f"image/{file_ext}"})

                if upload_response.status_code == 200:
                    public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
                    ListingMedia.objects.create(
                        listing=listing,
                        file_path=public_url,
                        file_name=file_name,
                        media_type=media_file.content_type
                    )

            return redirect("listings")
    else:
        form = ListingForm(instance=listing)

    context = {
        'form':form,
        'medias': listing.medias.all()
    }
    return render(request, "listing/edit.html",context)

@login_required
def listing_delete(request, id):
    listing = get_object_or_404(Listing, id=id)
    medias = listing.medias.all()
    if medias.count() > 0:
        for media in medias:
        #     file_path = media.file_path.replace(settings.MEDIA_URL, '')
        #     if default_storage.exists(file_path):
        #         default_storage.delete(file_path)
        #     media.delete()

        # supabase delete
            res = supabase.storage.from_(bucket_name).remove(media.file_name)
    listing.delete()
    return redirect("listings")