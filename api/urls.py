from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', views.api_registration_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('labs', views.lab_list.as_view()),
    path('lab_invites', views.lab_invite_list.as_view()),
    path('inventories', views.inventory_list.as_view()),
    path('items', views.item_list.as_view()),
    path('item_batches', views.item_batch_list.as_view()),
    path('item_notices', views.item_notices_list.as_view()),
    path('item_orders', views.item_order_list.as_view()),
    path('item_activity_logs', views.item_activity_log_list.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
