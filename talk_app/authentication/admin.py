from django.contrib import admin

# Register your models here.
from django.contrib import admin

from authentication.models import CustomUser
from channels.models import Channel

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Channel)
