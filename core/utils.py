    # -*- coding: utf-8 -*-

TIPO_CARTAO = (
    ('VS','Visa'),
    ('MC','Mastercard'),
    ('AE','American Express'),
    ('EO','Elo')
)

CATEGORIAS = (
    ('AL','Aluguel'),
    ('EE',' Energia Elétrica'),
    ('AG','Água'),
    ('TE','Telefone')
)

RECEPTOR_PAGAMENTO = (
    ('PF','Profissional'),
    ('RC','Recepção'),
)

PARCELAS =  (
    (0, 'Escolha uma opção'),
    (1, '1x'),
    (2, '2x'),
    (3, '3x'),
    (4, '4x'),
    (5, '5x'),
    (6, '6x'),
    (7, '7x'),
    (8, '8x'),
    (9, '9x'),
    (10, '10x'),
    (11, '11x'),
    (12, '12x'),
    
)

CONVENIOS = (
    ('particular','Particular'),
    ('unimed','Unimed'),
    ('intermed','Intermed'),
    ('humanasaude','Humana Saúde'),
    ('geapsaude','Geap Saúde'),
    ('fusma','Fusma'),
    ('cassi','Cassi'),
    ('caixa_economica','Caixa Economica'),
    ('camed','Camed'),
    ('medplan','Medplan'),
    ('petrobras','Petrobrás'),
    ('capsesp','Capsesp'),
    ('bradesco','Bradesco'),
    ('assefaz','Assefaz'),
    ('correios','Correios'),
    ('pro_bomo','Pro Bomo'),
)

FORMA_PAGAMENTO = (
    ('ES','Especie'),
    ('TF','Tranferência'),
    ('CD','Cartão de Débito'),
    ('EC','Especie e Cartão'),
    ('VS','Cartão Visa'),
    ('MC','Cartão Mastercard'),
    ('AE','Cartão American Express'),
    ('CS','Cartão Credishop'),
    ('HP','Cartão HyperCard'),
    ('EO','Cartão Elo'),
)

STATUS_CONTA = (
    ('PG','Pago'),
    ('PD','Pendente'),
    ('FT','Faturado'),
    ('PC','Parcial'),
)

TIPO_ATENDIMENTO = (
    ('EV','Evolução'),
    ('AV','Avaliação'),
    ('DM','Desmarcado na Hora'),
    ('FH','Justificada na Hora'),#orange
    ('FN','Falta Não Justificada'),#grey
    ('AR','ATendido/Recepção'),#recepçao
)

RACA = (
    ('B','Branca'),
    ('P','Preta'),
    ('D','Parda'),
    ('A','Amarela'),
    ('I','Indigena'),
)

UF = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MT', 'Mato Grosso'),
    ('MA', 'Maranhão'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RS', 'Rio Grande do Sul'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins'),
)

SEXO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

ESTADO_CIVIL =(
    ('', 'Escolha Um Opçao'),
    ('S','Solteiro'),
    ('C','Casado'),
    ('D','Divorciado'),
    ('V','Viúvo'),
    ('U','União Estável')
)

STATUS =(
    ('AG','Agendado'),#green
    ('AT','Atendido'),#blue
    ('FJ','Justificada'),#yellow
    ('FH','Justificada na Hora'),#orange
    ('FN','Não Justificada'),#grey
    ('DM','Desmarcado/Profisssional'),#purple
    ('CC','Cancelado'),#red
    ('BQ','Bloqueio'),#black
    ('PT','Particular'),#08d0aa eletricblue
    ('AR','Atendido/Recepção'),#FC0FC#183693
)

AREA =(
    ('AT','Atendente'),
    ('FS','Fisioterapeuta'),
    ('TA','Terapeuta ocupacional'),
    ('FN','Fonoaudiólogo(a)'),
    ('PI','Psiquiatra'),
    ('NT','Nutricionista'),
    ('PS','Psicólogo(a)'),
    ('DT','Dentista'),
    ('EF','Educador(a) Físico(a)'),
    ('ET','Esteticista'),
    ('MT','Musicoterapeuta'),
    ('EN','Enfermeiro(a)'),
    ('PP','Psicopedagogo(a)'),
)

TIPO_GUIA =(
    ('PV','Provisoria'),
    ('PM','Permanente'),
)

STATUS_GUIA =(
    ('I','Intercambio'),
    ('N','Normal'),
)

FILHO =(
    ('', 'Escolha Um Opçao'),
    ('A','Adotivo'),
    ('B','Biológico'),
)

SAUDE_MAE =(
    ('', 'Escolha Um Opçao'),
    ('D','Doenças'),
    ('I','Inquietações'),
)

TIPO_PARTO =( 
    ('', 'Escolha Um Opçao'),
    ('N','Normal'),
    ('C', 'Cezaria'),
    ('I','Induzido'),
)

GESTACAO =( 
    ('', 'Escolha Um Opçao'),
    ('CO','Completa'),
    ('PR', 'Prematura'),
    ('PO','Pós_matura'),
)

AMAMENTACAO =( 
    ('', 'Escolha Um Opçao'),
    ('NO','Normal'),
    ('AR', 'Artificial'),
)

MATRIMONIO =( 
    ('', 'Escolha Um Opçao'),
    ('CA','Casados'),
    ('SE', 'Separados'),
)

DESCONTO =( 
    ('', 'Escolha um desconto'),
    ('CA','5'),
    ('SE', '10'),
    ('SE', '15'),
    ('SE', '20'),
    ('SE', '25'),
    ('SE', '30'),
    ('SE', '35'),
    ('SE', '40'),
    ('SE', '45'),
    ('SE', '50'),
)