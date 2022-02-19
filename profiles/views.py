from django.shortcuts import get_object_or_404
from django.shortcuts import render
from profiles.models import Profile


def index(request):
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles_index.html', context)


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {'profile': profile}
    return render(request, 'profile.html', context)
