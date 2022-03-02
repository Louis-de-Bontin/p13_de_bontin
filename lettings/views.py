from django.shortcuts import get_object_or_404
from django.shortcuts import render
from lettings.models import Letting


def index(request):
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    a = 1/0
    del(a)
    return render(request, 'lettings_index.html', context)


def letting(request, letting_id):
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'letting.html', context)
