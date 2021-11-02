$('#id_type').on('change', function() {
  if(this.value != 1)
  {
    $("#id_doctorid").prop("disabled", false);
  }
  else
  {
    $("#id_doctorid").prop("disabled", true);
  }
});

$( document ).ready(function() {
    $("#id_doctorid").prop("disabled", true);
});