"""
URL configuration for auditorium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from userlog.views import index
from seats.views import seats, success, verify
from seats import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="homepage"),
    path("seats", seats, name="selection"),
    path("success", success, name="submitted"),
    path("verify", verify, name="verification")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Custom 404 error view
handler404 = 'auditorium.views.error_404' 
# # Custom 500 error view
handler500 = 'auditorium.views.error_500'  