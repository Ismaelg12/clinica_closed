from django.apps import AppConfig

class EasyAuditConfig(AppConfig):
    name = 'easyaudit'
    verbose_name = 'Logs de acesso ao Sistema'

    def ready(self):
        from easyaudit.signals import auth_signals, model_signals, request_signals