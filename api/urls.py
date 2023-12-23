from django.urls import include, path

urlpatterns = [
    path('', include('api.conversations.urls')),
    path('', include('api.users.urls'))
]
