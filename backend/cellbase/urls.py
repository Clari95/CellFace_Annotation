from django.urls import path

from . import views
from . import authentication as auth_views

urlpatterns = [
    # authentication routes
    path('login', auth_views.handle_login, name='login'),
    path('logout', auth_views.handle_logout, name='logout'),
    # catch relative paths in simulated File System
    path('explorer/', views.explore, name='explore_root'),
    path('explorer/<path:f_path>/', views.explore, name='explore'),
    path('preprocess/<path:f_path>.raw', views.preprocess_dataset, name='preprocess_dataset'),
    # uploading dataset
    path('upload/', views.upload_bin, name='upload_bin'),
    path('uploadf/', views.upload_folder, name='upload_folder'),
    # preview dataset info and edit its metadata
    path('preview/<path:f_path>.raw', views.preview, name='preview'),
    path('preview/<path:f_path>.raw/meta/<str:ds_name>', views.metadata, name='metadata'),
    path('preview/<path:f_path>.raw/<str:group>/<str:ds_name>', views.preview_details, name='preview_details'),

    # status
    path('status/', views.status, name='status'),

    # more of utility routes
    path('tags/', views.available_tags, name='available_tags'),
    path('projects/', views.available_projects, name='available_projects'),
]

