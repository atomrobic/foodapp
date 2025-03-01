from django.contrib import admin
from django.urls import path
from myapp.views import register,checkout,menu_view,menu_item_detail,menu_views,menu_items_detail,dashboard_view,get_pending_orders, user_dashboard,order_success,update_order_status,user_login,update_quantity,remove_item, user_logout, user_profile, update_profile,catering_home,place_catering_order,order_list,add_menu_item,delete_menu_item,add_category,edit_menu_item,menu_report,add_to_cart,view_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", user_profile, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path("place-order/", place_catering_order, name="place_catering_order"),
     path("adminorders/", order_list, name="admin_catering_orders"),
     path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('admindashboard/', dashboard_view, name='dashboard'),

    path('', add_menu_item, name='add_menu_item'),
    path("menu/delete/<int:item_id>/", delete_menu_item, name="delete_menu_item"),     
    path("add-category/", add_category, name="add_category"),
    path("edit-menu-item/<int:item_id>/", edit_menu_item, name="edit_menu_item"),
    path("menu-report/", menu_report, name="menu_report"),
    path('menu/item/<int:item_id>/', menu_items_detail, name='menu_item_details'),

    

    path("home/", catering_home, name="catering_home"),
    path('menuitem/<int:item_id>/', menu_item_detail, name='menu_item_detail'),
path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path('cart/', view_cart, name='cart'),
    path('view/', menu_view, name='view'),  # Correct syntax

   path('cart/update/<int:item_id>/', update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', remove_item, name='remove_item'),
       path("checkout/", checkout, name="checkout"),
     path("order-success/<int:order_id>/", order_success, name="order_success"),  # ✅ This must match the view
       path("get_pending_orders/", get_pending_orders, name="get_pending_orders"),
    path('dashboard/', user_dashboard, name='user_dashboard'),

    path('menu/', menu_views, name='menu'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
