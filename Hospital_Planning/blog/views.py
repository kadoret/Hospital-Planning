# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def blog_view(request):
	blog_list = blog.objects.all()
	paginator = Paginator(blog_list, 15)
	page = request.GET.get('page')
	try:
		my_blog_page = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
                my_blog_page = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
                my_blog_page = paginator.page(paginator.num_pages)
        return render(request, 'blog/view.html', {'blog_list': my_blog_page})

@login_required
def blog_insert(request):
	pass
