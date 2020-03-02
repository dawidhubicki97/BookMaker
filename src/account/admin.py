from django.contrib import admin
from account.models import User
from account.models import Customer
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
	list_display=('email','username','password','is_active')
	search_fields=('email','username')
	readonly_fields=()
	filter_horizontal=()
	list_filter=()
	fieldsets=()

admin.site.register(User,AccountAdmin)
