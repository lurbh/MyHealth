$('#id_viewtype').on('change', function() {
  if(this.value == "calender")
  {
    $("#calendar").toggle();
    $("#scheduletable").toggle();
  }
  else if(this.value == "list") 
  {
    $("#scheduletable").toggle();
    $("#calendar").toggle();
  }
});

$( document ).ready(function() {
    $("#scheduletable").hide();
});

// superhero, slate , darky

// $(document).ready(function() {

//   var today = new Date();
//   var dd = String(today.getDate()).padStart(2, '0');
//   var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
//   var yyyy =  String(today.getFullYear());

//   today = yyyy + '/' + mm + '/' + dd;

  
//   $('#calendar').fullCalendar({
//     header: {
//       left: 'prev,next today',
//       center: 'title',
//       right: 'month,basicWeek,basicDay'
//     },
//     defaultDate: today,
//     themeSystem: 'bootstrap',
//     navLinks: true, // can click day/week names to navigate views
//     editable: false,
//     eventLimit: true, // allow "more" link when too many events
//     eventColor: '#9DCEDF',
//     eventTextColor: 'black',
//     backgroundColor: 'white',
//     // eventTimeFormat: {
//     //   hour: '2-digit',
//     //   minute: '2-digit',
//     //   hour12: 'false '
//     // },
//     events: [
//     {
//         title: 'All Day Event',
//         start: '2021-10-01',
//         display: 'background',
//         backgroundColor:'red',
//         borderColor:'black'
//     },
//     {
//         title: 'Meeting',
//         start: '2021-10-12T10:30:00',
//         end: '2021-10-12T12:30:00'
//       }
//     ]
//   });
// });