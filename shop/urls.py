from django.urls import path

from shop import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login/', views.LoginSysView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('categories/', views.CategoriesView.as_view(), name='categories_list'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('empty-cart/', views.empty_cart, name='empty_cart'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('<str:index>/', views.ProductsView.as_view(), name='products_list'),
    path('product-details/<int:id>', views.ProductDetailView.as_view(), name='detailed_view'),
    path('add-to-cart/<int:id>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<int:id>', views.DeleteFromCartView.as_view(), name='delete_from_cart')
]
