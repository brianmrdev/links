import json
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import forms, login, logout, authenticate
from django.http import HttpResponse
from bookmark.models import Link, Category
from .forms import AddLinkForm


class Index(View):
    def get(self, request):
        user = request.user
        
        if user.is_authenticated:
            all_link = Link.objects.all().order_by('-pk')
        else:
            all_link = Link.objects.filter(is_private=False).order_by('-pk')
        
        paginator = Paginator(all_link, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            listado = paginator.page(page)
        except (EmptyPage, InvalidPage):
            listado = paginator.page(paginator.num_pages)
        
        context_data = {
            'title': 'Home',
            'listado': listado,
            'addlinkform': AddLinkForm(),
        }
        return render(request, 'index.html', context_data)


class LinkDetail(View):
    def get(self, request, *args, **kwargs):
        getlink = get_object_or_404(Link, slug=kwargs['url'])
        getlink.count_access += 1
        getlink.save()
        response = redirect(getlink.url)
        return response

class Login(View):
    form = forms.AuthenticationForm

    def post(self, request):
        form = self.form(None, request.POST)
        context = {'form': form}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('1')
            else:
                return HttpResponse('2')
        else:
            return HttpResponse('3')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('public:index')


class AddLink(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            add = AddLinkForm(request.POST)
            if Link.objects.filter(name=request.POST['name']).exists():
                msg = {'status': False,
                       'msg': 'Está intentando registrar un link con un TITULO que ya existe'}
                return HttpResponse(json.dumps(msg))
            elif add.is_valid():                
                add.save()
                msg = {'status': True, 'msg': 'Link guardado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no válido'}
                return HttpResponse(json.dumps(msg))
    

class LinksViewDateCategory(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        getcategory = get_object_or_404(Category, slug=kwargs['url'])
        
        if user.is_authenticated:
            listlink = Link.objects.filter(category=getcategory).order_by('-pk')
        else:
            listlink = Link.objects.filter(category=getcategory, is_private=False).order_by('-pk')
        
        paginator = Paginator(listlink, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            listado = paginator.page(page)
        except (EmptyPage, InvalidPage):
            listado = paginator.page(paginator.num_pages)

        context_data = {
            'title': 'Categoría: {}'.format(getcategory.name),
            'listado': listado,
        }
        return render(request, 'index.html', context_data)