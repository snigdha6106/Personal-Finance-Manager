from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('budgets/', views.budgets, name='budgets'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),  # View for the settings page
    path('save-settings/', views.save_settings, name='save_settings'),  # View to save the settings and send SMS
    path('change-password/', views.change_password, name='change_password'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('signup/', views.signup, name='signup'), 
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/', views.categories, name='categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('change-password/', views.change_password, name='change_password'),
    path('login/', views.login_view, name='login'),
    path('transactions/', views.transactions, name='transactions'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('logout/', views.logout, name='logout'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),
]

