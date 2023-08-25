from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recognition.views import upload_content


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_content)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
