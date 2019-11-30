$(".changenum").submit(function(event) {
  event.preventDefault();
  var element = event.target;
  var select = element.querySelector("select").value; 
  var button = element.querySelector("button").value; 
  var url=document.URL.split("?")[0];
  $.post('orders/'+button+'/'+select+'/update', {})
});