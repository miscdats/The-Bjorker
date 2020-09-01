$(document).ready(function() {
    console.log('Process: ' + appConfig.process);
    var refresh_id = setInterval(function() {
        $.get(
          appConfig.process,
          function(data) {
            console.log('Data: ', data);
            let job_status = data.data.job_status;
            if (job_status == "failed" || job_status == 'finished') {
                console.log('Results : ' + appConfig.results);
                window.location.replace(appConfig.results,
                    {job_id:data.data.job_id, job:data});
            }
          }
        )}
      , 3000);
  });
