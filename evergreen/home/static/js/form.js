$(".changenum").submit(function(event) {
  event.preventDefault();
  var element = event.target;
  var select = element.querySelector("select").value; 
  var button = element.querySelector("button").value; 
  document.cookie = "meal_id_"+button+"="+select+";path=/";
});