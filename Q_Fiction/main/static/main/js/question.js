const url = 'http://127.0.0.1:8000/ask-question/';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

$(document).ready(() => {
  $("#ask-btn").click(() => {
    // $(".ans").css("display", "none")
    $(".ans").css("display", "block")
    $("#p-ans").html(`
    <div>
    <p>Opening The Chamber of Secrets...</p>
    <p class="loader"><p>
    </div>`)
    console.log('pressed');
    let question = $("#input-ques").val();
    console.log(question);
    axios.post(url, {question}).then(res => {
      $("#p-ans").html(`<p class="text-info">${res.data.ans}<p>`)
    });

  })
})