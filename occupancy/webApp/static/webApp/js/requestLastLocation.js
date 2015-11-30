$(document).ready(function(){
	console.log("RequestLastLocation js working!!! ");
});

function getLastLocationData(uid, num, token, methodName)
{
	var lastnUrl = "https://192.168.1.40:9199/lastn?uid="+uid.toString()+"&last="+num.toString()+"&token="+token.toString();
	console.log(lastnUrl);
	$.getJSON(lastnUrl)
	.done(function( data ) {
		methodName(data);
	});
}

function parseFloors(data){
	floorList = [];
	var lastnObj = data['Last n connections'];
	for (var key in lastnObj){
		if(lastnObj.hasOwnProperty(key)){
			var floorNum = getFloor(lastnObj[key].label)
			if (floorNum == null){
				break;
			}
			else{
				floorList.push("Floor "+floorNum);
			}
		}
	}
	populateModal(floorList);
}

function getFloor(str){
	if(typeof str !== 'undefined'){
		if (str.substring(0,3) === 'ACB')
		{
			return str.substring(3,4);
		}
		else {
			return null;
		}
	}
	else{
		return null;
	}
}

function populateModal(floorList){
	$(".last-location-list-item").remove();
	if (floorList.length > 0){
		for (var i=0; i < floorList.length; ++i){
			var item = "<li class='last-location-list-item list-item'>" + floorList[i] + "</li>";
			$(".last-location-list").append(item);
		}
	}
	else{
		$(".last-location-list").append("<p class='last-location-list-item list-para'>No last location recorded within the Academic building</p>");
	}
	$('#last-location-modal').modal('show');
}