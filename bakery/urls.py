from django.urls import path

from bakery import views

# router = routers.DefaultRouter()
# router.register(r'login_user', views.LoginUser, basename='login_user')

urlpatterns = [
    path(r'user/register/', views.RegisterUser.as_view({'post': 'post'}),
         name='register_user'),
    path(r'user/login/', views.LoginUser.as_view({'post': 'post'}),
         name='login_user'),
    path(r'bakery/ingredient/', views.BakeryIngredientViewSet.as_view({
        'post': 'post',
        'get': 'list'
    }),
         name='ingredient_url'),
    path(r'bakery/item/', views.BakeryItemViewSet.as_view({
        'get': 'list'
    }),
         name='get_items_list'),
    path(r'bakery/add_item/', views.AddBakeryItemViewSet.as_view({
        'post': 'post'
    }),
         name='add_item'),
    path(r'bakery/item/<int:pk>', views.BakeryItemViewSet.as_view({
        'get': 'retrieve',
    }),
         name='get_single_item'),
    path(r'bakery/orders/', views.OrderItemViewSet.as_view({
        'get': 'list',
    }),
         name='get_all_orders'),
    path(r'bakery/order/', views.OrderItemViewSet.as_view({
        'post': 'post',
    }),
         name='make_an_order'),
    path(r'bakery/trending/', views.TrendingItemViewSet.as_view({
        'get': 'get',
    }),
         name='get_trending_item'),
]

# urlpatterns = router.urls
