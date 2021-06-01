from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor, Patient, Images, Consultation
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)


class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class ImagesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Images, ImagesAdmin)

class ConsultationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Consultation, ConsultationAdmin)