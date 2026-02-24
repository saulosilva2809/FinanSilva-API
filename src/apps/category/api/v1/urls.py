from django.urls import path

from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    SubCategoryListCreateView, SubCategoryRetrieveUpdateDestroyView
)


urlpatterns = [
    path('category/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('category/<uuid:pk>', CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_update_destroy'),
    path('sub-category/', SubCategoryListCreateView.as_view(), name='sub_category_list_create'),
    path('sub-category/<uuid:pk>', SubCategoryRetrieveUpdateDestroyView.as_view(), name='sub_category_retrieve_update_destroy'),
]
