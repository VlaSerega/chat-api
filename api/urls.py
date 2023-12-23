from django.urls import include, path

urlpatterns = [
    path('', include('api.conversations.urls')),
    path('', include('api.messages.urls')),
    path('', include('api.users.urls'))
]
