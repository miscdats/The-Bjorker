$(document).ready(function() {
        var refresh_id = setInterval(function() {
            $.get(
              "{{ url_for('process_status', job_id=job_id) }}",
              function(data) {
                console.log(data);
                if (data.data.job_status == 'completed') {
                  window.location.replace("{{ url_for('results') }}");
                }
              }
            )}
          , 1500);
      });
