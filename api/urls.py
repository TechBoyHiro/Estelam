from django.urls import re_path
from .controllers import UserController

urlpatterns = [
    # USER PATHS
    re_path(r't/user/add/$', UserController.SignUp, name="User Registration"),
]