$(document).ready(function() {
    let process = "{{ url_for('process_status', job_id=appConfig.job_id) }}";
    console.log('Process: ' + process);
    var refresh_id = setInterval(function() {
        $.get(
          process,
            {job_id:appConfig.job_id},
          function(data) {
            console.log('Data: ', data);
            if (data.finished == "true") {
                let results = "{{ url_for('results', job_id=data.data.job_id) }}";
                console.log('Results : ' + results);
                window.location.replace(results,
                    {job_id:data.data.job_id});
            }
          }
        )}
      , 1500);
  });
