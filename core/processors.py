from controle_usuarios.models import Profissional

#verificar se atendente estA LOGADO para mostrar opções no menu
def verificar_atendente_logado(request):
	profissional = ""
	if request.user.is_authenticated:
		profissional = Profissional.objects.filter(
			user=request.user,tipo=1)
		
	context = {'atendente':profissional}
	return context

#verificar se profissional estA LOGADO para mostrar opções no menu
def verificar_profissional_logado(request):
	profissional = ""
	if request.user.is_authenticated:
		profissional = Profissional.objects.filter(
			user=request.user,tipo=2)
		
	context = {'profissional_logado':profissional}
	return context