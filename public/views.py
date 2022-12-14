import json
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import forms, login, logout, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from bookmark.models import Link, Category
from .forms import AddLinkForm


class Index(View):
    def get(self, request):
        user = request.user

        if user.is_authenticated:
            all_link = Link.objects.all().order_by('-pk')
        else:
            all_link = Link.objects.filter(is_private=False).order_by('-pk')

        paginator = Paginator(all_link, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            listado = paginator.page(page)
        except (EmptyPage, InvalidPage):
            listado = paginator.page(paginator.num_pages)

        context_data = {
            'title': 'Personal, minimalist and ultra-fast bookmarking service.',
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
                       'msg': 'Est?? intentando registrar un link con un TITULO que ya existe'}
                return HttpResponse(json.dumps(msg))
            elif add.is_valid():
                add.save()
                msg = {'status': True, 'msg': 'Link guardado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no v??lido'}
                return HttpResponse(json.dumps(msg))


class LinksViewDateCategory(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        getcategory = get_object_or_404(Category, slug=kwargs['url'])

        if user.is_authenticated:
            listlink = Link.objects.filter(
                category=getcategory).order_by('-pk')
        else:
            listlink = Link.objects.filter(
                category=getcategory, is_private=False).order_by('-pk')

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
            'title': 'Categor??a: {}'.format(getcategory.name),
            'listado': listado,
        }
        return render(request, 'index.html', context_data)


@csrf_exempt
def delete_link(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Link.objects.get(pk=request.POST['id']).delete()
            msg = {'status': True, 'msg': 'Link eliminado correctamente'}
            return HttpResponse(json.dumps(msg))
        except ObjectDoesNotExist:
            msg = {'status': False,
                   'msg': 'El link que usted decea eliminar no existe'}
            return HttpResponse(json.dumps(msg))
    else:
        msg = {'status': False, 'msg': 'Ocurri?? un error'}
        return HttpResponse(json.dumps(msg))

def search_result(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        link = request.POST.get('link')
        qs = Link.objects.filter(name__icontains=link)
        if len(qs) > 0 and len(link) > 0:
            data= []
            for pos in qs:
                item = {
                    'pk': pos.pk,
                    'name': pos.name,
                    'slug': pos.slug,
                    'description': pos.description
                }
                data.append(item)
            res = data
        else:
            res = 'No link found ...'

        return JsonResponse({'data': res})
    return JsonResponse({})


class LinkEdit(View):
    def get(self, request, *args, **kwargs):
        getlink = get_object_or_404(Link, slug=kwargs['slug'])
        context = {'title': getlink.name, 'getlink': getlink, 'editlinkform': AddLinkForm(instance=getlink)}
        return render(request, 'link_edit.html', context)


class LinkSave(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            linkid = Link.objects.get(pk=request.POST['pk'])
            add = AddLinkForm(request.POST, instance=linkid)
            if add.is_valid():
                add.save()

                msg = {'status': True, 'msg': 'Link actualizada correctamente'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Formulario no v??lido'}
            return HttpResponse(json.dumps(msg))