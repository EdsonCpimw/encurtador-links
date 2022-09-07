$('[data-widget="pushmenu"]').on('click', function (){
        $('[data-widget="pushmenu"]').PushMenu("toggle");
});

$(function () {
  bsCustomFileInput.init();
});

$(function () {
$("#usuarios").DataTable({
  "responsive": true, "lengthChange": false, "autoWidth": false,"bDestroy": true
}).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
});

$(document).ready(function()
{
  $('#select2').select2();
});

$(document).ready( function () {
  var table = $('#example').DataTable();

  $(".dataTables_empty").text("Desculpe, nada foi encontrado!");
});

function filtroLinks(){
    valor = document.getElementById('links').value;
//    alert(valor);
    $.ajax({
        type: 'GET',
        url: '/list_link/',
        data: {
            filter: valor,
        },
        success: function(links){
            var json = JSON.stringify(links);
            console.log(links)
            console.log(json)
            $('#usuarios').DataTable().ajax.reload();
        },
        error: function(result){
           alert(result)
        }
    });
}
