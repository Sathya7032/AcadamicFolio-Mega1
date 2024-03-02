from django.urls import path
from .views import *

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('',index,name="index"),
    path('code/',code,name="code"),
    path('contact/',contact,name="contact"),
    path('login/',login_view,name="login"),
    path('register/',register_view,name="register"),
    path('logout/',logout_view,name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name='password/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password/reset_password_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name='password_reset_complete'),
    
    path('tasks/', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),

    path('homepage/',homepage,name="homepage"),
    path('blog_detail/',blogs,name='blogs'),
    path('blog_detail/<int:blog_id>/',singleBlog,name='singleBlog'),
    path('tutorials/',tutorials,name="tutorials"),
    path('tutorials/<int:tut_id>/',tutorialView,name="tutorialView"),
    path('tutorials/post/<int:post_id>/',tutorialPost,name="tutorialPost"),
    path('meme/',meme,name="meme"),


    path('upload_meme/',upload_meme,name="upload_meme"),
    path('upload_blog/',post_blog,name="add_blog"),
]
