from django.shortcuts import render, get_object_or_404, redirect
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
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


def index(request):
    base_query = Listing.objects.prefetch_related('medias').filter(admin_status=True).order_by('-created_at')
    price = request.GET.get('price')
    city = request.GET.get('city')
    subcity = request.GET.get('subcity')
    bedrooms = request.GET.get('bedrooms')

    ads = cache.get('ads')
    if not ads:
        ads = Ads.objects.filter(position='main', status=True).order_by('created_at')
        cache.set('ads', ads, 60 * 60)

    cities = cache.get('cities')
    if not cities:
        cities = City.objects.all()
        cache.set('cities', cities, 60 * 60)

    subcities = cache.get('subcities')
    if not subcities:
        subcities = SubCity.objects.all()
        cache.set('subcities', subcities, 60 * 60)

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
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list.exists():
        messages.info(request, "No House Found 😔")

    comment_form = CommentForm()
    context = {
        "listings": page_obj,
        "page_obj": page_obj,
        "cities": cities,
        "subcities": subcities,
        "price_ranges": {
            '5000': '<=5000',
            '10000': '<=10000',
            '20000': '<=20000',
            '30000': '<=30000',
            '40000': '<=40000',
            '50000': '<=50000',
            '60000': '<=60000',
            '80000': '<=80000',
            '120000': '<=120000',
        },
        "bedrooms": {
            '0': 'Studio',
            '1': '1 bedroom',
            '2': '2 bedrooms',
            '3': '3 bedrooms',
            '4': '4 bedrooms',
            '5': '5+ bedrooms',
        },
        "user": request.user,
        "ads": ads,
        "comment_form": comment_form
    }

    return render(request, 'listing/index.html', context)


@login_required
def my_listings(request):
    listings = Listing.objects.filter(user_id=request.user.id).order_by('-created_at')

    ads = Ads.objects.filter(position='main', status=True).order_by('created_at')
    cities = City.objects.all()
    subcities = SubCity.objects.all()

    paginator = Paginator(listings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if listings.count() < 1:
        messages.info(request, "You Have No House Listing, Click Post to create one!")

    context = {
        "listings": page_obj,
        "page_obj": page_obj,
        "cities": cities,
        "subcities": subcities,
        "price_ranges": {
            '5000': '<=5000',
            '10000': '<=10000',
            '20000': '<=20000',
            '30000': '<=30000',
            '40000': '<=40000',
            '50000': '<=50000',
            '60000': '<=60000',
            '80000': '<=80000',
            '120000': '<=120000',
        },
        "user": request.user,
        "ads": ads
    }
    return render(request, 'listing/my_listings.html', context)

def listing_retrieve(request, id):
    listing = get_object_or_404(Listing, id=id)
    return render(request, 'listing/detail.html', {"listing": listing})


@login_required
def listing_payment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        listing.is_paid = True
        listing.save()
        return redirect("listings")

    return render(request, "payment/listing_payment.html", {"listing": listing})


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.is_paid = False
            listing.save()
            form.save_m2m()

            for media_file in request.FILES.getlist('media'):
                ext = os.path.splitext(media_file.name)[1]
                filename = f"listings/{uuid.uuid4()}{ext}"

                saved_path = default_storage.save(filename, media_file)

                ListingMedia.objects.create(
                    listing=listing,
                    file_path=settings.MEDIA_URL + saved_path,
                    file_name=os.path.basename(saved_path),
                    media_type=media_file.content_type
                )

            return redirect("listing_payment", listing_id=listing.id)

    else:
        form = ListingForm()

    return render(request, "listing/create.html", {"form": form})

@login_required
def set_status(request, id):
    listing = get_object_or_404(Listing, id=id, user_id=request.user.id)
    listing.status = not listing.status
    listing.save()
    return redirect(reverse('listing_retrieve', kwargs={'id': listing.id}))


@login_required
def listing_update(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        delete_media_ids = request.POST.getlist('delete_media')

        if form.is_valid():
            form.save()

            for media_id in delete_media_ids:
                media = ListingMedia.objects.filter(id=media_id, listing=listing).first()
                if media:
                    file_path = media.file_path.replace(settings.MEDIA_URL, "")
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)
                    media.delete()

            for media_file in request.FILES.getlist('media'):
                ext = os.path.splitext(media_file.name)[1]
                filename = f"listings/{uuid.uuid4()}{ext}"
                saved_path = default_storage.save(filename, media_file)

                ListingMedia.objects.create(
                    listing=listing,
                    file_path=settings.MEDIA_URL + saved_path,
                    file_name=os.path.basename(saved_path),
                    media_type=media_file.content_type
                )

            return redirect("listings")

    else:
        form = ListingForm(instance=listing)

    return render(request, "listing/edit.html", {
        "form": form,
        "medias": listing.medias.all()
    })


@login_required
def listing_delete(request, id):
    listing = get_object_or_404(Listing, id=id)
    medias = listing.medias.all()

    for media in medias:
        if media.file_path and default_storage.exists(media.file_path.name):
            default_storage.delete(media.file_path.name)
        media.delete()

    listing.delete()
    return redirect("listings")