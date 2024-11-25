from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views

urlpatterns = [
    # LOGIN
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("correction/logout/", LogoutView.as_view(), name="logout"),
    # HOME
    path("", views.home, name="home"),
    # TURMAS
    path("cursos/", views.cursos, name="cursos"),
    path("salvar/", views.salvar, name="salvar"),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    # ATIVIDADES
    path("activities/<int:id>/", views.activities, name="activities"),
    path("create_activity/<int:id>/", views.create_activity, name="create_activity"),
    path("select_activity/<int:id>/", views.select_activity, name="select_activity"),
    path("update_activity/<int:id>/", views.update_activity, name="update_activity"),
    path("delete_activity/<int:id>/", views.delete_activity, name="delete_activity"),
    # ANSWERS
    path("activities_details/<int:id>/", views.answers, name="activities_details"),
    path("create_answer/<int:id>/", views.create_answer, name="create_answer"),
    path("select_answer/<int:id>/", views.select_answer, name="select_answer"),
    path(
        "update_correction/<int:id>/", views.update_correction, name="update_correction"
    ),
    path(
        "delete_correction/<int:id>/", views.delete_correction, name="delete_correction"
    ),
    # ALUNOS
    path("students/<int:id>/", views.students, name="students"),
    path("create_student/<int:id>/", views.create_student, name="create_student"),
    path("select_student/<int:id>/", views.select_student, name="select_student"),
    path("update_student/<int:id>/", views.update_student, name="update_student"),
    path("delete_student/<int:id>/", views.delete_student, name="delete_student"),
    # DETALHES
    path("details/<int:id>/", views.details, name="details"),
    # OCR
    path("extract_text/", views.extract_text, name="extract_text"),
    # USUÁRIO
    path("user_settings/", views.user_settings, name="user_settings"),
    path("update_user/", views.update_user, name="update_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
