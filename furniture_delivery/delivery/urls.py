from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'delivery'

router = routers.SimpleRouter()


# CRUD order for staff
router.register('staff-order', views.StaffOrderView, basename='staff-order'),
# Refueling list and change
router.register('fueling-list', views.FuelingViewSet, basename='list_fueling'),
# List repairs
router.register('all-repairs', views.RepairsViewSet, basename='list_repairs'),
router.register('now-repairs', views.DriverCarRepairViewSet, basename='list_driver_car_repairs'),
# Drivers list task 4,5
router.register('drivers', views.DriverListViewSet, basename='drivers_list'),
# Managers list for task 6
router.register('managers', views.ManagerViewSet, basename='managers_list'),
# Cars list for task 7
router.register('cars', views.CarsListViewSet, basename='car_list'),


urlpatterns = [
    path('', include(router.urls)),
    # Add repair
    path('add-repair/', views.AddRepairView.as_view()),
    # Add order
    path('add-order/', views.AddOrderView.as_view()),
    # Future order list
    path('future-order-list/', views.FutureOrderListView.as_view()),
    # Add fueling
    path('add-fueling/', views.AddFuelingView.as_view()),
]
