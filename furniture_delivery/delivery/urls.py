from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register('driver', views.DriverViewSet, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
    # Список замовлень
    path('order/', views.OrderViewSet.as_view({'get': 'list'})),
    # Для оформлення замовлення
    path('order/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
    # Для прийому заявки менеджером
    path('order/change/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    # Список заправок
    path('fueling/', views.RefuelingViewSet.as_view({'get': 'list'})),
    # Для реєстрації заправок
    path('fueling/<int:pk>/', views.RefuelingViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
    # Список ремонтів
    path('repairs/', views.RepairsViewSet.as_view({'get': 'list'})),
    # Для додавання деталей про ремонт
    path('repairs/<int:pk>/', views.RepairsViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
    # Список водіїв для завдань 4 та 5
    path('drivers/', views.DriversViewSet.as_view({'get': 'list'})),
    # Список менеджерів для завдання 6
    path('managers/', views.ManagerViewSet.as_view({'get': 'list'})),
    # Список авто для завдання 7
    path('cars/', views.CarsViewSet.as_view({'get': 'list'})),
    #
    path('drivers/detail/', views.DriversListViewSet.as_view({'get': 'list'})),
]
