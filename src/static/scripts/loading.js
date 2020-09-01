$(document).ready(function() {
    console.log('Process: ' + appConfig.process);
    var refresh_id = setInterval(function() {
        $.get(
          appConfig.process,
          function(data) {
            console.log('Data: ', data);
            if (data.finished == "true") {
                console.log('Results : ' + appConfig.results);
                window.location.replace(appConfig.results,
                    {job_id:data.data.job_id, job:data});
            }
          }
        )}
      , 3000);
  });
