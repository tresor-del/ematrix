from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist, Category
from .forms import ListingForm, CommentForm, BidForm


def index(request):
    user= request.user
    bid = Bid.objects.all()
    listings = Listing.objects.filter(is_closed=False).all()
    try:
        user_watchlist_listing= Watchlist.objects.filter(user=user).all()
        return render(request, "auctions/index.html",{
            "listings": listings,
            "bid": bid,
            "listings_in_watchlist": len(user_watchlist_listing)
        })
    except:
        return render(request, "auctions/index.html",{
            "listings": listings,
            "bid": bid
        })
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST ,request.FILES)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.user= request.user
            forms.save()
        else:
            form = ListingForm()
            user=request.user
            user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
            return render(request, "auctions/listing.html", {
                'form': form,
                "listings_in_watchlist": len(user_listings_in_watchlist)
            })
        return HttpResponseRedirect(reverse('index'))
    else:
        form = ListingForm()
        user= request.user
        user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
    return render(request, "auctions/listing.html", {
        'form': form,
        "listings_in_watchlist": len(user_listings_in_watchlist)
    })


def listing_views(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    bid = Bid.objects.filter(listing=listing).all()
    user= request.user
    listing_category= listing.category
    listings_category= Listing.objects.filter(category=listing_category).exclude(slug=slug).all()
    valable_bid= listing.price + 1
    try:
        user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
    except TypeError:
        user_listings_in_watchlist= Watchlist.objects.all()
    comments= Comment.objects.filter(listing=listing).all()
    formm = CommentForm()
    form = BidForm()
    try:
        watchlist=Watchlist.objects.filter(user=user, listing=listing).all()
    except TypeError:
        watchlist= Watchlist.objects.all()

    if listing.is_closed:
        try:
            user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
        except TypeError:
            user_listings_in_watchlist= Watchlist.objects.all()
        comments= Comment.objects.filter(listing=listing).all()
        formm = CommentForm()
        form = BidForm()
        try:
            watchlist=Watchlist.objects.filter(user=user, listing=listing).all()
        except TypeError:
            watchlist= Watchlist.objects.all()
        highest_price= listing.price
        winner_bid=Bid.objects.get(listing=listing, bid=highest_price)
        winner=winner_bid.user
        if request.user==winner:
            return render(request, f"auctions/listingviews.html", {
                            "listing": listing,
                            "comments": comments,
                            'number_comment': len(comments),
                            "bid": bid,
                            "bids": len(bid),
                            "listings_in_watchlist": len(user_listings_in_watchlist),
                            "watchlist": len(watchlist),
                            "formm": formm,
                            "form": form,
                            'listing_closed_message': f"Congratulation {winner} ! You win the auction for this listing",
                            "listings_category":listings_category,
                            'valable_bid': valable_bid
                        })
        else:
            return render(request, f"auctions/listingviews.html", {
                            "listing": listing,
                            "comments": comments,
                            'number_comment': len(comments),
                            "bid": bid,
                            "bids": len(bid),
                            "listings_in_watchlist": len(user_listings_in_watchlist),
                            "watchlist": len(watchlist),
                            "formm": formm,
                            "form": form,
                            'listing_closed_message': "Auction for this listing is closed",
                            "listings_category":listings_category,
                            'valable_bid': valable_bid
                        })
    else:
        if request.method == "POST":
            if "form" in request.POST:
                    form = BidForm(request.POST)
                    if form.is_valid():
                        user_bid = form.cleaned_data["bid"]
                        bidlist=[]
                        bid = Bid.objects.filter(listing=listing).all()
                        for other_bid in bid:
                            if user_bid<int(other_bid.bid):
                                bidlist.append(other_bid.bid)
                        if len(bidlist) != 0 or user_bid == listing.price :
                            form.clean()
                            listing = get_object_or_404(Listing, slug=slug)
                            bid = Bid.objects.filter(listing=listing).all()
                            valable_bid= listing.price + 1
                            return render(request, f"auctions/listingviews.html", {
                                "listing": listing,
                                "comments": comments,
                                'number_comment': len(comments),
                                "bid": bid,
                                "bids": len(bid),
                                "listings_in_watchlist": len(user_listings_in_watchlist),
                                "watchlist": len(watchlist),
                                "formm": formm,
                                "form": form,
                                'message': "YOUR BID MUST BE GREATER THAN THE CURRENT PRICE",
                                "listings_category":listings_category,
                                'valable_bid': valable_bid
                            })
                        elif len(bidlist) == 0 and user_bid <= listing.price :
                            form.clean()
                            listing = get_object_or_404(Listing, slug=slug)
                            bid = Bid.objects.filter(listing=listing).all()
                            valable_bid= listing.price + 1
                            return render(request, f"auctions/listingviews.html", {
                                "listing": listing,
                                "comments": comments,
                                'number_comment': len(comments),
                                "bid": bid,
                                "bids": len(bid),
                                "listings_in_watchlist": len(user_listings_in_watchlist),
                                "watchlist": len(watchlist),
                                "formm": formm,
                                "form": form,
                                'message': "YOUR BID MUST BE GREATER THAN THE CURRENT PRICE",
                                "listings_category":listings_category,
                                'valable_bid': valable_bid
                            })
                        else:
                            form_bid = form.save(commit=False)
                            form_bid.user= request.user
                            form_bid.listing= listing
                            form_bid.bid = user_bid
                            form_bid.save()
                            form = BidForm()
                            listing.price = float(user_bid)
                            listing.save()
                            listing = get_object_or_404(Listing, slug=slug)
                            bid = Bid.objects.filter(listing=listing).all()
                            valable_bid= listing.price + 1
                            return render(request, f"auctions/listingviews.html", {
                                "listing": listing,
                                "comments": comments,
                                'number_comment': len(comments),
                                "bid": bid,
                                "bids": len(bid),
                                "listings_in_watchlist": len(user_listings_in_watchlist),
                                "watchlist": len(watchlist),
                                "formm": formm,
                                "form":form,
                                "listings_category":listings_category,
                                'valable_bid': valable_bid
                            })
                    else:
                        form = BidForm()
                        listing = get_object_or_404(Listing, slug=slug)
                        bid = Bid.objects.filter(listing=listing).all()
                        valable_bid= listing.price + 1
                        return render(request, f"auctions/listingviews.html", {
                            "listing": listing,
                            "comments": comments,
                            'number_comment': len(comments),
                            "bid": bid,
                            "bids": len(bid),
                            "listings_in_watchlist": len(user_listings_in_watchlist),
                            "watchlist": len(watchlist),
                            "formm": formm,
                            "form": form,
                            "listings_category":listings_category,
                            'valable_bid': valable_bid
                        })

            elif "formm" in request.POST:
                    formm= CommentForm(request.POST)
                    if formm.is_valid():
                        form1= formm.save(commit=False)
                        form1.user = request.user
                        form1.listing = listing
                        form1.save()
                        formm = CommentForm()

                    else:
                        formm = CommentForm()
                        valable_bid= listing.price + 1
                        return render(request, f"auctions/listingviews.html", {
                            "listing": listing,
                            "comments": comments,
                            'number_comment': len(comments),
                            "bid": bid,
                            "bids": len(bid),
                            "listings_in_watchlist": len(user_listings_in_watchlist),
                            "watchlist": len(watchlist),
                            "formm": formm,
                            "form": form,
                            "listings_category":listings_category,
                            'valable_bid': valable_bid
                        })
                    return render(request, f"auctions/listingviews.html", {
                            "listing": listing,
                            "comments": comments,
                            'number_comment': len(comments),
                            "bid": bid,
                            "bids": len(bid),
                            "listings_in_watchlist": len(user_listings_in_watchlist),
                            "watchlist": len(watchlist),
                            "formm": formm,
                            'form': form,
                            "listings_category":listings_category,
                            'valable_bid': valable_bid
                        })
            elif "form_close_bid" in request.POST:
                listing=get_object_or_404(Listing, slug=slug)
                listing.is_closed= True
                listing.save()
                return redirect('index')
        return render(request, f"auctions/listingviews.html", {
                "listing": listing,
                "comments": comments,
                'number_comment': len(comments),
                "bid": bid,
                "bids": len(bid),
                "listings_in_watchlist": len(user_listings_in_watchlist),
                "watchlist": len(watchlist),
                "formm": formm,
                "form": form,
                "listings_category":listings_category,
                'valable_bid': valable_bid
            })


@login_required
def profile(request, name):
    userp = User.objects.get(username=name)
    userw= request.user
    listingw= Watchlist.objects.filter(user=userw).all()
    return render(request, "auctions/profile.html", {
        "user": userp,
        "listings_in_watchlist": len(listingw)
    })

    

@login_required
def add_to_watchlist(request, slug):
    user = request.user
    list= get_object_or_404(Listing, slug=slug)
    watchlist= Watchlist.objects.create(user=user, listing=list)
    watchlist.save()
    return HttpResponseRedirect(reverse("listingv", kwargs={"slug": slug }))

@login_required
def delete_from_watchlist(request, slug):
    user= request.user
    listing= get_object_or_404(Listing, slug=slug)
    watchlist=Watchlist.objects.get(user=user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listingv", kwargs={"slug": slug }))

@login_required
def watchlist(request):
    user= request.user
    user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
    bid = Bid.objects.all()
    return render(request, "auctions/watchlist.html", {
        "listing":user_listings_in_watchlist,
        "listings_in_watchlist": len(user_listings_in_watchlist),
        "bid":bid
    })

def categories(request):
    categories=Category.objects.all()
    user=request.user
    try:
        user_listings_in_watchlist= Watchlist.objects.filter(user=user).all()
    except:
        user_listings_in_watchlist= Watchlist.objects.all()
    
    return render(request, "auctions/categories.html",{
        "categories": categories,
        "listings_in_watchlist": len(user_listings_in_watchlist)
    })

def category_active_listing(request, category):
    cat=get_object_or_404(Category, category=category)
    category_listings= Listing.objects.filter(category=cat, is_closed=False).all()
    user = request.user
    try:
        user_listings_in_watchlist=Watchlist.objects.filter(user=user)
    except:
        user_listings_in_watchlist= Watchlist.objects.all()
    return render(request, 'auctions/category_active_listing.html',{
        'category_listings': category_listings,
        'category': category,
        "listings_in_watchlist": len(user_listings_in_watchlist)
    })