$(document).ready(function(){
	console.log("Jquery working!!! ");
	start();
	var myVar = setInterval(start, 15000);
});

var gToken;
var gChart;
var flag = true;
var dateFormat = "YYYY-MM-DD-HH:mm:ss";
var requestCtr = 0;

function showToken(token) {
	gToken = token;
}

function start(){
	var datetime = getDateTime();
	makeRequest(datetime);
}

function getDateTime() {
	// today = new Date();
	// var m1 = moment();
	// m1Str = m1.toString();
	var m = moment();
	// var m1 = m.format("YYYY-MM-DD-HH:mm:ss");
	var dateString = m.format(dateFormat);
	return dateString;
}

function makeRequest(datetime)
{
	var ApiUrl = "https://192.168.1.40:9136/count?at="+datetime.toString()+"&format=yyyy-mm-dd-hh24:mi:ss&type=bfwru&token="+gToken.toString();
	console.log(ApiUrl);
	// $.ajax({
	// 	url: API,
	// 	type: 'GET',
	// 	dataType: 'json',
	// 	success: function(data) { console.log(data); },
	// 	error: function() { console.log	('boo!'); },
	// 	beforeSend: setHeader
	// });

	// $.ajaxSetup({
	// 	headers : {   
	// 		'Access-Control-Allow-Origin': '*'
	// 	}
	// });
	$.getJSON(ApiUrl)
	.done(function( data ) {
		processData(data, datetime);
	});
}

function processData(data, datetime){
	requestCtr = requestCtr + 1;
	var buildingDic = {}
	// var buildingList = []
	var occInfo = data.occupancy_information;
	for (var key in occInfo){
		if (occInfo.hasOwnProperty(key)) {
			if (compareStrings(occInfo[key].building, "Academic")){
				var floor = occInfo[key].floor;
				var floorCnt = parseInt(occInfo[key].count);
				// if (typeof buildingList[floor] === 'undefined'){
				// 	buildingList[floor] = floorCnt;
				// }
				// else{
				// 	var cnt = buildingList[floor];
				// 	buildingList[floor] = cnt + floorCnt;
				// }
				if(floor in buildingDic){
					var cnt = buildingDic[floor];
					buildingDic[floor] = cnt + floorCnt;
				}
				else{
					buildingDic[floor] = parseInt(occInfo[key].count);
				}
			}
		}
	}
	console.log(buildingDic);
	makeChart(buildingDic, datetime);
}

function compareStrings(str1, str2){
	if(str1 === str2){
		return true;
	}
	else{
		return false;
	}
}

function makeChart(dic, datetime){
	if (flag)
	{
		flag = false;
		console.log("New Chart!!!");
		$(function () {
			var chart = new Highcharts.Chart({
			    chart: {
			        renderTo: 'chart4'
			    },
			    
			    xAxis: {
			    	type: 'datetime',
			    },

			    title:{
			    	text : 'Number of devices in Academic Building'
			    }
			    
			});
			gChart = chart;
			addSeries(dic, datetime);
			addDataPoints(dic, datetime);
		});
	}
	else
	{
		console.log("Old Chart!!!");
		addDataPoints(dic, datetime);
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
				name: 'Floor '+(key),
				pointInterval:  15000,
            	pointStart: Date.UTC(mYear, mMonth, mDate, mHour, mMinute, mSeconds, mMilliseconds),
			});
	    }
	}
}

function addDataPoints(dic, datetime){
	var ctr = 0;
	for(var key in dic) {
	    if(dic.hasOwnProperty(key)) {
	        //key                 = keys,  left of the ":"
	        //driversCounter[key] = value, right of the ":"
	        var point = [datetime, dic[key]];
	        var shiftFlag = false;
	        if (!shiftFlag && requestCtr>5){
	        	shiftFlag = true;
	        }
	        gChart.series[key].addPoint(point, true, shiftFlag);
	        ctr = ctr + 1;
	    }
	}
}