
$(document).ready(function() {
  /*++++++++++++++++++++++++++++ADD agendamento do FullCalendar++++++++++++++++++++++++*/
  addAgendamentoOnSelection = function(start, end, allDay) {
    //setando as horas no input vindo do calendario no click
    $('#hora_inicial').val(start.format('HH:mm') );
    $('#hora_fim').val(end.format('HH:mm'));
    //setando a data no input vindo do calendario no click
    $('#data_agenda').val($.fullCalendar.formatDate(start, "DD/MM/Y"));  
    $("#createEventModal").modal("show");
    $('#submitButton').on('click',function(){
    //dicionario dos dados
    $('#agendamento_form').validate({
      rules: {
        hora_inicio: { required: true, },
        hora_fim: { required: true,},
        paciente: { required: true },
        profissional: { required: true },
        convenio: { required: true },
        status: { required: true },
        telefone: { required: true },
      },
      messages: {
        hora_inicio: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        hora_fim: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        paciente: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        profissional: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        convenio: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        status: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        telefone: { required: '<span class="text-danger">Prencha esse Campo</span>' },
      },
      submitHandler: function( form ){
        var dados = $( form ).serialize();
        $.ajax({
          type: "POST",
          url: '/adicionar/agenda/',
          data: dados,
          success: function (response) {
            if(dados){
              swal({ title:"Agenda!", 
                text:"O Agendamento Foi Adicionado Com Sucesso!",
                type:"success",
                showConfirmButton: true,
                allowOutsideClick: false,
              }).then(function(){
                window.location.reload();
              })
            }

          },
          error: function(response) {
            alert('Ops..Ocorreu algum Erro :(');
          }
        });
        $('#submitButton').unbind('click');
        //$('#createEventModal').find('input').val('');
        $('#createEventModal').modal('hide');
        return false;
      }
    });
  }); 
    return false;
  }


  /*++++++++++++++++++++++++++++EventClick do FullCalendar++++++++++++++++++++++++*/
  eventClickAgendamento = function (event, jsEvent, view) {
  //lista os dados no modal para atender
  $('#modalProfissional').html(event.profissional);
  $('#modalPaciente').html(event.title);
  $('#modalConvenio').html(event.convenio);
  $('#modalCelular').html(event.celular);
  $('#modalDate').html($.fullCalendar.formatDate(event.start, "DD-MM-YYYY"));
  $('#modalStartDate').html(event.start.format('HH:mm') );
  $('#modalEndTime').html(event.end.format('HH:mm') );
  //envia pra um span no botão atualizar
  $('#id_agenda').html(event.id);
  //oculta botão conforme status
  if(event.status == 'AG' || event.status == 'BQ' || event.status == 'PT'){
    //hide buttons
    $('#add_atendimento').hide();
    $('#updateButton').show();
    $('#deleteButton').show();
  }else if(event.status == 'AD'){
    $('#add_atendimento').show();
    $('#updateButton').hide();
    $('#deleteButton').hide();
  }else{
    $('#add_atendimento').hide();
    $('#updateButton').hide();
    $('#deleteButton').hide();
  }
  var id_atender  = event.id;
  $(".atender").click(function () {
    var tipo = $(this).attr("tipo");
    var linkAtender = '/adicionar/atendimento/'+ id_atender+tipo ;
    $('.atender').attr('href', linkAtender);
  });
 //enviando dados para o modal
 $('#DetalheModal').modal("show");
 $('#deleteButton').on('click', function(e){
  e.preventDefault();
  deleteAgendamento(event);
});
 $('#updateButton').on('click', function(e){
  e.preventDefault();
  updateAgendamento(event);
});
} 

/*+++++++++++crir paciente apartir do modal++++++++++++++++++++++++*/
$('#submitSaveButton').on('click',function(){
  $('#paciente_form').validate({
    rules: {
      nome: { required: true, },
      telefone: { required: true,},
      nascimento: { required: true },
      profissional: { required: true },
      convenio: { required: true },
      cpf: { required: true },

    },
    messages: {
      nome: { required:'<span class="text-danger">Prencha esse Campo</span>'},
      telefone: { required:'<span class="text-danger">Prencha esse Campo</span>'},
      nascimento: { required: '<span class="text-danger">Prencha esse Campo</span>' },
      profissional: { required:'<span class="text-danger">Prencha esse Campo</span>'},
      convenio: { required:'<span class="text-danger">Prencha esse Campo</span>'},
      cpf: { required:'<span class="text-danger">Prencha esse Campo</span>'},
    },
    submitHandler: function( form ){
      var dados = $('#paciente_form').serialize();
      console.log(dados);
      $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: dados,
        success: function(response){
          alert('O Paciente Foi Adicionado Com Sucesso!"');
        },
        error: function(response) {
          alert('Ops..Ocorreu algum Erro :(');
        }
      });
      return false;
    }
  });
});

}); 


/*+++++++++++Update FullCalendar++++++++++++++++++++++++*/

function updateAgendamento(event){
  //data vindo do database no click sendo convertida
  var data_calendar = $.fullCalendar.formatDate(event.start, "DD/MM/YYYY");
  $("#createEventModal").modal("show");
  //desabilitar campo repetir sessoes 
  //$( "#sessoes" ).prop( "disabled", true );
  //setando dados no template vindo do banco de dados
  var data         =  $('#data_agenda').val(data_calendar);
  var horaI        =  $('#hora_inicial').val(event.start.format('HH:mm'));
  var horaF        =  $('#hora_fim').val(event.end.format('HH:mm'));
  var paciente     =  $('#paciente').selectpicker('val',event.paciente_id);
  var profissional =  $('#profissional').selectpicker('val',event.profissional_id);
  var convenio     =  $('#convenio').selectpicker('val',event.convenio_id);
  var telefone     =  $('#telefone').val(event.telefone);
  var status       =  $('#status').val(event.status);
  var sala         =  $('#sala').selectpicker('val',event.sala_id);
  var obs          =  $('#observacao').val(event.observacao);
  $('#submitButton').on('click',function(){
    $('#agendamento_form').validate({
      rules: {
        hora_inicio: { required: true, },
        hora_fim: { required: true,},
        paciente: { required: true },
        profissional: { required: true },
        convenio: { required: true },
        status: { required: true },
        telefone: { required: true },
      },
      messages: {
        hora_inicio: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        hora_fim: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        paciente: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        profissional: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        convenio: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        status: { required: '<span class="text-danger">Prencha esse Campo</span>' },
        telefone: { required: '<span class="text-danger">Prencha esse Campo</span>' },
      },
      submitHandler: function( form ){
        var dados = $( form ).serialize();
        //pega o id do agendamento no span
        var id    = $('#id_agenda').text();
        $.ajax({
          type: "POST",
          url: '/update/agendamento/'+id+'/calendar/',
          data: dados,
          success: function (response) {
            if(dados){
              swal({ title:"Agenda!", 
                text:"O Agendamento Foi Atualizado Com Sucesso!",
                type:"success",
                showConfirmButton: true,
                allowOutsideClick: false,
              }).then(function(){
                window.location.reload();
              })
            }
          },
          error: function(response) {
            alert('Ops..Ocorreu algum Erro :(');
          }
        });
        $('#submitButton').unbind('click');
        //$('#createEventModal').find('input').val('');
        $('#createEventModal').modal('hide');
        return false;
      }
    });
  });   
  return false;  
}

/*+++++++++++delele FullCalendar++++++++++++++++++++++++*/
function deleteAgendamento(event){
  if (confirm("Você tem certeza que quer deletar esse agendamento?")) {
    var id     = event.id;
    var status = event.status;
    $.ajax({
      type: "GET",
      url: '/deletar/agendamento/calendar',
      data: {'id': id,'status':status},
      dataType: "json",
      success: function (data) {
        alert('Agendamento Removido Com Sucesso!');
      },
      failure: function (data) {
        alert('There is a problem!!!');
      }

    });
      location.reload();
  }
}
