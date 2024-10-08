from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from.models import User, Province



class MyUserAdmin (UserAdmin):
    fieldsets = (
        (None,{'fields':('username','password')}),
            
        (_('Personal info'),{'fields':('first_name','last_name','phone_number','email')}),
        
        (_('Permissions'),{'fields':('ia_active','is_staff','is_superuser','groups','user_permissions')}),

        (_('Important dates'),{'fields':('last_login','date_joined')}),)
    add_fieldsets=(
        (None,{'classes':('wide',),
               'fields':('username','phone_number','password1','password2')})
    )
    list_display = ('username','phone_number','email','is_staff')
    search_fields=('username__exact',)
    ordering = ('-id',)

    def get_search_results(self, request: HttpRequest, queryset: QuerySet[Any], search_term: str) -> tuple[QuerySet[Any], bool]:
        return super().get_search_results(request, queryset, search_term)
        
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(phone_number=search_term_as_int)
        return queryset,may_have_duplicates


        
        admin.site.unregister (Group)
        admin.site.register(Province)
        admin.site.register(User, MyUserAdmin)    


