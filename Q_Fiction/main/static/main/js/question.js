const url = window.location.href
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";


let phrases = {
  harrypotter: "<p>Opening The Chamber of Secrets...</p>",
  lotr: "<p>Destroying the One Ring...</p>",
  asoif: "<p>Waiting for Winter To Come...</p>"
}


$(document).ready(() => {
  console.log(bookName)
  $("#ask-btn").click(() => {
    // $(".ans").css("display", "none")
    $(".ans").css("display", "block")
    let phrase = phrases[bookName]
    $("#p-ans").html(`
    <div>
    ${phrase}
    <p class="loader"><p>
    </div>`)
    console.log('pressed')
    let question = $("#input-ques").val()
    console.log(question)
    axios.post(url, {question}).then(res => {
      $("#p-ans").html(`<p class="text-info">${res.data.ans}<p>`)
    });

  })
})