from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView


urlpatterns = [
    path('category/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('category/<uuid:pk>', CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_update_destroy'),
]
