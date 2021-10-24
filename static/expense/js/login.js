
function showPassword(name) {
      var x = document.getElementById(name);
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
}