"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    # map each one of our app's own urls (to keep everything modular)
    path('', include('cellbase.urls')),
    path('', include('labeling.urls')),
    path('', include('labeling_pw.urls')),
    path('admin/', admin.site.urls),
] + static(settings.PREVIEW_URL, document_root=settings.PREVIEW_ROOT)
# ^ this is needed to allow requesting the images by their path in cache
