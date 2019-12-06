$(".changenum").submit(function(event) {
  event.preventDefault();
  var element = event.target;
  var select = element.querySelector("select").value; 
  var button = element.querySelector("button").value; 
  document.cookie = "meal_id_"+button+"="+select+";path=/";
  var selectPrice = document.querySelectorAll("#cart .s_price")
  var dish = document.querySelectorAll("#cart h3")
  var selectvalue = document.querySelectorAll("#cart select")
  var totalprice = 0;
  for (i = 0; i < selectPrice.length; i++) {
  	var str = selectPrice[i].innerText
  	var price = str.match(/[+-]?\d+(?:\.\d+)?/).map(Number);
  	var number = selectvalue[i].value
    var dishname = dish[i].innerText.split(":")[0];
    dishprice = number*price
    dishprice = dishprice.toFixed(2)
      console.log(dishname)
    $(dish[i]).html( dishname + ": " + dishprice + "$")
	  totalprice = totalprice + price*number
  	// console.log(price)
  	// console.log(number)
	}
	totalprice = totalprice.toFixed(2)
	// console.log(totalprice)
	$(".control h3").html("total price: " + totalprice + "$")

});

$(".addtocart").submit(function(event) {
  var element = event.target;
  var select = element.querySelector("select").value; 
  var button = element.querySelector("button").value; 
  document.cookie = "meal_id_"+button+"="+select+";path=/";
});