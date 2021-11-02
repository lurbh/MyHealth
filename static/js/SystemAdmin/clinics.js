$(document).on('click', '.confirm-delete', function(){
  var elm  = $(this);
  var objectID = elm.data('object-id');
  var answer = confirm('Are you sure you want to delete this?');
  if (answer) {
    alert(objectID)
    //var url = "{% url 'sadmindeleteclinic' %}";
    //document.location.href = url + "/" + id;
  }
})