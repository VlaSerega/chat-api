from django.urls import path

from api.views import UserSearchListView, MyConversationView, MyContactsView, ConversationView

urlpatterns = [
    path('users/search/', UserSearchListView.as_view()),
    path('conversation/my/', MyConversationView.as_view()),
    path('users/contacts/', MyContactsView.as_view()),
    path('conversation/', ConversationView.as_view())
]
