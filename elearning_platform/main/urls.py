from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views  # Add this import


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:chapter_id>/', views.quiz_view, name='quiz'),
    path('profile/', views.profile, name='profile'),
    path('video/<int:chapter_id>/', views.video_view, name='video_view'),
    path('accounts/', include('django.contrib.auth.urls')),  # Ensure this is included
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Ensure this line is correct
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
     path('submit-contact-form/', views.submit_contact_form, name='submit_contact_form'),
]
