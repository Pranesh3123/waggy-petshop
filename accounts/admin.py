from django.contrib import admin
from .models import UserProfile, UserShippingAddress

# Custom Admin Headers
admin.site.site_header = "Waggy Pet Shop Admin"
admin.site.site_title = "Waggy Admin Portal"
admin.site.index_title = "Waggy Pet Shop Products Details"

admin.site.register(UserProfile)
admin.site.register(UserShippingAddress)
