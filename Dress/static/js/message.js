var url = window.location.href;
if (url.charAt(url.length - 1) == '/') {
  url = url.substring(0, url.length - 1);
}

/* Name */
const name = url.substring(url.lastIndexOf('/') + 1, url.length);

var scroll_down = function () {
  //  $("#message_box").scrollTop($("#message_box")[0].scrollHeight);
  $('#msgs').scrollTop($('#msgs')[0].scrollHeight);
}

$(document).ready(function () {
  get_messages();
  $("#msg").keypress(function (e) {
    if (e.which == 13) {
      $("#send").click();
      e.preventDefault();
    };
  });
});

var get_messages = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.responseText;
      var dp = new DOMParser();
      console.log(r);
      var c = dp.parseFromString(r, "text/html")
      var el = c.getElementsByTagName("body")[0].firstChild;
      document.getElementById("message_box").innerHTML = "";
      document.getElementById("message_box").appendChild(el);
      scroll_down();
    }
  }
  var fd = new FormData();
  fd.append('recipient', name)
  xhttp.open('POST', '/get_messages');
  xhttp.send(fd);
};

var send_message = function () {
  var msg = $("#msg").val().trim();
  if (msg == "") return;
  var fd = new FormData();
  fd.append('msg', msg)
  fd.append('recipient', name)

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      get_messages();
    }
  }

  xhttp.open('POST', '/send_message');
  xhttp.send(fd);

  $('#msg').val("");

}
