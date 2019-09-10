from atendimento.render_pdf import *
from agenda.models import Agendamento

class LiberarPacientePdf(View):
    def get(self, request,pk):
        paciente = get_object_or_404(Agendamento,pk=pk)
        today = timezone.now()
        params = {
            'today': today,
            'agenda': paciente,
            'request': request
        }
        return Render.render('relatorios/liberar_atendimento_pdf.html', params)

class ImprimirAgendamentos(View):
    def get(self, request,pk):
        paciente     = get_object_or_404(Paciente,pk=pk)
        agendamentos = Agendamento.objects.filter(paciente=paciente).order_by('data')
        today        = timezone.now()
        params   = {
            'today': today,
            'agenda': agendamentos,
            'request': request
        }
        return Render.render('agenda/pdfs/imprimir_agendamento.html', params)