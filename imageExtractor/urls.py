"""imageExtractor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import asyncio
import threading

from django.urls import path
from . import views, queue_worker

urlpatterns = [
    path('', views.index),
    path('extract', views.extract)
]
print('Init Queue Worker.')
loop = asyncio.new_event_loop()
p = threading.Thread(target=queue_worker.init, args=(loop,))
p.start()
print('Init Success.')
