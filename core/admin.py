from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm
from .forms import CustomUsuario
from .models import Produto

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('id','name', 'cpf', 'email', 'logradouro', 'complemento', 'numero', 'bairro', 'cep', 'cidade', 'uf')
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Informações Pessoais', {'fields': ('name','cpf', 'logradouro', 'complemento', 'numero', 'bairro', 'cep', 'cidade', 'uf')}),
        ('Permissões', {'fields': ('is_active','is_staff', 'is_superuser', 'groups','user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login','date_joined')}),
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'preco', 'estoque', 'modificado', 'criados')
