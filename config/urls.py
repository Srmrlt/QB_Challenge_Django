from django.contrib import admin
from django.urls import path, include
from data_processor.views import stream_binary_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data_processor.urls')),
    path('stream/<path:file_path>', stream_binary_file, name='stream_binary_file'),
]
