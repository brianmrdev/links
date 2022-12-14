from django.shortcuts import render
from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from bookmark.models import Link


class Index(View):
    def get(self, request):
        all_link = Link.objects.all().order_by('-pk')
        
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
            'title': 'Links',
            'listado': listado,
        }
        return render(request, 'index.html', context_data)


class LinkDetail(View):
    def get(self, request, *args, **kwargs):
        getlink = get_object_or_404(Link, slug=kwargs['url'])
        getlink.count_access += 1
        getlink.save()
        response = redirect(getlink.url)
        return response
