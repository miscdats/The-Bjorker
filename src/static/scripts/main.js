$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('.btn').on('click', function() {
  $.ajax({
    url: '/analyze',
    data: { type: $(this).data.value() },
    method: 'POST'
  })
  .done((res) => {
    getStatus(res.data.job_id)
  })
  .fail((err) => {
    console.log(err)
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/analyze/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`
    $('.resulting').prepend(html);
    const jobStatus = res.data.job_status;
    if (jobStatus === 'completed' || jobStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.job_id);
    }, 1500);
  })
  .fail((err) => {
    console.log(err)
  });
}
