$(document).ready(function() {
    var job_id = data;
    var refresh_id = setInterval(function() {
        $.get(
          "{{ url_for('process_status', job_id=" + job_id + ") }}",
          function(data) {
            console.log(data);
            if (data.finished) {
              window.location.replace("{{ url_for('results', job_id= " + job_id + ") }}");
            }
          }
        )}
      , 1500);
  });
