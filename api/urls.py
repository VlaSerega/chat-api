from django.urls import include, path

urlpatterns = [
    path('', include('api.conversation.urls')),
    path('', include('api.users.urls'))
]
