$("#id_clinicid").change(function () {
      var urldoctor = $("#bookappointmentform").attr("data-doctor-url");  
      var urlslots = $("#bookappointmentform").attr("data-slots-url");  
      var clinicId = $(this).val();  

      $.ajax({                       
        url: urldoctor,                   
        data: {
          'clinicid': clinicId       
        },
        success: function (data) { 
          $("#id_doctorid").empty();  
          $("#id_doctorid").html(data);  
        }
      });

      $.ajax({                       
        url: urlslots,                   
        data: {
          'clinicid': clinicId       
        },
        success: function (data) {   
          $("#id_appt-min").empty();
          $("#id_appt-min").html(data);  
        }
      });

});