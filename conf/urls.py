"""university URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.admin.sites import all_sites
# from abiturients.admin import AuthForm

# admin.autodiscover()
# admin.site.login_form = AuthForm
# admin.site.login_template = 'login.html'

paths = [path(f'{site.name}', site.urls) for site in all_sites]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('application.urls')),
    path("dynamic-admin-form/", include("dynamic_admin_forms.urls")),
    # path("dynamic-admin-form/", include("dynamic_admin_forms.urls"))
]

urlpatterns.extend(paths)
