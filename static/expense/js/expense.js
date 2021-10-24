
 function check() {
    var selection = document.getElementById("id_type");
    var user_select = selection.options[selection.selectedIndex].text;
    if (user_select != "Expense") {
      document.getElementById("div_id_expense_category").style.display = "none";
       document.getElementById("new_category").style.display = "none";
    }
    else {
      document.getElementById("div_id_expense_category").style.display = "block";
      document.getElementById("new_category").style.display = "none";
    }
  }