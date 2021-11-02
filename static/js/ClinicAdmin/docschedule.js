$(document).ready(function () {

    $('.timepicker').timepicker({
      timeFormat: 'HH:mm ',
      interval: 60,
      minTime: '00:00',
      maxTime: '23:00',
      dynamic: false,
      dropdown: true,
      scrollbar: false
    }); 
})

