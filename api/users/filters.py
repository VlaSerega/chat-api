from django_filters import rest_framework as filters

from api.models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains', required=True)

    class Meta:
        model = User
        fields = ('email',)
