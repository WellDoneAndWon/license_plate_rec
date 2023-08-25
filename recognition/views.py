from django.shortcuts import render, redirect
from .forms import UploadContentForm
from .services.recognition_photo import recognition_license_plate_photo
from .services.recognition_video import recognition_license_plate_video
import os
import datetime
from pathlib import Path


def upload_content(request):
    if request.method == 'POST':
        delete_files_in_folder()
        form = UploadContentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                photo_instance = form.save()
                photo_path = photo_instance.image.url
                result_img = recognition_license_plate_photo(photo_path, datetime.datetime.now().timestamp())
                return render(request, 'recognition/upload_page.html', {'form': form, 'res_img': result_img})
            elif form.cleaned_data['video']:
                video_instance = form.save()
                video_path = video_instance.video.url
                result_video = recognition_license_plate_video(video_path, datetime.datetime.now().timestamp())
                return render(request, 'recognition/upload_page.html', {'form': form, 'res_vid': result_video})
    else:
        form = UploadContentForm()
    return render(request, 'recognition/upload_page.html', {'form': form})


def delete_files_in_folder(folder_path=str(Path(Path.cwd(), 'answer'))):
    try:
        files = os.listdir(folder_path)
        print(files)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                if int(datetime.datetime.now().timestamp()) - int(file.split('.')[0].split('-')[1]) > 600:
                    os.remove(file_path)
    except Exception as e:
        print(f"Ошибка при удалении файлов: {e}")
