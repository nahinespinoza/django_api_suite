from django.urls import path
from . import views
from demo_rest_api.views import DemoRestApi, DemoRestApiItem #Importo las clases 

urlpatterns = [
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources" ),
   path("<str:id>/", DemoRestApiItem.as_view(), name="demo_rest_api_item"),

]