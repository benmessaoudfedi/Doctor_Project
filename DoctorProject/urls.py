from django.contrib import admin
from django.urls import path
from Doctor import views, pdfviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
    path('home/', views.home, name="home"),
    path('', views.accueil, name="accueil"),
    path('profile/', views.profileview, name="profileview"),
    path('profile/edit/', views.profileedit, name="profileedit"),
    path('change-password/',views.change_password, name='change_password'),
    path('patients-list/', views.doctor_list_patients, name='list_patients'),

    path('add-patient/', views.AddPatient, name='add_patient'),
    path('edit-patient/<int:pk>', views.EditPatient, name='edit_patient'),
    path('delete-patient/<int:pk>', views.DeletePatient, name='delete_patient'),
    path('add-consultation/<int:pk>', views.AddConsultation, name='add_consultation'),
    path('add-consultation/', views.AddDirectConsultation, name='add_direct_consultation'),
    path('consultations-list/', views.doctor_list_consultations, name='list_consultations'),
    path('delete-consultation/<int:pk>', views.DeleteConsultation, name='delete_consultation'),
    path('patient-profile/<int:pk>', views.PatientProfile, name='patient_profile'),
    path('edit-consultation/<int:pk>', views.EditConsultation, name='edit_consultation'),
    path('consultation/<int:pk>', views.ConsultationView, name='view_consultation'),

    path('list-consultations-pdf/', pdfviews.listconsultationspdfviews.as_view(), name="list_consultation_pdf"),
    path('consultations-pdf/<int:pk>', pdfviews.consultationspdfviews.as_view(), name="consultation_pdf"),
    path('list-patients-pdf/', pdfviews.listpatientspdfviews.as_view(), name="list_patients_pdf"),
    path('add-images/<int:pk>', views.images_upload, name='images_upload'),
    path('consultation-images/<int:pk>', views.ajax_server,name='consultation_image'),
    path('images-list/<int:pk>', views.consultation_list_images, name='consultation_list_images'),
    path('edit-image/<int:pk>', views.edit_consultation_image, name='edit_consultation_image'),
    path('delete-image<int:pk>/<int:fk>/', views.delete_image, name='delete_image'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]
