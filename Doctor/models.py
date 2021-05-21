from django.db import models
from django.contrib.auth.models import User
from DoctorProject import settings
departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

Gender=[('Male','Male'),
('Female','Female')
]

Provenance=[('Tunis','Tunis'),
('Ariana','Ariana'),
('Ben Arous','Ben Arous'),
('Manouba','Manouba'),
('Nabeul','Nabeul'),
('Zaghouan','Zaghouan'),
('Bizerte','Bizerte'),
('Béja','Béja'),
('Jendouba','Jendouba'),
('Kef','Kef'),
('Siliana','Siliana'),
('Sousse','Sousse'),
('Monastir','Monastir'),
('Mahdia','Mahdia'),
('Sfax','Sfax'),
('Kairouan','Kairouan'),
('Sidi Bouzid','Sidi Bouzid'),
('Gabès','Gabès'),
('Mednine','Mednine'),
('Tataouine','Tataouine'),
('Gafsa','Gafsa'),
('Tozeur','Tozeur'),
('Kebili','Kebili')
]

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='static/assets/DoctorProfilePic/',default='static/assets/DoctorProfilePic/photo_default.jpg', null=True, blank=True)
    address = models.CharField(max_length=40,null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False,null=True, blank=True)
    patients = models.ManyToManyField('Patient', through='Consultation', related_name='doctorconsultation')
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=40,null=True, blank=True)
    last_name = models.CharField(max_length=40,null=True, blank=True)
    address = models.CharField(max_length=40,null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)
    carte_cin= models.CharField(max_length=40,null=True, blank=True)
    sexe= models.CharField(max_length=40,choices=Gender,default='Male')
    type_dossier= models.CharField(max_length=40,null=True, blank=True)
    provenance= models.CharField(max_length=40,choices=Provenance,default='Tunis')
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE, related_name='doctor')
    doctors = models.ManyToManyField(Doctor, through='Consultation', related_name='doctorconsultation')


class Consultation(models.Model):
    doctor = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date= models.DateField()
    description =models.TextField()
    symptoms = models.TextField()

class Images(models.Model):
    Image_Consultation = models.ImageField(upload_to='static/assets/ConsultationImages/', null=False, blank=False)
    Consultation = models.ForeignKey('Consultation', on_delete=models.CASCADE)
    model_image=models.CharField(max_length=30,null=True, blank=True)

