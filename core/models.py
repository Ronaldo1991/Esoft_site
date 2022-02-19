from django.db import models
import uuid


# O AbstractBaseUser tem menos funcionalidades que o AbstractUser
# Por isso utilizamos o AbstractUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from stdimage.models import StdImageField


class UsuarioManager(BaseUserManager):

    use_in_migrations = True # Avisa que será o model de User utilizado no Banco de dados

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_field.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        
        return self._create_user(email, password, **extra_fields)

class CustomUsuario(AbstractUser):
    id = models.CharField(primary_key=True, serialize=False, verbose_name='ID', default=f'{uuid.uuid4()}', max_length=36)
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    name = models.CharField(max_length=50, default=None)
    cpf = models.CharField(max_length=14, default='000.000.000-00')
    logradouro = models.CharField(max_length=150, default='Desconhecido')
    complemento = models.CharField(max_length=30, default='Desconhecido')
    numero = models.IntegerField(blank=True)
    bairro = models.CharField(max_length=30, default='Desconhecido')
    cep = models.CharField(max_length=10, default='00.000-000')
    cidade = models.CharField(max_length=30, default='Desconhecido')
    uf = models.CharField(
        max_length=2, 
        default='BH',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    USERNAME_FIELD = 'email' # Aqui é configurado qual atributo usado para validação 
    REQUIRED_FIELDS = ['name']
    # Exige todos os campos na configuração também exige a senha.
    # São os campos mostrados na criação do superuser.

    def __str__(self):
        return self.email
    
    objects = UsuarioManager() 
    # Diz que os objeto são gerenciados pelo UsuarioManager
    # Se isso não for especificado o Usuário utilizado será o padrão do Django


class Base(models.Model):
    id = models.AutoField(primary_key=True, max_length=100)
    criados = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    

    class Meta:
      abstract = True


class Produto(Base):
    nome = models.CharField(max_length=30, default='Desconhecido')
    preco = models.DecimalField(max_digits=100, decimal_places=2)
    estoque = models.IntegerField()


    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
      
    def __str__(self):
        return self.nome
    
    objects = UsuarioManager() 
