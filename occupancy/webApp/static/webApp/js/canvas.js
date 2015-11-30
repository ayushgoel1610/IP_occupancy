var floor5color = "#F15C80";
var floor4color = "#8085E9";
var floor3color = "#F7A35C";
var floor2color = "#90ED7D";
var floor1color = "#434348";
var floor0color = "#7CB5EC";
var floorColors = ["#F15C80", "#8085E9", "#F7A35C", "#90ED7D", "#434348", "#7CB5EC"];

var floorIdMap = {}
var usedElevator = []
var flag = true;
var chartFlag = true;
var dateFormat = "YYYY-MM-DD-HH:mm:ss";
var numRequestsSoFar = 0;

function drawDots(floor, wing, count, uids)
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
			color=floor5color;
		else if(floor=='4')
			color=floor4color;
		else if(floor=='3')
			color=floor3color;
		else if(floor=='2')
			color=floor2color;
		else if(floor=='1')
			color=floor1color;
		else
			color=floor0color;

		var wingCount = parseInt(count);

		var buildingIndexId = "building-index";

		// $newUl = $("<ul class='list-inline'><li class='index-element'>"+floor+"</li><li class='index-element' style='padding-left:20px'>"+wing+"</li><li class='index-element' style='padding-left:20px'>"+wingCount+"</li></ul>");
		// $newUl.appendTo(find($(buildingIndexId));
		
		// var list = $(".building-index").append('<ul></ul>').find('ul');
		// list.append("<li class='index-element'>"+floor+"</li><li class='index-element' style='padding-left:20px'>"+wing+"</li><li class='index-element' style='padding-left:20px'>"+wingCount+"</li>");

		if(wing=="Cafeteria")
			wing="B";

		var floorClassName=".list-inline.floor."+floor;
		var wingClassName=".wing."+wing;
		var wingClassHeight = $(wingClassName).height();
		var wingClassWidth = $(wingClassName).width();
		var posX = (Math.random() * (wingClassWidth)).toFixed();
    	var posY = (Math.random() * (wingClassHeight)).toFixed();
		// console.log(floorClassName+" "+wingClassName + " count:" + wingCount);
		for(var i=0; i<uids.length; ++i)
		{
			// $(floorClassName).find(wingClassName).prepend($('<div class="dot"></div>'));
			var divsize = 11;
	        var posx = (Math.random() * (wingClassWidth - divsize)).toFixed();
	        var posy = (Math.random() * (wingClassHeight - divsize)).toFixed();
	        $newdiv = $("<div id = '"+uids[i]+"' class='dot' data-toggle='tooltip' onClick='get_id(this.id)' title='"+uids[i]+"'></div>").css({
	            "left": posx +"px",
	            "top": posy + "px",
	            "position":"absolute",
	            "background-color":color
	        });
	        $newdiv.appendTo($(floorClassName).find(wingClassName));
		}
	}
}

function processData(data, datetime){
	var buildingDic = {}
	var occInfo = data.occupancy_information;
	for (var key in occInfo){
		if (occInfo.hasOwnProperty(key)) {
			if (compareStrings(occInfo[key].building, "Academic")){
				var floor = occInfo[key].floor;
				var uids = occInfo[key].uids;
				var count = occInfo[key].count;
				var wing = occInfo[key].wing;
				drawDots(floor, wing, count, uids);
				if (flag)
				{
					if(floor in floorIdMap){
						var arr = floorIdMap[floor];
						floorIdMap[floor] = arr.concat(uids);
					}
					else{
						floorIdMap[floor] = uids;
					}
				}
			}
		}
	}
	console.log(floorIdMap);
	flag = false;
	addTooltip();
}

function compareStrings(str1, str2){
	if(str1 === str2){
		return true;
	}
	else{
		return false;
	}
}

function checkUidInMap(uid, currentFloor, currentWing){
	var oldFloor = parseInt(getKeyByValue(floorIdMap, uid));
	if (oldFloor > -1){
		if(currentFloor != oldFloor && currentFloor!="" && currentWing!=""){
			console.log("uid: "+uid+" changed floor from: "+oldFloor+" to: "+currentFloor);
			if (Math.abs(currentFloor - oldFloor) > 2){
				usedElevator.push(uid);
			}
			var oldColor = $('#'+uid).css("background-color");
			modifyUidMap(uid, oldFloor, currentFloor);
			redrawDot(oldColor, uid, currentFloor, currentWing);
		}
	}
	else if (currentFloor!="" && currentWing!="") {
		// appending new dots here
		var color;
		if(currentFloor=='5')
			color=floor5color;
		else if(currentFloor=='4')
			color=floor4color;
		else if(currentFloor=='3')
			color=floor3color;
		else if(currentFloor=='2')
			color=floor2color;
		else if(currentFloor=='1')
			color=floor1color;
		else
			color=floor0color;
		if(currentFloor in floorIdMap){
			var arr = floorIdMap[currentFloor];
			floorIdMap[currentFloor] = arr.concat(uid);
		}
		else{
			floorIdMap[currentFloor] = uid;
		}
		console.log('new device found, uid: '+uid);
		redrawDot(color, uid, currentFloor, currentWing);
	}
	addTooltip();
}

function redrawDot(color, uid, floor, wing){
	if($('#'+uid).length > 0){
		$('#'+uid).remove();
	}

	if(wing=="Cafeteria")
		wing="B";
	
	// console.log("color: "+color+", uid: "+uid+", floor: "+floor+", wing: "+wing);

	var floorClassName=".list-inline.floor."+floor;
	var wingClassName=".wing."+wing;
	var wingClassHeight = $(wingClassName).height();
	var wingClassWidth = $(wingClassName).width();
	var posX = (Math.random() * (wingClassWidth)).toFixed();
	var posY = (Math.random() * (wingClassHeight)).toFixed();
	var divsize = 11;
	var posx = (Math.random() * (wingClassWidth - divsize)).toFixed();
	var posy = (Math.random() * (wingClassHeight - divsize)).toFixed();
	$newdiv = $("<div id = '"+uid+"' class='dot' data-toggle='tooltip' onClick='get_id(this.id)' title='"+uid+"'></div>").css({
		"left": posx +"px",
		"top": posy + "px",
		"position":"absolute",
		"background-color":color
	});
	$newdiv.appendTo($(floorClassName).find(wingClassName));
}

function modifyUidMap(id, oldFloor, newFloor){
	var oldArray = floorIdMap[oldFloor];
	// console.log("uid to be modified: "+id);
	// console.log("oldArray before deleting: "+oldArray);
	if (typeof oldArray !== 'undefined' && oldArray.length > 0) {
		var delIndex = oldArray.indexOf(id);
		if (delIndex > -1) {
			oldArray.splice(delIndex, 1);
		}
	}
	floorIdMap[oldFloor] = oldArray;
	// console.log("oldArray after deleting: "+floorIdMap[oldFloor]);
	
	var newArray = floorIdMap[newFloor];
	// console.log("newArray before adding: "+newArray);
	if (typeof newArray !== 'undefined' && newArray.length > 0) {
		floorIdMap[newFloor] = newArray.concat(id);
	}
	// console.log("newArray after adding: "+floorIdMap[newFloor]);
	// console.log(floorIdMap);
}

function getKeyByValue(obj, value){
	for( var prop in obj ) {
		if( obj.hasOwnProperty( prop ) ) {
			var tempArr = obj[ prop ];
			if (tempArr.indexOf(value)>-1){
				return prop;
			}
			// if( obj[ prop ] === value )
		}
	}
	return -1;
}

function startDrill(token, interval){
	timeInterval = interval;
	showToken(token, processDrillData, true, timeInterval);
}

function stopDrill(){
	stopRequests();
}

function processDrillData(data, datetime){
	numRequestsSoFar = numRequestsSoFar + 1;
	var buildingDic = {}
	var occInfo = data.occupancy_information;
	for (var key in occInfo){
		if (occInfo.hasOwnProperty(key)) {
			if (compareStrings(occInfo[key].building, "Academic")){
				var floor = occInfo[key].floor;
				var uids = occInfo[key].uids;
				var wing = occInfo[key].wing;
				var count = parseInt(occInfo[key].count);
				for (var i = 0; i < uids.length; ++i){
					checkUidInMap(uids[i], floor, wing);
				}
				if(floor in buildingDic){
					var cnt = buildingDic[floor];
					buildingDic[floor] = cnt + count;
				}
				else{
					buildingDic[floor] = count;
				}
			}
		}
	}
	console.log(buildingDic);
	console.log("usedElevator: "+usedElevator);
	makeChart(buildingDic, datetime);
}

function makeChart(dic, datetime){
	if (chartFlag)
	{
		chartFlag = false;
		$(function () {
			var chart = new Highcharts.Chart({
			    chart: {
			        renderTo: 'building-chart'
			    },

			    yAxis: {
			    	title:{
			    		text: 'Number of Devices'
			    	}
			    },
			    
			    xAxis: {
			    	type: 'datetime'
			    	// tickInterval: 15 * 1000,
			    },

			    title:{
			    	text : 'Real time chart of devices in Academic Building'
			    }
			    
			});
			gChart = chart;
			addSeries(dic, datetime);
			addDataPoints(dic, datetime);
		});
	}
	else
	{
		addDataPoints(dic, datetime)
	}
}

function addSeries(dic, datetime){
	var m2 = moment(datetime, dateFormat);
	var mYear = m2.year();
	var mMonth = m2.month();
	var mDate = m2.date();
	var mHour = m2.hours()
	var mMinute = m2.minutes();
	var mSeconds = m2.seconds();
	var mMilliseconds = m2.milliseconds();
	for(var key in dic) {
	    if(dic.hasOwnProperty(key)) {
	        //key                 = keys,  left of the ":"
	        //driversCounter[key] = value, right of the ":"
	        gChart.addSeries({
	        	id : key,
				name: 'Floor '+(key),
				pointInterval:  15000,
            	pointStart: Date.UTC(mYear, mMonth, mDate, mHour, mMinute, mSeconds, mMilliseconds),
			});
	    }
	}
}

function addDataPoints(dic, datetime){
	// var ctr = 0;
	for(var key in dic) {
	    if(dic.hasOwnProperty(key)) {
	        //key                 = keys,  left of the ":"
	        //driversCounter[key] = value, right of the ":"
	        var point = [datetime, dic[key]];
	        var shiftFlag = false;
	        if (!shiftFlag && numRequestsSoFar > 8){
	        	shiftFlag = true;
	        }
	        var chartSeries = gChart.get(key);
	        chartSeries.addPoint(point, true, shiftFlag);
	        // gChart.series[ctr].addPoint(point);
	        // ctr = ctr + 1;
	    }
	}
	// console.log("ctr: "+ctr);
}

function writeElevatorIds(){
	$(".elevator-list-item").remove();
	if (usedElevator.length > 0){
		// var uList = "<ul id='elevator-list'></ul>";	// Create text with HTML
		for (var i=0; i < usedElevator.length; ++i){
			var item = "<li class='elevator-list-item list-item'>" + usedElevator[i] + "</li>";
			$(".elevator-list").append(item);
		}
		$(".elevator-list").append("<strong class='elevator-list-item list-strong'>Total: "+usedElevator.length+"</strong>");
	}
	else{
		$(".elevator-list").append("<p class='elevator-list-item list-para'>No devices recorded that may have used elevators</p>");
	}
	$('#elevator-modal').modal('show');
}

function clearVars(){
	numRequestsSoFar = 0;
	chartFlag = true;
	usedElevator = [];
}

function addTooltip(){
	$('[data-toggle="tooltip"]').tooltip();
}

