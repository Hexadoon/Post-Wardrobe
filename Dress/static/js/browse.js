var item_no = 1

$(document).ready(function () {
  load_many();
});

var filter_change = function () {
  item_no = 1;
  document.getElementById("items").innerHTML = "";
  load_many();
};

var get_item = function (count) {
  if (count == 0) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.responseText;
      if (r == "Unavailable") {
        item_no++;
        get_item(count);
      } else if (r == "No more") {
        var btn = document.getElementById("load_more");
        btn.parentNode.removeChild(btn);
        return;
      } else {
        var dp = new DOMParser();
        console.log(r);
        var c = dp.parseFromString(r, "text/html")
        var el = c.getElementsByTagName("body")[0].firstChild;
        document.getElementById("items").appendChild(el);
        item_no++;
        get_item(count - 1);
      }
    }
  }

  var form = document.getElementById("filterform");
  var fd = new FormData(form)
  fd.append("item_no", item_no);

  xhttp.open('POST', '/getitem');
  xhttp.send(fd);
  return "done";
};

var load_many = function () {
  get_item(6);
};
