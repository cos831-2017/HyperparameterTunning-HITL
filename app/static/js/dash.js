// Shorthand for $( document ).ready()
$(function() {
  
  $("#btn-start").bind("click", function() {
    window.location.href = "/dashboard/start";
  });

  $("#btn-stop").bind("click", function() {
    window.location.href = "/dashboard/finalizeorabort";
  });

});
