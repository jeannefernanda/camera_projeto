from django.shortcuts import redirect, render
from django.views import View
import base64, datetime, os, glob
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.urls import reverse

class CameraView(View):
    template_name = 'camera_app/camera.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        if 'confirm' in request.POST:
            response = save_photo(request)
            if response:
                return response
        # Redirecionar para a página da câmera
        return redirect('camera')

def save_photo(request):
    if request.method == 'POST':
        photo_data = request.POST.get('photo')

        # Decodificar a foto a partir do formato base64
        format, imgstr = photo_data.split(';base64,')
        ext = format.split('/')[-1]
        photo = ContentFile(base64.b64decode(imgstr), name=f'photo.{ext}')

        # Verifique se a pasta "photos" existe, caso contrário, crie-a
        if not os.path.exists('photos'):
            os.makedirs('photos')

        # Obter a data e hora atual
        current_datetime = datetime.datetime.now()
        timestamp = current_datetime.strftime('%Y%m%d_%H%M%S')

        # Gerar o nome de arquivo único usando a data e hora atual
        filename = f'photo_{timestamp}.{ext}'
        photo_path = os.path.join('photos', filename)

        # Salve a foto no servidor
        with open(photo_path, 'wb') as f:
            for chunk in photo.chunks():
                f.write(chunk)

        # Redirecionar para a página de detalhes da foto
        return redirect(reverse('photo_detail', kwargs={'filename': filename}))

    # Se o método da requisição não for POST, retorne None
    return None

def photo_detail(request, filename):
    photo_path = os.path.join('photos', filename)

    # Verifica se o arquivo existe
    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as f:
            image_data = f.read()
        
        return HttpResponse(image_data, content_type='image/png')
    else:
        return HttpResponse('Foto não encontrada.')

def photo_gallery(request):
    photo_paths = glob.glob('photos/*.png')  # Modifique o padrão de arquivo se necessário
    photo_list = []

    for photo_path in photo_paths:
        filename = os.path.basename(photo_path)
        photo_list.append({
            'filename': filename,
            'url': reverse('photo_detail', kwargs={'filename': filename})
        })

    context = {
        'photo_list': photo_list
    }

    return render(request, 'camera_app/photo_gallery.html', context)