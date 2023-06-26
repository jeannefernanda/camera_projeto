from django.shortcuts import redirect, render
from django.views import View
import os
import base64
from django.core.files.base import ContentFile
import datetime

class CameraView(View):
    template_name = 'camera_app/camera.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        if 'confirm' in request.POST:
            save_photo(request)

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

    return redirect('camera')
