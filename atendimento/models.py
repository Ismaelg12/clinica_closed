# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from core.utils import TIPO_ATENDIMENTO,STATUS,TIPO_GUIA,STATUS_GUIA
from django.core.validators import MaxValueValidator, MinValueValidator

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Models de Atendimento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

#Cabecalho de todos os atendimentos
class Atendimento(models.Model):
    tipo          = models.CharField(max_length=2,blank=True,
        choices=TIPO_ATENDIMENTO)
    data          = models.DateField()
    paciente      = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    hora_inicio   = models.TimeField()
    hora_fim      = models.TimeField()
    convenio      = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    procedimento  = models.ForeignKey(Procedimento,on_delete=models.PROTECT,blank=True,null=True)
    profissional  = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    guia          = models.ForeignKey('Guia',on_delete=models.PROTECT,blank=True,null=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em     = models.DateTimeField('Criado em', auto_now_add=True)


    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'

    def __str__(self):
        return str(self.paciente) + ' '+ str(self.convenio)+ ' ' +str(self.procedimento)

        
#atendimento evolução
class Evolucao(models.Model):
    atendimento   = models.OneToOneField(Atendimento,
        on_delete=models.CASCADE,primary_key=True)
    evolucao      = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Evolução'
        verbose_name_plural = 'Evoluções'

    def __str__(self):
        return "{}".format(self.atendimento)


#Ficha de TerapiaOcupacional
class TerapiaOcupacional(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    peso                 = models.FloatField('Peso ao Nascer',validators=[
        MinValueValidator(0.5), MaxValueValidator(58)])
    gestacao_parto       = models.TextField('Gestação/Parto',blank=True)
    aspecto_motor        = models.TextField('Aspecto Motor',blank=True)
    aspecto_sensorio     = models.TextField('Aspecto Sensório-Perceptivo.',blank=True)
    aspecto_social       = models.TextField('Aspecto Social',blank=True)
    comunicacao          = models.TextField('Comunicação',blank=True)
    condulta_terapeutica = models.TextField('Condulta Terapeutica Social',blank=True)

    class Meta:
        verbose_name = 'Terapia'
        verbose_name_plural = 'Terapia'

    def __str__(self):
        return "{}".format(self.atendimento)

#Ficha de Psiquiatria
class Psiquiatria(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    queixa               = models.TextField('Queixa',blank=True)
    hma                  = models.TextField('HMA',blank=True)
    queixa_sintomatica   = models.TextField('Queixa sintomatica',blank=True)
    hist_medicacao       = models.TextField('Historico de medicações.',blank=True)
    ante_psiquiatrico    = models.TextField('Antecedentes psiquiátricos',blank=True)
    ante_medico          = models.TextField('Antecedentes Médicos',blank=True)
    exam_complementar    = models.TextField('Exames Complementares',blank=True)
    observacao           = models.TextField('Observacao',blank=True)
    eixo1                = models.TextField('Eixo1',blank=True)
    eixo2                = models.TextField('Eixo2',blank=True)
    eixo3                = models.TextField('Eixo3',blank=True)
    eixo4                = models.TextField('Eixo4',blank=True)
    eixo5                = models.TextField('Eixo5',blank=True)
    Condulta_psiquiatrica= models.TextField('Condulta Psiquiatrica', blank=True)

    class Meta:
        verbose_name = 'Psiquiatria'
        verbose_name_plural = 'Psiquiatria'

    def __str__(self):
        return "{}".format(self.atendimento)

class Fisioterapeuta(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    cid                  = models.TextField('Hipótese diagnóstica',blank=True)
    queixa               = models.TextField('Queixa',blank=True)
    has                  = models.BooleanField('has')
    cardiaca             = models.BooleanField('Insuficiência Cardíaca')
    dm                   = models.BooleanField('Dm')
    hipotireoidismo      = models.BooleanField('Hipotireidismo')
    neoplasia            = models.BooleanField('Neoplasias')
    onde_neoplasia       = models.CharField('Local Neoplasia',max_length=30,blank=True)
    tromboflebite        = models.BooleanField('Tromboflebites')
    fratura              = models.BooleanField('Fraturas')
    onde_fratura         = models.CharField('Local Fratura',max_length=30,blank=True)
    sintese_metalica     = models.BooleanField('Síntese metálica')  
    disturbio            = models.BooleanField('Distúrbios de sensibilidades')
    doenca               = models.BooleanField('Doenças dermatológicas')
    marca_passo          = models.BooleanField('Marca-Passo')
    epifise              = models.BooleanField('Epífise férteis')
    sind_raynaud         = models.BooleanField('Síndrome de Raynaud')
    fotosensibilidade    = models.BooleanField('História de fotosensibilidade')
    gravidez             = models.BooleanField('Gravidez')
    outro                = models.TextField('outros', blank=True)
    exam_complementar    = models.TextField('Exames Complementares', blank=True)
    exam_fisico          = models.TextField('Exames físicos', blank=True)
    esquema_corporal     = models.TextField('Esquema Corporal', blank=True)
    Condu_fisioterapica  = models.TextField('Condulta Fisioterapica', blank=True)

    class Meta:
        verbose_name = 'Fisioterapia'
        verbose_name_plural = 'Fisioterapia'

    def __str__(self):
        return "{}".format(self.atendimento)

class Anaminese_adulto(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    queixa               = models.TextField('Queixa Principal',blank=True)
    psic_anterior        = models.BooleanField('Psicologia Anterior')
    psiq_anterior        = models.BooleanField('Psiquiatra Anterior')
    encaminhado_por      = models.CharField('Encaminhado Por',max_length=30,blank=True)
    outro_profissional   = models.CharField('Atendido por outros',max_length=30,blank=True)
    uso_medicacao        = models.CharField('Uso de Medicamentos',max_length=30,blank=True)
    med_psiquiatrico     = models.CharField('Medicamentos Psiquiatricos',max_length=30,blank=True)
    reacao_fisiolo       = models.CharField('Reações Fisiológicas',max_length=30,blank=True)
    hist_doencas         = models.CharField('Histórico de doenças',max_length=30,blank=True)
    hist_dificuldade     = models.TextField('Histórico de Dificuldades',blank=True)
    dinamica_fam         = models.TextField('Dinâmica Familiar',blank=True)
    fato_marcante        = models.TextField('Fato marcante',blank=True)
    trauma               = models.TextField('Traumas',blank=True)
    afetivo              = models.TextField('Relacionamento afetivo',blank=True)
    vida_sexual          = models.TextField('Vida Sexual',blank=True)
    amizade              = models.TextField('Amizades',blank=True)
    lazer                = models.TextField('Atividades de Lazer',blank=True)
    rotina               = models.TextField('Rotina',blank=True)
    escolar              = models.TextField('Rotina Escola',blank=True)
    profissional2        = models.TextField('Rotina profissional',blank=True)
    pessoal              = models.TextField('Rotina pessoal',blank=True)
    familiar             = models.TextField('Rotina familiar',blank=True)
    plano_futuro         = models.TextField('Planos futuros',blank=True) 
    expectativa          = models.TextField('Expectaticas para terapia',blank=True)
    dificul_pessoal      = models.TextField('Dificuldades Pessoais',blank=True)
    caracteristica       = models.TextField('Caracteristicas',blank=True)
    meta                 = models.TextField('Metas',blank=True)
    postura_geral        = models.CharField('POstura feral',max_length=30,blank=True)
    cuidado_pessoal      = models.CharField('Cuidados Pessoais',max_length=30,blank=True)
    fluencia             = models.CharField('Fluencia verbal',max_length=30,blank=True)
    organizacao          = models.CharField('Organização',max_length=30,blank=True)
    tique                = models.CharField('Tiques',max_length=30,blank=True)
    observacao           = models.TextField('Observações',blank=True)

    class Meta:
        verbose_name = 'Anaminese_adulto'
        verbose_name_plural = 'Anaminese_adulto'

    def __str__(self):
        return "{}".format(self.atendimento)

class Anaminese_crianca(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    responsavel          = models.CharField('Responsável pela criança',max_length=30,blank=True)
    n_irmaos             = models.CharField('Dinâmica Familiar',max_length=30,blank=True)
    posicao_familiar     = models.CharField('Atendido por outros',max_length=30,blank=True)
    matrimonio           = models.BooleanField('Casados/Separados')
    reacao_1             = models.CharField('Reação1 da Criança',max_length=30,blank=True)
    caso_separado        = models.CharField('Caso de separação',max_length=30,blank=True)
    filho                = models.BooleanField('Biológico/Adotivo')
    crianca_ciente       = models.BooleanField('Criança é ciente')
    reacao_2             = models.CharField('Reação2 da Criança',max_length=30,blank=True)
    queixa               = models.TextField('Queixa Principal criança',blank=True)
    tempo                = models.CharField('Tempo',max_length=30,blank=True)
    frequencia           = models.CharField('Frequência',max_length=30,blank=True)
    consequencia         = models.CharField('Consequências',max_length=30,blank=True)
    atitude_Pais         = models.CharField('Atitude dos Pais',max_length=30,blank=True)
    esforco              = models.CharField('Esforços comportamentais',max_length=30,blank=True)
    outro_profissional   = models.CharField('Outros Profissionais',max_length=30,blank=True)
    medicacoes           = models.CharField('Medicações em uso',max_length=30,blank=True)
    ativ_ocupacional     = models.CharField('Atividades Ocupacionais',max_length=30,blank=True)
    gestacao             = models.BooleanField('Completa/Prematura/Pós-matura')
    saude_mae            = models.BooleanField('Doenças/Imquietações')
    Parto                = models.BooleanField('Normal/Cezariana/induzido')
    idade                = models.CharField('Idade',max_length=30,blank=True)
    enjoou               = models.BooleanField('Enjoou?')
    tempo_1              = models.CharField('Tempo1',max_length=30,blank=True)
    gav_desejada         = models.BooleanField('Criança foi desejada?')
    abortos              = models.BooleanField('Sim/não?')
    qnt_abortos          = models.CharField('Quantos abortos',max_length=30,blank=True)
    compl_gravidez       = models.CharField('Complicações na gravidez',max_length=30,blank=True)
    denc_concepcao       = models.CharField('Doenças antes da concepção',max_length=30,blank=True)
    amamentacao          = models.BooleanField('Materna/Artificial?')
    ate_idade1           = models.CharField('Ate que idade1?',max_length=30,blank=True)
    mamadeira            = models.BooleanField('Usou mamadeira?')
    ate_idad2            = models.CharField('Ate que idade2?',max_length=30,blank=True)
    alimentacao          = models.CharField('Como é a alimentação?',max_length=30,blank=True)
    desenv_esperado      = models.BooleanField('Desenvolvimento esperado?')
    sorriu_idade         = models.CharField('sorriu em que idade?',max_length=30,blank=True)
    engatinhou_idade     = models.CharField('Engatinhou em que idade?',max_length=30,blank=True)
    ficou_pe             = models.CharField('Ficou em pé?',max_length=30,blank=True)
    andou_idade          = models.CharField('Andou em que idade?',max_length=30,blank=True)
    correu               = models.CharField('Correu em que idade?',max_length=30,blank=True)
    braco                = models.BooleanField('Maior tempo nos braços?')
    palavras             = models.CharField('Falou em que idade?',max_length=30,blank=True)
    atraso_fala          = models.BooleanField('Sim/Não')
    troca_letra          = models.BooleanField('Sim/não')
    qual1                = models.CharField('Qual1?',max_length=30,blank=True)
    dificul_esfincter    = models.BooleanField('Sim/não')
    contro_esfincter     = models.BooleanField('Sim/não')
    idade2                = models.CharField('Idade de controle?',max_length=30,blank=True)
    mania                = models.CharField('Mania',max_length=30,blank=True)
    enurese_noturna      = models.BooleanField('Enurese noturna')
    desenv_afetado       = models.CharField('Qual1?',max_length=30,blank=True)
    dificul_fala         = models.BooleanField('Dificuldades de Fala')
    qual4                = models.CharField('Qual14',max_length=30,blank=True)
    visao                = models.BooleanField('Dificuldades de vidão')
    qual5                = models.CharField('Qual5?',max_length=30,blank=True)
    locomocao            = models.BooleanField('Dificuldades de locomoção')
    qual6                = models.CharField('Qual6?',max_length=30,blank=True)
    avds                 = models.CharField('Atividades diárias?',max_length=30,blank=True)
    banha_so             = models.BooleanField('Banha só')
    escova_so            = models.BooleanField('Escola dentes so')
    usa_banheiro_so      = models.BooleanField('Usua o banheiro só')
    precisa_auxilio      = models.BooleanField('Necessita de ajuda par respirar')
    retirada_fruda       = models.BooleanField('Retirada de Fraudas')
    intervencao          = models.BooleanField('Atende a internvenções')
    chora_fabi           = models.BooleanField('Chora Fácil')
    recus_auxililo       = models.BooleanField('Recusa auxilio')
    resistencia          = models.BooleanField('Resistencia a toque')
    bem_escola           = models.BooleanField('Vai bem na escola')
    gosta_estudar        = models.BooleanField('Gosta de estudar')
    estudam_crianca      = models.BooleanField('Pais estudam com a crianca')
    orientacao_dever     = models.BooleanField('Recebe ajudad nos deveres')
    quem_ajuda           = models.CharField('Quem ajuda?',max_length=30,blank=True)
    tempo_ajuda          = models.CharField('Tempo de ajuda?',max_length=30,blank=True)
    gosta_professora     = models.BooleanField('Gosta da professora')
    nota_baixa           = models.BooleanField('É castigado')
    materia              = models.BooleanField('Dificuldades em materias')
    qual7                = models.CharField('Qual7?',max_length=30,blank=True)
    idade_escola         = models.CharField('Frequenta a escola a quanto tempo?',max_length=30,blank=True)
    destro               = models.CharField('Destro?',max_length=30,blank=True)
    outra_escola         = models.BooleanField('Sim/Não')
    qual8                = models.CharField('Qual8?',max_length=30,blank=True)
    mortivo_trans        = models.CharField('Motivo da transferencia?',max_length=30,blank=True)
    repetiu_serie        = models.BooleanField('Sim/Não')
    lingua_estrangeira   = models.BooleanField('Sim/Não')
    qual_ling            = models.CharField('Qual Ligua?',max_length=30,blank=True)
    esporte              = models.BooleanField('Sim/Não')
    qual_esporte         = models.CharField('Qual Esporte?',max_length=30,blank=True)
    danca                = models.BooleanField('Sim/Não')
    qual_danca           = models.CharField('Qual Dança?',max_length=30,blank=True)
    intru_musical        = models.BooleanField('Sim/Não')
    qual_inst            = models.CharField('Qual Instrumento?',max_length=30,blank=True)
    outra_ativi          = models.BooleanField('Sim/Não')
    qual_outra           = models.CharField('Qual outra atividade?',max_length=30,blank=True)
    faz_amigo            = models.BooleanField('Sim/Não')
    adaptacao            = models.BooleanField('Sim/Não')
    compa_brincadeira    = models.CharField('Companheiros de Brincadeiras?',max_length=30,blank=True)
    mesmo_sexo           = models.BooleanField('Sim/Não')
    sexo_oposto          = models.BooleanField('Sim/Não')
    mesma_idade          = models.BooleanField('Sim/Não')
    mais_nova            = models.BooleanField('Sim/Não')
    mais_velha           = models.BooleanField('Sim/Não')
    tv                   = models.BooleanField('Sim/Não')
    musica               = models.BooleanField('Sim/Não')
    leitura              = models.BooleanField('Sim/Não')
    colecao              = models.BooleanField('Sim/Não')
    computador           = models.BooleanField('Sim/Não')
    outra_distracao      = models.CharField('Qual Ligua?',max_length=30,blank=True)
    obediente            = models.BooleanField('Sim/Não')
    independente         = models.BooleanField('Sim/Não')
    comunicativo         = models.BooleanField('Sim/Não')
    agressivo            = models.BooleanField('Sim/Não')
    cooperador           = models.BooleanField('Sim/Não')
    outra_atitude        = models.CharField('Qual10?',max_length=30,blank=True)
    tranquilo            = models.BooleanField('Sim/Não')
    seguro               = models.BooleanField('Sim/Não')
    ancioso              = models.BooleanField('Sim/Não')
    alegre               = models.BooleanField('Sim/Não')
    emotivo              = models.BooleanField('Sim/Não')
    queixoso             = models.BooleanField('Sim/Não')
    outra_emocao         = models.BooleanField('Sim/Não')
    insonia              = models.BooleanField('Sim/Não')
    pesadelo             = models.BooleanField('Sim/Não')
    hipersonia           = models.BooleanField('Sim/Não')
    dorme_sozinho        = models.BooleanField('Sim/Não')
    dorme_pais           = models.BooleanField('Sim/Não')
    divide_quarto        = models.CharField('Qual10?',max_length=30,blank=True)
    perturbacao          = models.BooleanField('Sim/Não')
    habito_especial      = models.BooleanField('Sim/Não')
    disciplina_pai       = models.TextField('Disciplina Pais',blank=True)
    contrariado          = models.TextField('Reação ao ser Contrariado',blank=True)
    histo_doenca         = models.TextField('Histórico de doenças',blank=True)
    freque_doenca        = models.TextField('Frequencia das doenças',blank=True)
    idade3               = models.CharField('Idade3?',max_length=30,blank=True)
    qual_neurologico     = models.TextField('Problemas neurológicos',blank=True)
    acomp_psicologico    = models.BooleanField('Sim/Não')
    outro_acompanha      = models.TextField('outro Acompanhamento',blank=True)
    uso_medicamento      = models.CharField('Usa Medicamentos?',max_length=30,blank=True)
    outra_ocorrencia     = models.CharField('Outras ocorrencias em saúde',max_length=30,blank=True)
    probl_mental         = models.BooleanField('Sim/Não')
    grau_parentesco      = models.CharField('Grau Parentesco',max_length=30,blank=True)
    dificul_apresentada  = models.CharField('Dificuldade apresentada',max_length=30,blank=True)
    relac_pai            = models.CharField('Realação com os Pais',max_length=30,blank=True)
    relac_irmao          = models.CharField('Relação com irmãos',max_length=30,blank=True)
    ponto_posi           = models.CharField('Pontos positivos',max_length=30,blank=True)
    ponto_nega           = models.CharField('Pontos Negativos',max_length=30,blank=True)
    terapia              = models.TextField('Entende a terapia?',blank=True)
    Observacao           = models.TextField('Oservações',blank=True)


    class Meta:
        verbose_name = 'Anaminese_crianca'
        verbose_name_plural = 'Anaminese_crianca'

    def __str__(self):
        return "{}".format(self.atendimento)

class Uroginecologia(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE, primary_key=True)
    encaminhado_por      = models.CharField('Encaminhado Por',max_length=150,blank=True)
    medico_responsavel   = models.CharField('Médico Responsável',max_length=150,blank=True)
    diagnostico_origem   = models.TextField('Diagnóstico de origem',blank=True)
    queixa               = models.TextField('Queixa Principal',blank=True)
    hda                  = models.CharField('HDA',max_length=150,blank=True)
    hpp                  = models.CharField('HPP',max_length=150,blank=True)
    antece_cirurgico     = models.CharField('Antecedentes Cirurgicos',max_length=150,blank=True)
    antece_familiar      = models.CharField('Amtecedentes Familiares',max_length=150,blank=True)
    uso_medicacao        = models.CharField('Uso de Medicamentos',max_length=150,blank=True)
    incont_urinaria      = models.BooleanField('Sim/Não')
    como_perde           = models.CharField('Como perde Urina',max_length=150,blank=True)
    quanto_perde         = models.CharField('Quanto tempo perde xixi',max_length=150,blank=True)
    como_urina           = models.CharField('Como Urina',max_length=150,blank=True)
    frequencia_perda     = models.CharField('Frequencia perda de Urina',max_length=150,blank=True)
    usa_frauda           = models.BooleanField('Sim/Não')
    frequencia_urina     = models.CharField('Frequencia da Urina',max_length=150,blank=True)
    funcao_intestinal    = models.CharField('Funcao Intestinal',max_length=150,blank=True)
    menarca              = models.CharField('Menarca',max_length=150,blank=True)
    contracepcao_tipo    = models.CharField('Contracepção/Tipo',max_length=150,blank=True)
    menopausa            = models.CharField('Menopausa/Tipo',max_length=150,blank=True)    
    gpca                 = models.CharField('GPCA',max_length=150,blank=True)
    episotomia           = models.BooleanField('Sim/Não')
    forceps              = models.BooleanField('Sim/Não')
    tempo_parto          = models.CharField('Tempo de Parto',max_length=150,blank=True)
    complicacao          = models.CharField('Complicações de Parto',max_length=150,blank=True)
    Cirurg_ginecologica  = models.CharField('Cirurgia Ginecológica',max_length=150,blank=True)
    dst                  = models.CharField('DST',max_length=150,blank=True)
    infec_urinaria       = models.CharField('Infecção Unirinária',max_length=150,blank=True)
    exame_complementar   = models.TextField('Exames Complementares',max_length=150,blank=True)
    exame_fisico         = models.TextField('Exames Fisicos',max_length=150,blank=True)
    afa                  = models.CharField('AFA',max_length=150,blank=True)
    perfect              = models.CharField('PERFECT',max_length=150,blank=True)


    class Meta:
        verbose_name = 'Uroginecologia'
        verbose_name_plural = 'Uroginecologia'

    def __str__(self):
        return "{}".format(self.atendimento)

class Neurologia(models.Model):
    atendimento      = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    diag_medico      = models.CharField('Diagnóstico Médico',max_length=30,blank=True)
    medico           = models.CharField('Médico',max_length=30,blank=True)
    diag_fisio       = models.TextField('Diagnóstico Fisioterapeuta',blank=True)
    distur_assoc     = models.TextField('Disturbios associados',blank=True)
    hda              = models.TextField('hda',max_length=100,blank=True)
    exame            = models.TextField('Exames Complementares',max_length=100,blank=True)
    cirurgia         = models.TextField('Cirurgias',max_length=100,blank=True)
    dispo_auxi       = models.TextField('Dispositivos auxiliares',max_length=100,blank=True)
    capacidade       = models.TextField('Capacidade',max_length=100,blank=True)
    pre_test         = models.TextField('Pre-Testes',max_length=100,blank=True)
    aval_video       = models.TextField('Avaliação Vídeo',max_length=100,blank=True)
    aval_postural    = models.TextField('Avaliação Postural',max_length=100,blank=True)
    adm_1            = models.CharField('adm_1',max_length=30,blank=True)
    adm_2            = models.CharField('adm_2',max_length=30,blank=True)
    adm_3            = models.CharField('adm_3',max_length=30,blank=True)
    adm_4            = models.CharField('adm_4',max_length=30,blank=True)
    adm_5            = models.CharField('adm_5',max_length=30,blank=True)
    adm_6            = models.CharField('adm_6',max_length=30,blank=True)
    adm_7            = models.CharField('adm_7',max_length=30,blank=True)
    adm_8            = models.CharField('adm_8',max_length=30,blank=True)
    articular_1      = models.CharField('articular_1',max_length=30,blank=True)
    articular_2      = models.CharField('articular_2',max_length=30,blank=True)
    articular_3      = models.CharField('articular_3',max_length=30,blank=True)
    articular_4      = models.CharField('articular_4',max_length=30,blank=True)
    articular_5      = models.CharField('articular_5',max_length=30,blank=True)
    articular_6      = models.CharField('articular_6',max_length=30,blank=True)
    articular_7      = models.CharField('articular_7',max_length=30,blank=True)
    articular_8      = models.CharField('articular_8',max_length=30,blank=True)
    encurtamento_1   = models.CharField('encurtamento_1',max_length=30,blank=True)
    encurtamento_2   = models.CharField('encurtamento_2',max_length=30,blank=True)
    encurtamento_3   = models.CharField('encurtamento_3',max_length=30,blank=True)
    encurtamento_4   = models.CharField('encurtamento_4',max_length=30,blank=True)
    encurtamento_5   = models.CharField('encurtamento_5',max_length=30,blank=True)
    encurtamento_6   = models.CharField('encurtamento_6',max_length=30,blank=True)
    encurtamento_7   = models.CharField('encurtamento_7',max_length=30,blank=True)
    encurtamento_8   = models.CharField('encurtamento_8',max_length=30,blank=True)
    tonus_1          = models.CharField('tonus_1',max_length=30,blank=True)
    tonus_2          = models.CharField('tonus_2',max_length=30,blank=True)
    tonus_3          = models.CharField('tonus_3',max_length=30,blank=True)
    tonus_4          = models.CharField('tonus_4',max_length=30,blank=True)
    tonus_5          = models.CharField('tonus_5',max_length=30,blank=True)
    tonus_6          = models.CharField('tonus_6',max_length=30,blank=True)
    tonus_7          = models.CharField('tonus_7',max_length=30,blank=True)
    tonus_8          = models.CharField('tonus_8',max_length=30,blank=True)
    forca_1          = models.CharField('forca_1',max_length=30,blank=True)
    forca_2          = models.CharField('forca_2',max_length=30,blank=True)
    forca_3          = models.CharField('forca_3',max_length=30,blank=True)
    forca_4          = models.CharField('forca_4',max_length=30,blank=True)
    forca_5          = models.CharField('forca_5',max_length=30,blank=True)
    forca_6          = models.CharField('forca_6',max_length=30,blank=True)
    forca_7          = models.CharField('forca_7',max_length=30,blank=True)
    forca_8          = models.CharField('forca_8',max_length=30,blank=True)
   
    class Meta:
        verbose_name = 'Neurologia'
        verbose_name_plural = 'Neurologia'

    def __str__(self):
        return "{}".format(self.atendimento)

class Nutricao(models.Model):
    atendimento           = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    qpdhda                = models.TextField('QPD / HDA',blank=True)
    exam_fisico           = models.TextField('Exames Físicos',blank=True)
    exam_complementar     = models.TextField('Exames Complementares',blank=True)

   
    class Meta:
        verbose_name = 'Nutricao'
        verbose_name_plural = 'Nutricao'

    def __str__(self):
        return "{}".format(self.atendimento)
        
class Guia(models.Model):
    numero           = models.CharField(max_length=20)
    convenio         = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
    paciente         = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    #profissional     = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    profissional     = models.ManyToManyField(Profissional)
    procedimento     = models.ForeignKey(Procedimento,on_delete=models.CASCADE)
    quantidade       = models.IntegerField()
    qtdautorizada    = models.IntegerField()
    validade         = models.DateField()
    data_autorizacao = models.DateField()
    tipo_guia        = models.CharField(max_length=2,choices=TIPO_GUIA)
    status           = models.CharField(max_length=1,choices=STATUS_GUIA,default='N')
    validada         = models.BooleanField(default=False)
    atualizado_em    = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em        = models.DateTimeField('Criado em', auto_now_add=True)
    ativo            = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Guia'
        verbose_name_plural = 'Guias'
        ordering            = ['quantidade']

    def __str__(self):
        return str(self.numero) + ' | ' + str(self.procedimento)+ ' | ' + str(self.quantidade)
    
    #propriedade para notificar guias vencidas com alertas
    @property
    def verifica_vencimento(self):
        data_atual      = datetime.date.today()
        futuro          = self.validade - datetime.timedelta(days=7)

        if data_atual > self.validade:
            return "Vencido"
        elif data_atual > futuro and data_atual < self.validade:
            return "Alerta"
        else:
            return "Valido"

   