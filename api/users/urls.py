from django.urls import re_path

from api.users.views import MyContactsView, UserSearchListView

urlpatterns = [
    re_path(r'^users/search/', UserSearchListView.as_view()),
    re_path(r'^users/contacts/', MyContactsView.as_view()),
]
