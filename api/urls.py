from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('register/', views.api_registration_view),
    path('users', views.user_list.as_view()),
    path('user/<int:pk>', views.user_detail.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('labs', views.lab_list.as_view()),
    path('lab/<int:pk>', views.lab_detail.as_view()),
    path('lab_invites', views.lab_invite_list.as_view()),
    path('lab_invite/<int:pk>', views.lab_invite_detail.as_view()),
    path('inventories', views.inventory_list.as_view()),
    path('inventory/<int:pk>', views.inventory_detail.as_view()),
    path('items', views.item_list.as_view()),
    path('item/<int:pk>', views.item_detail.as_view()),
    path('item_batches', views.item_batch_list.as_view()),
    path('item_batch/<int:pk>', views.item_batch_detail.as_view()),
    path('item_notices', views.item_notices_list.as_view()),
    path('item_orders', views.item_order_list.as_view()),
    path('item_activity_logs', views.item_activity_log_list.as_view()),
    path('item_batch_history/<int:pk>', views.history_list.as_view()),
    path('item_history/<int:pk>', views.item_quantity_history.as_view()),
    path('item_all_history/<int:pk>', views.item_quantity_history.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
