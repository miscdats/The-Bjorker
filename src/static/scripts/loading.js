$(document).ready(function() {
    var path_name = window.location.pathname;
    var n = path_name.lastIndexOf('/');
    var job_id = path_name.substring(n + 1);
    var refresh_id = setInterval(function() {
        $.get(
          "{{ url_for('process_status', job_id=" + job_id + ") }}",
          function(data) {
            console.log(data);
            if (data.finished === True) {
              window.location.replace("{{ url_for('results', job_id= " + job_id + ") }}");
            }
          }
        )}
      , 1500);
  });
