from django.contrib import admin
from .models import Listing, Bid, Comment, Watchlist, Category

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'creation_date', "user","category")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", 'comment')

class BidAdmin(admin.ModelAdmin):
    list_display=("listing", "bid", "user")

class WatchlistAdmin(admin.ModelAdmin):
    list_display=("user","listing")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Category)
