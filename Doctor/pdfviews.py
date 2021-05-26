from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


from django.views.generic import View

from datetime import datetime

from Doctor.models import Consultation, Patient


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class listconsultationspdfviews(View):
    def get(self, request, *args, **kwargs):
        template = get_template('accounts/doctor_list_consultations_pdf.html')
        consultations = Consultation.objects.filter(doctor=request.user.doctor).select_related()
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d")

        context = {'consultations': consultations}

        html = template.render(context)
        pdf = render_to_pdf('accounts/doctor_list_consultations_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "List_Consultations_%s.pdf" % (formatedDate)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")

            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("Not found")

class consultationspdfviews(View):
    def get(self, request, *args, **kwargs):
        template = get_template('accounts/view_consultation_pdf.html')
        consultation= Consultation.objects.select_related().get(id=self.kwargs['pk'])
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d")

        context = {'consultation': consultation}

        html = template.render(context)
        pdf = render_to_pdf('accounts/view_consultation_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Consultations_%s.pdf" % (formatedDate)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")

            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("Not found")

class listpatientspdfviews(View):
    def get(self, request, *args, **kwargs):
        template = get_template('accounts/doctor_list_patients_pdf.html')
        patients = Patient.objects.all().filter(doctor_id=request.user.doctor)
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d")

        context = {'patients': patients}

        html = template.render(context)
        pdf = render_to_pdf('accounts/doctor_list_patients_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "List_Patients_%s.pdf" % (formatedDate)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")

            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("Not found")