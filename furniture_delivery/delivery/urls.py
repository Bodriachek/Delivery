from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'delivery'

router = routers.SimpleRouter()

# For change order, for staff
router.register('order', views.OrderViewSet, basename='order')
# Refueling list and change
router.register('fueling/list', views.FuelingViewSet, basename='list_fueling'),
# List repairs
router.register('repairs', views.RepairsViewSet, basename='list_repairs'),
router.register('driver/repair', views.DriverCarRepairViewSet, basename='list_driver_car_repairs'),
# Drivers list task 4,5
router.register('drivers', views.DriverListViewSet, basename='drivers_list'),
# Managers list for task 6
router.register('managers', views.ManagerViewSet, basename='managers_list'),
# Cars list for task 7
router.register('cars', views.CarsViewSet, basename='cars_list'),


urlpatterns = [
    path('', include(router.urls)),
    # Add repair
    path('repair/add', views.AddRepairView.as_view()),
    # Add order
    path('order/add', views.CreateOrderView.as_view()),
    # Add fueling
    path('fueling/add', views.AddFuelingView.as_view()),
]
