from django.urls import path, include
from accounts import views as views

# ________________________________________________

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    # api-v1
    path('api/v1/', include('accounts.api.v1.urls', namespace='api-v1'), name='api-v1'),
]

# ________________________________________________
