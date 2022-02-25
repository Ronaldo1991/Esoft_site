from django.views import View
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from core.models import CustomUsuario
from core.models import Produto
from core.models import HistoricoProduto
from django.db.models import F
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from chartjs.views.lines import BaseLineChartView
from random import randint
import datetime


class AcountRegister(View):
    
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        try:
            usuario_aux = CustomUsuario.objects.get(email=request.POST['email'])
            if usuario_aux.email:
                print('Usuário já existe')
                context = {
                    'usuarioexistente': 'Esse E-mail já existe tente outro.'
                }
                return render(request, 'register.html', context)
        except CustomUsuario.DoesNotExist:
            email = request.POST['email']
            if "@" not in email:
                context = {
                    'email_formato': 'O formato não é de email, falta o @.'}
                return render(request, 'register.html', context)
            if "." not in email:
                context = {
                    'email_formato': 'O formato não é de email, falta o ".".'}
                return render(request, 'register.html', context)
            name = request.POST['name']
            password = request.POST['password']
            password2 = request.POST['password2']
            cpf = request.POST['cpf']
            logradouro = request.POST['logradouro']
            complemento = request.POST['complemento']
            numero = request.POST['numero']
            bairro = request.POST['bairro']
            cep = request.POST['cep']
            # Fazer o tratamento
            cidade = request.POST['cidade']
            uf = request.POST['uf']
            
            lista_estados = ('AC', 'AL', 'AP', 'AM', 'BA','CE','DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB',\
                     'PR', 'PE', 'PI', 'RJ', 'RN','RS','RO', 'RR','Roraima', 'SC','SP', 'SE', 'TO')
            if len(uf) > 2:
                context = {
                    'uf': 'Coloque apenas as iniciais do seu Estado.'
                    
                }
                return render(request, 'register.html', context)                
            if str(uf) not in lista_estados:
                context = {
                    'uf': 'O estado não existe no Brasil, escreva outro.'
                    
                }
                return render(request, 'register.html', context)                
            if password != password2:
                print('Senhas diferentes.')
                context = {
                    'senhaigual': 'As duas senhas são diferentes escreva de novo.'
                }
                return render(request, 'register.html', context)
            novoUsuario = CustomUsuario.objects.create_user(name=name, cpf=cpf, logradouro=logradouro, complemento=complemento, numero=numero, 
            bairro=bairro, cep=cep, cidade=cidade, uf=uf, password=password, email=email )
            print(novoUsuario)
            novoUsuario.save()
            verifica_usuario = CustomUsuario.objects.get(email=request.POST['email'])
            print(verifica_usuario)
            if verifica_usuario:
                context = {
                    'cadastro_sucesso': 'Usuário cadastrado com sucesso.'
                }
                return render(request, 'register.html', context)
            else:
                print('Falha nos 2 cadastros.')
                context = {
                    'cadastro_falha': 'Houve falha no cadastro cadastre-se de novo.'
                }
                return render(request, 'register.html', context)


class Login(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        try:
            usuario_aux = CustomUsuario.objects.get(email=request.POST['email'])
            username = request.POST['email']
            password = request.POST['password']
            print(username)
            print(password)
            if usuario_aux.email:
                usuario_aux = authenticate(request, email=request.POST['email'], username=request.POST['email'], password=request.POST['password'])
                print(usuario_aux)
                if usuario_aux:
                    login(request, usuario_aux)
                    print(f"O valor do login é: {request.user.is_authenticated}")
                    return render(request, 'home.html')
                else:
                    context = {
                        'usuariofalha': 'Houve algum problema com a sua senha.'
                    }
                    return redirect('login')
        except CustomUsuario.DoesNotExist:
            print('Usuário não existe')
            context = {
                'usuarionaoexistente': 'Não há cadastro com esse usuário de E-mail.'
            }
            return render(request, 'login.html', context)


class Logout(View):
    
    def get(self, request):
        print("Entrou no Logout")
        logout(request)
        return render(request, "index.html")


class IndexView(TemplateView):
    template_name = 'index.html'


class HomeView(TemplateView):
    template_name = 'home.html'


class ProdutoView(TemplateView, View):

    def get(self, request):
        """
        Retrieve information about all products.
        """
        print(f"O método utilizado é: {request.method}")
        context = super(ProdutoView, self).get_context_data()
        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
        return render(request, "produtos.html", context)
    
    
    def post(self, request):
        """
        Create new products.
        """
        print("Entrou no POST")
        print(type(request.POST))
        print(request.POST)
        print(request.POST.keys())
        print(request.POST.items())
        if 'patch' in request.POST.keys():
            """
            Update a product.
            """
            print("Entrou no PATCH")
            try:
                nome = request.POST['nome']
                preco = request.POST['preco']
                estoque = request.POST['estoque']
                produto = Produto.objects.filter(nome=nome)
                lista = list(Produto.objects.filter(nome=nome))[0]
                print(lista)
            except IndexError:
                context = {
                    'produto_inexistente': 'O produto não existe procure outro.'
                }
                context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                return render(request, 'produtos.html', context)
            else:
                try:
                    preco = float(preco)
                except ValueError:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                else:
                    if preco < 0:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                try:
                    estoque = int(estoque)
                except ValueError:
                        context = {
                            'estoque_falha': 'O valor do estoque não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                else:
                    if preco < 0 or estoque < 0:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                try:
                    produto.update(nome=nome, preco=preco, estoque=estoque)
                    print(produto)
                    dia = int(datetime.datetime.now().day)
                    hora = int(datetime.datetime.now().hour)
                    ano = int(datetime.datetime.now().year)
                    mes = int(datetime.datetime.now().month)
                    historico_produto = HistoricoProduto.objects.create(nome=nome, preco=preco, estoque=estoque, dia=dia, hora=hora, ano=ano, mes=mes)
                    historico_produto.save()
                    if not historico_produto:
                        context = {
                            'produto_falha': 'Houve falha no Histórico do Produto.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                    print(historico_produto)
                except:
                    context = {
                        'produto_falha': 'Houve um erro no momento de editar o produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                else:
                    context = {
                        'produto_sucesso': 'Produto editado com sucesso.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)

        elif 'delete' in request.POST.keys():
            """
            Delete a product.
            """ 
            print("Entrou no delete")
            try:
                nome = request.POST['nome']
                produto = Produto.objects.filter(nome=nome)
                lista = list(Produto.objects.filter(nome=nome))[0]
                print(lista)
            except IndexError:
                context = {
                    'produto_inexistente': 'O produto não existe procure outro.'
                }
                context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                return render(request, 'produtos.html', context)
            else:
                produto.delete()
                dia = int(datetime.datetime.now().day)
                hora = int(datetime.datetime.now().hour)
                ano = int(datetime.datetime.now().year)
                mes = int(datetime.datetime.now().month)
                historico_produto = HistoricoProduto.objects.create(nome=nome, preco=0, estoque=0, dia=dia, hora=hora, ano=ano, mes=mes)
                historico_produto.save()
                if not historico_produto:
                    context = {
                        'produto_falha': 'Houve falha no Histórico do Produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                print(historico_produto)
                if not produto:
                    context = {
                        'produto_sucesso': 'Produto deletado com sucesso.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                else:
                    context = {
                        'produto_falha': 'Houve um erro no momento de deletar o produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
        
        elif 'delete_id' in request.POST.keys():
            """
            Delete a product by id.
            """ 
            print("Entrou no delete por id")
            try:              
                lista = list(request.POST.keys())
                produto = Produto.objects.filter(nome=lista[2])
                
            except IndexError:
                context = {
                    'produto_inexistente': 'O produto não existe procure outro.'
                }
                context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                return render(request, 'produtos.html', context)
            else:
                produto.delete()
                dia = int(datetime.datetime.now().day)
                hora = int(datetime.datetime.now().hour)
                ano = int(datetime.datetime.now().year)
                mes = int(datetime.datetime.now().month)
                historico_produto = HistoricoProduto.objects.create(nome=lista[2], preco=0, estoque=0, dia=dia, hora=hora, ano=ano, mes=mes)
                historico_produto.save()
                if not historico_produto:
                    context = {
                        'produto_falha': 'Houve falha no Histórico do Produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                print(historico_produto)
                if not produto:
                    context = {
                        'produto_sucesso': 'Produto deletado com sucesso.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                else:
                    context = {
                        'produto_falha': 'Houve um erro no momento de deletar o produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)

        else:
            context = super(ProdutoView, self).get_context_data()
            # Recupera dados do BD, caso exista
            context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
            
            try:
                usuario_aux = Produto.objects.get(nome=request.POST['nome'])
                if usuario_aux.nome:
                    context = {
                        'produto_existente': 'Esse produto já existe cadastre outro.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
            except Produto.DoesNotExist:
                nome = request.POST['nome']
                preco = request.POST['preco']
                estoque = request.POST['estoque']
                # Treating value rules
                try:
                    preco = float(preco)
                except ValueError:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                else:
                    if preco < 0:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                try:
                    estoque = int(estoque)
                except ValueError:
                        context = {
                            'estoque_falha': 'O valor do estoque não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                else:
                    if estoque < 0:
                        context = {
                            'preco_falha': 'O valor do preço não é válido insira outro.'
                        }
                        context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                        return render(request, 'produtos.html', context)
                novoProduto = Produto.objects.create(nome=nome, preco=preco, estoque=estoque)
                novoProduto.save()
                verifica_produto = Produto.objects.get(nome=request.POST['nome'])
                dia = int(datetime.datetime.now().day)
                hora = int(datetime.datetime.now().hour)
                ano = int(datetime.datetime.now().year)
                mes = int(datetime.datetime.now().month)
                historico_produto = HistoricoProduto.objects.create(nome=nome, preco=preco, estoque=estoque, dia=dia, hora=hora, ano=ano, mes=mes)
                historico_produto.save()
                if not historico_produto:
                    context = {
                        'produto_falha': 'Houve falha no Histórico do Produto.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                print(historico_produto)
                if verifica_produto:
                    context = {
                        'produto_sucesso': 'Produto cadastrado com sucesso.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)
                else:
                    context = {
                        'produto_falha': 'Houve falha no cadastro do Produto de novo.'
                    }
                    context['produtos'] = Produto.objects.order_by(F('nome').asc(nulls_last=True)).all()
                    return render(request, 'produtos.html', context)


class DadosJSONView(BaseLineChartView):


    def get_labels(self):
        """Return 12 labels for axis x."""
        global labels
        if datetime.datetime.now().month  in [1,3,5,7,8,10,12]:
            labels = [
            "01","02","03","04","05","06","07","08","09","10",
            "11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24","25","26","27","28","29","30",
            "31",
        ]
        
        elif datetime.datetime.now().month == 2:
            labels = [
            "01","02","03","04","05","06","07","08","09","10",
            "11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24","25","26","27","28",
        ]
        else:            
            labels = [
            "01","02","03","04","05","06","07","08","09","10",
            "11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24","25","26","27","28","29","30",
        ]
        return labels
    
    def get_providers(self):
        """Return datasets."""
        lista = list(HistoricoProduto.objects.order_by().values_list('nome').distinct())
        # Getting only distinct Objects using field nome
        datasets = [i for i in lista]
        print(datasets)
        return datasets
    
    def get_data(self):
        """
        Return 6 datasets for graphic plotage.

        Each line is dataset.
        Each Column is a Label.

        12 labels, so 12 columns.
        6 datasets, so 6 lines.
        """
        global labels
        # print(labels)
        dados = []
        lista = list(HistoricoProduto.objects.order_by().values_list('nome').distinct())
        # dados_dia = list(HistoricoProduto.objects.order_by(F('criados').asc(nulls_last=True)).values_list('modificado','nome'))
        # print(dados_dia[0][0])
        # print(int(str(dados_dia[0][0]).split("-")[-1]))
        dia = int(datetime.datetime.now().day)
        ano = int(datetime.datetime.now().year)
        # print(dia)
        # print(dados_dia)
        # print(len(lista))
        dados_mes = list(HistoricoProduto.objects.all())
        filtrados = HistoricoProduto.objects.filter(dia=dia, ano=ano)
        print(filtrados)
        for c in range(0,len(lista)):
            for l in range(0,len(labels)):
                dado = [randint(1,200) for i in range(1,(dia+1))]
            dados.append(dado)
        return dados
