  $(document).ready(function () {
      var calendar = $('#fullCalendar').fullCalendar({
          weekends: false,
          dragScroll: false,
          defaultView: 'agendaWeek', 
          minTime: '08:00:00',
          maxTime: '20:00:00',
          header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
          },
          /*eventos para chamar o modal de detalhes */
         eventRender: function(event, element) {
      $(element).tooltip({title: event.title});             
    },
    //opção de click no evento para redirecionar para modal
      eventClick: function (event, jsEvent, view) {
        $('#modalProfissional').html(event.profissional);
        $('#modalPaciente').html(event.title);
        $('#modalConvenio').html(event.convenio);
        $('#modalCelular').html(event.celular);
        $('#modalDate').html($.fullCalendar.formatDate(event.start, "DD-MM-YYYY"));
        $('#modalStartDate').html(event.start.format('h:mm') );
        $('#modalEndTime').html(event.end.format('h:mm') );
        var id_atender = event.id;
        var tp = $('.atender').attr('tipo');
        var linkAtender = '/adicionar/atendimento/'+ id_atender+ tp;
        $('.atender').attr('href',linkAtender);
        //eniviando dados para o modal
        $('#DetalheModal').modal("show");//changed just for demo purposes

      },
          events: [
          {% for event in agenda %}
            {
              profissional: "{{ event.profissional}}",
              convenio: "{{ event.convenio}}",
              celular: "{{ event.telefone}}",
              title: "{{ event.paciente}}",
              start: '{{ event.data|date:"Y-m-d" }}T{{event.hora_inicio}}',
              end: ' {{ event.data|date:"Y-m-d" }}T{{event.hora_fim}}',
              color: '{% if event.status == 'AT'%} blue {%endif%}',
              id: '{{ event.id }}',
              allDay:false,
            },
          {% endfor %}
          ],
          selectable: true,
          selectHelper: true,
          editable: true,
          eventLimit: true,
      
          select: function(start, end, allDay){
            
          $.ajax({
            type: 'get',
            dataType:'json',
            beforeSend: function () {
              //$("#cadastrar_agenda .modal-content").html("");
              $("#createEventModal").modal("show");
            },
            success: function (data) {
              $("#createEventModal .modal-content").html(data.html_form);
            }
          });
          //data vindo do calendario no click
          var data_calendar = $.fullCalendar.formatDate(start, "Y-MM-DD");
          //dhoras vindo calendario no click
          var start_date    = $('#fullCalendar').fullCalendar('getView').start
          var end_date      = $('#fullCalendar').fullCalendar('getView').end
          //alert('Time block is between ' + start.format() + ' and ' + end.format());
          //setando as horas no input vindo do calendario
          $('#hora_inicial').val(start.format('h:mm') );
          $('#hora_fim').val(end.format('h:mm'));
         //setando a data no input vindo do calendario
          $('#data_agenda').val($.fullCalendar.formatDate(start, "DD/MM/Y"));
          $('#submitButton').on('click',function(){
            //dicionario dos dados
            var formData = {             
              'data':data_calendar,
              'hora_inicio': $('#hora_inicial').val(),
              'hora_fim': $('#hora_fim').val(),
              'sessoes': $('#sessoes').val(),
              'paciente': $('#paciente').val(),
              'profissional': $('#profissional').val(),
              'sala': $('#sala').val(),
              'convenio': $('#convenio').val(),
              'status': $('#status').val(),
              'telefone': $('#telefone').val(),
              'observacao': $('#observacao').val()
             }
          if( $('#data').val() == '' ){
              alert("Campo data é obrigatório");
            } else if( $('#hora_inicio').val() == '' ){
              alert("Campo hora inicial é obrigatório");
            } else if( $('#hora_fim').val() == '' ){
              alert("Campo hora final é obrigatório");
            } else if( $('#sessoes').val() == '' ){
              alert("Campo sessoes é obrigatório");
            } else if( $('#paciente').val() == '' ){
              alert("Campo paciente é obrigatório");
            } else if( $('#profissional').val() == '' ){
              alert("Campo profissional é obrigatório");
            } else if( $('#convenio').val() == '' ){
              alert("Campo convenio é obrigatório");
            } else if( $('#status').val() == '' ){
              alert("Campo status é obrigatório");
            } else if( $('#telefone').val() == '' ){
              alert("Campo Telefone é obrigatório");
            }else {

              $.ajax({
              url: '/adicionar/agenda/',
              data:formData,
              dataType: 'json',
              success: function(data){
                if (data){
                  swat("Adicionando");
                  console.log('Dados salvos')
                } else {
                  $('#createEventModal .modal-content').html(data.html_form)
                }
              }
          })
          $('#submitButton').unbind('click');
          $('#createEventModal').modal('hide');
          location.reload();

        }
           
     });   
      return false;
    },

    });
  });



   function deleteAgendamento(event){
    if (confirm("Are you sure you want to remove it?")) {
      var id = event.id;
      $.ajax({
        type: "GET",
        url: '/deletar/agendamento/calendar',
        data: {'id': id},
        dataType: "json",
        success: function (data) {
          calendar.fullCalendar('refetchEvents');
          alert('Agendamento Removido');
        },
        failure: function (data) {
          alert('There is a problem!!!');
        }
      });
      location.reload();
    }
  }


  jQuery(function($){
    $.noConflict();
    $('.hora_agenda').daterangepicker({
    singleDatePicker: true,
    timePicker: true,
    timePicker24Hour: true,
    timePickerIncrement: 05,
    timePickerSeconds: false,
    minDate: ' 07:00:00',
    maxDate: ' 20:00:00',
    locale: {
        format: 'HH:mm'
    }
    }).on('show.daterangepicker', function (ev, picker) {
        picker.container.find(".calendar-table").hide();
    });
  $('#telefone').mask('(00) 00000-0000');
});