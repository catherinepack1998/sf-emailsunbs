from django.urls import path
from .views import IndexView, add_authors_group

urlpatterns = [
    path('', IndexView.as_view()),
    path('upgrade-authors/', add_authors_group, name = 'upgrade-authors')
]