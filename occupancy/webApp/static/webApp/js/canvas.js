$(document).ready(function(){
});

function drawDots(floor, wing, count)
{
	// var newDiv = document.createElement('div');
	// newDiv.className = 'dot';
	// var floorClassName="list-inline floor "+floor;
	// var wingClassName="wing "+wing;
	// console.log(floorClassName+" "+wingClassName);
	// document.getElementsByClassName(floorClassName)[0].getElementsByClassName(wingClassName)[0].appendChild(newDiv);
	if(floor!="" && wing!="")
	{
		var color;
		if(floor=='5')
			color="#3FADAB";
		else if(floor=='4')
			color="#808080";
		else if(floor=='3')
			color="#666666";
		else if(floor=='2')
			color="#4D4D4D";
		else if(floor=='1')
			color="#333333";
		else
			color="#000000";

		if(wing=="Cafeteria")
			wing="B";

		var floorClassName=".list-inline.floor."+floor;
		var wingClassName=".wing."+wing;
		var wingCount = parseInt(count);
		var wingClassHeight = $(wingClassName).height();
		var wingClassWidth = $(wingClassName).width();
		var posX = (Math.random() * (wingClassWidth)).toFixed();
    	var posY = (Math.random() * (wingClassHeight)).toFixed();
		// console.log(floorClassName+" "+wingClassName + " count:" + wingCount);
		for(i=0; i<wingCount; ++i)
		{
			// $(floorClassName).find(wingClassName).prepend($('<div class="dot"></div>'));
			var divsize = 11;
	        var posx = (Math.random() * (wingClassWidth - divsize)).toFixed();
	        var posy = (Math.random() * (wingClassHeight - divsize)).toFixed();
	        $newdiv = $("<div class='dot'></div>").css({
	            "left": posx +"px",
	            "top": posy + "px",
	            "position":"absolute",
	            "background-color":color
	        });
	        $newdiv.appendTo($(floorClassName).find(wingClassName));
		}
	}
}
