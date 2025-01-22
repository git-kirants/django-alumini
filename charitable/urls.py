from django.urls import path
from . import views

urlpatterns = [
    path('funds/', views.fund_list, name='fund_list'),
    path('funds/create/', views.fund_create, name='fund_create'),
    path('funds/<int:fund_id>/', views.fund_detail, name='fund_detail'),
    path('funds/<int:fund_id>/donate/', views.make_donation, name='make_donation'),
    path('funds/<int:fund_id>/donations/', views.fund_donations, name='fund_donations'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('funds/<int:fund_id>/apply/', views.apply_scholarship, name='apply_scholarship'),
    path('my-applications/', views.my_applications, name='my_scholarship_applications'),
    path('applications/review/', views.review_applications, name='review_applications'),
    path('applications/<int:application_id>/review/', views.review_application, name='review_application'),
    path('fund/<int:fund_id>/edit/', views.fund_edit, name='fund_edit'),
    path('fund/<int:fund_id>/toggle/', views.fund_toggle_status, name='fund_toggle_status'),
    path('fund/<int:fund_id>/delete/', views.fund_delete, name='fund_delete'),
    path('funds/<int:fund_id>/donations/', views.fund_donations, name='fund_donations')
] 