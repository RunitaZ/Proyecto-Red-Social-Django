from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from .models import PerfilUsuario #modelo creado

# Register your models here.
class PerfilInline(admin.StackedInline):
    model=PerfilUsuario  
    can_delete=False 
    verbose_name_plural="Perfil" 

class UserAdmin(BaseUserAdmin):
    inlines=(PerfilInline,) 

admin.site.unregister(User)  #quita la configuracion por defecto 
admin.site.register(User,UserAdmin)    #regitramos los cambios personalizados 
admin.site.register(PerfilUsuario) 