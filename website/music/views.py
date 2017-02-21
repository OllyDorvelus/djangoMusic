# from django.shortcuts import render

# Create your views here.

# from django.http import HttpResponse
#from django.http import HttpResponse
from django.http import Http404
#from django.template import loader
# from django.shortcuts import render, get_object_or_404
# from .models import Album, Song


# def index(request):
#     all_albums = Album.objects.all()
#     html = ''
#     for album in all_albums:
#         url = '/music/' + str(album.id) + '/'
#         html += '<a href="' + url + '">' + album.album_title + '</a><br>'
#     return HttpResponse(html)

# def index(request):
#     all_albums = Album.objects.all()
#     template = loader.get_template('music/index.html')
#     context = {'all_albums': all_albums}
#     return HttpResponse(template.render(context, request))

# def index(request):
#     all_albums = Album.objects.all()
#     context = {'all_albums': all_albums}
#     return render(request, 'music/index.html', context)


# def detail(request, album_id):
#     try:
#         album = Album.objects.get(pk=album_id)
#     except Album.DoesNotExist:
#         raise Http404("Album does not exist")
#     return render(request, 'music/detail.html', {'album': album})


# def detail(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     return render(request, 'music/detail.html', {'album': album})
#
#
# def test(request):
#     return HttpResponse("<h1>Hello World</h1>")
#
# def favorite(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         selected_song = album.song_set.get(pk=request.POST['song'])
#     except (KeyError, Song.DoesNotExist):
#         return render(request, 'music/detial.html'), {
#             'album':album,
#              'error_message': "You did not select a valid Song",
#         }
#     else:
#         selected_song.is_favorite = True
#         selected_song.save()
#         return render(request, 'music/detail.html', {'album': album})

#fresh start
from django.views import generic
from .models import Album, Song
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, UserLoginForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Album.objects.filter(user = self.request.user)
        else:
            return Album.objects.filter(user = None)


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
    def get_object(self, *args, **kwargs):
        obj = super(DetailView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied
        else:
            return obj



class AlbumCreate(LoginRequiredMixin, CreateView):
    login_url = "music:login"
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumCreate, self).form_valid(form)















class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    def get_object(self, *args, **kwargs):
        obj = super(AlbumUpdate, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied
        else:
            return obj

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class SongCreate(LoginRequiredMixin, CreateView):
    login_url = 'music:login'
    model = Song
    fields = ['album', 'file_type', 'song_title']


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'
    #display blank form

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         redirect("music:index")
#     else:
#         redirect("music:login")

class UserLoginFormView(View):
    form_class = UserLoginForm
    template_name = "music/login_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("music:index")

        else:

            return redirect("music:login")
        #return render(request, self.template_name, {'form': form})

#def logout_view:
def logout_view(request):
    logout(request)
    return redirect('music:index')





