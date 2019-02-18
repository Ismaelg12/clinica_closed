from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.utils import timezone
from atendimento.models import Atendimento
from pacientes.models import Paciente

class Pdf(View):
    def get(self, request,pk):
        atendimento = get_object_or_404(Atendimento,pk=pk)
        today = timezone.now()
        params = {
            'today': today,
            'atendimento': atendimento,
            'request': request
        }
        return Render.render('relatorios/atendimento_detalhe_pdf.html', params)

class Historico_Pdf(View):
    def get(self, request,pk):
        paciente              = get_object_or_404(Paciente,pk=pk)
        atendimentos          = Atendimento.objects.filter(paciente=paciente)
        today = timezone.now()
        params = {
            'today': today,
            'atendimentos': atendimentos,
            'request': request
        }
        return Render.render('relatorios/atendimentos_paciente_pdf.html', params) 

class Render:
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
