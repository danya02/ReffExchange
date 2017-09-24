from django.contrib import admin

# Register your models here.

from .models import Role, User, Invite, Provider, Campaign, Promo

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Invite)
admin.site.register(Provider)
admin.site.register(Campaign)
admin.site.register(Promo)
