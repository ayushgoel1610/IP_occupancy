$(document).ready(function(){
	console.log("Request js working!!! ");
});

var dateFormat = "YYYY-MM-DD-HH:mm:ss";
var intervalId = 0;

function showToken(token, methodName, shouldRepeat, timeInterval) {
	startRequests(token, methodName, shouldRepeat);
	if (shouldRepeat){
		intervalId = setInterval(function() { startRequests(token, methodName); }, timeInterval);
	}
}

function startRequests(token, methodName){
	var datetime = getDateTime();
	makeRequest(datetime, token, methodName);
}

function stopRequests(){
	clearInterval(intervalId);
}

function getDateTime() {
	var m = moment();
	var dateString = m.format(dateFormat);
	return dateString;
}

function makeRequest(datetime, token, methodName)
{
	var ApiUrl = "https://192.168.1.40:9136/count?at="+datetime.toString()+"&format=yyyy-mm-dd-hh24:mi:ss&type=bfwru&token="+token.toString();
	console.log(ApiUrl);
	$.getJSON(ApiUrl)
	.done(function( data ) {
		methodName(data, datetime);
	});
}