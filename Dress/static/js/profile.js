var chevron_state = 0;

var change_available_status = function (item_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      if ($("#" + item_id + "_card").hasClass("darken")) {
        $("#" + item_id + "_card").removeClass("darken");
      } else {
        $("#" + item_id + "_card").addClass("darken");
      }
    }
  }
  xhttp.open('GET', '/change_available_status/' + item_id);
  xhttp.send();
};

var change_chevron = function () {
  if (chevron_state == 0) {
    $("#chevron_parent").removeClass("fa-chevron-down");
    $("#chevron_parent").addClass("fa-chevron-up");
    chevron_state = 1;
  } else {
    $("#chevron_parent").addClass("fa-chevron-down");
    $("#chevron_parent").removeClass("fa-chevron-up");
    chevron_state = 0;
  }
};

var update_file = function () {

  var uploadField = document.getElementById("item_img");

  if (uploadField.files[0].size > (25 * 1024 * 1024)) {
    uploadField.type = "text";
    uploadField.type = "file";
    uploadField.value = "";
    alert("File is too big!");
    return;
  };

  var fileandpath = $("#item_img").val();
  var filename = fileandpath.substring(fileandpath.lastIndexOf('\\') + 1, fileandpath.length);
  console.log(filename);
  $("#img_label").html(filename);
};

var check_val = function (s) {
  console.log(s);
  return (document.getElementById(s).value.trim() != '');
}

/*
  Generates a UUID

  Source:
  https://www.w3resource.com/javascript-exercises/javascript-math-exercise-23.php
*/
var create_UUID = function () {
  var dt = new Date().getTime();
  var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (dt + Math.random() * 16) % 16 | 0;
    dt = Math.floor(dt / 16);
    return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
  return uuid;
}


var add_dress = function () {
  var val_list = ['item_name', 'item_description', 'item_price'];
  var i;
  for (i of val_list) {
    if (!check_val(i)) {
      alert('You must fill out all the inputs!');
      return;
    }
  }
  if (document.getElementById("item_img").files.length == 0) {
    alert('You must fill out all the inputs!');
    return;
  }

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      location.reload();
    }
  }

  var fd = new FormData();

  fd.append('name', $("#item_name").val());
  fd.append('description', $("#item_description").val());
  fd.append('price', $("#item_price").val());
  fd.append('size', $("#item_size").val());
  fd.append('material', $("#item_material").val());
  fd.append('color', $("#item_color").val());
  fd.append('occassion', $("#item_occassion").val());
  fd.append('weather', $("#item_weather").val());
  fd.append('condition', $("#item_condition").val());

  var fileandpath = $("#item_img").val();
  var filename = fileandpath.substring(fileandpath.lastIndexOf('\\') + 1, fileandpath.length);
  filename = create_UUID() + filename;

  fd.append('src', $("#item_img")[0].files[0], filename)

  xhttp.open('POST', '/add_item');
  xhttp.send(fd);
};
