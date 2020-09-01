$(document).ready(function() {
    var refresh_id = setInterval(function() {
        $.get(
          "{{ url_for('process_status') }}", job_id=appConfig.job_id,
          function(data) {
            console.log('Data: ', data);
            if (data.finished == "true") {
                window.location.replace("{{ url_for('results') }}", job_id=data.data.job_id);
            }
          }
        )}
      , 1500);
  });
