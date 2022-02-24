import os
import time
import threading

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import View

from Image.models import Image
# Create your views here.
from Image.steno_encryption import steno_decrypt
from django.contrib.auth.mixins import LoginRequiredMixin

def validate_form(data, image):
    error = {}
    if data['caption'] == "":
        error['caption_error'] = "Caption is required"
    if data['key1'] == "":
        error['key1_error'] = "Key required to encrypt the image"
    elif len(data['key1']) < 6:
        error['key1_error'] = "Key must be greater than 6"
    if data['key1'] != data['key2']:
        error['key2_error'] = "Both key must match"
    if data['msg'] == "":
        error['msg_error'] = "No msg to encode"
    if 'image' not in image:
        error['image_error'] = "Select the image for encryption"
    return error


class EncryptImage(LoginRequiredMixin,View):
    paginate_by = 8
    login_url = '/'
    redirect_field_name = 'login'


    def get(self, request, *args, **kwargs):
        queryset = Image.objects.all()
        page = request.GET.get('page', 1)
        photos = self.get_photos(queryset, page)
        print(photos)
        return render(request, "index.html", {'objects': photos})

    def post(self, request, *args, **kwargs):
        default_value = {
            'caption': request.POST['caption'],
            'key1': request.POST['key1'],
            'msg': request.POST['msg'],
        }
        error = validate_form(request.POST, request.FILES)

        if error == {}:
            photo = Image()
            photo.caption = request.POST['caption']
            photo.image = request.FILES['image']
            photo.save(**{'key': request.POST['key1'], 'msg': request.POST['msg']})
            default_value = {}

        queryset = Image.objects.all()
        page = request.GET.get('page', 1)
        photos = self.get_photos(queryset, page)
        context = dict(default_value, **dict(error, **{'objects': photos}))
        return render(request, "index.html", context)

    def get_photos(self, queryset, page):
        paginator = Paginator(queryset, self.paginate_by)
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)
        return photos


class DecryptImage(LoginRequiredMixin, View):
    template_image = 'decryption-image.html'
    template_form = 'decryption-form.html'
    image = None
    login_url = '/login/'
    redirect_field_name = 'login'


    def get(self, request, i, *args, **kwargs):
        photos = get_object_or_404(Image, id=i)
        context = {
            'caption': photos.caption
        }
        return render(request, self.template_form, context)

    def post(self, request, i, *args, **kwargs):
        photos = get_object_or_404(Image, id=i)
        context = {
            'caption': photos.caption
        }
        key = request.POST['key']
        if key != "":
            image = steno_decrypt(key, photos.image.path)
            context = dict(context, **image)
            if 'error' not in image:
                self.image = context['image']
                thread = threading.Thread(target=self.thread_function, args=())
                thread.start()
                return render(request, self.template_image, context)
            else:
                return render(request, self.template_form, context)
        else:
            context['error'] = 'Key required for decryption'
            return render(request, self.template_form, context)

    def thread_function(self):
        time.sleep(5)
        os.remove(self.image)
