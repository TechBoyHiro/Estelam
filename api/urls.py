from django.urls import re_path
from .controllers import UserController,EstelamController

urlpatterns = [
    # USER PATHS
    re_path(r't/user/add/$', UserController.SignUp, name="User Registration"),
    re_path(r'estelam/add/$', EstelamController.AddEstelam, name="Add New Estelam"),
]