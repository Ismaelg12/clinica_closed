$(function () {
  $(".js-create-book").click(function () {
    $.ajax({
      url: '/adicionar/agendamento/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

});

$(function () {
  $(".js-update").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/atualizar/agendamento/'+btn.attr("id")+'/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

});