from django.urls import path
from .views import create_model, model_detail_api,model_viewer,generate_object

urlpatterns = [
    path("generate/", create_model, name="create_model"),
    path("api/models/<int:model_id>/", model_detail_api, name="model_detail_api"),
     path("viewer/<int:model_id>/", model_viewer, name="model_viewer"),
      path('api/generate-object/', generate_object, name='generate_object'),
]


