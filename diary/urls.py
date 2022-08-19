from django.urls import path
from .views import CreateDiaryView, ReadDiaryView, DetailDiaryView, EditDiaryView, DeleteDiaryView

urlpatterns = [
    path('create/', CreateDiaryView.as_view(), name='create_diary'),
    path('read/', ReadDiaryView.as_view(), name='read_diary'),
    path('id/<int:pk>/', DetailDiaryView.as_view(), name='detail_diary'),
    path('edit/<int:pk>/', EditDiaryView.as_view(), name='edit_diary'),
    path('del/<int:pk>/', DeleteDiaryView.as_view(), name='del_diary'),

]