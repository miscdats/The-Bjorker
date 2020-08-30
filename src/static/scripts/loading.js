$(document).ready(function() {
        var refresh_id = setInterval(function() {
            $.get(
              "{{ url_for('process_status') }}",
              function(data) {
                console.log(data);
                if (data.status == 'completed') {
                  window.location.replace("{{ url_for('results') }}");
                }
              }
            )}
          , 1000);
      });
