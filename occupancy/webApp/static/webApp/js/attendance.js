var otable;
$(document).ready( function () {
	dynamictable();
  otable =  $('#table_id').DataTable({
      "iDisplayLength":-1,
      "bLengthChange":false,
      "scrollY":calcDataTableHeight(),
      "scrollX":true,
      "bPaginate":false,
      "bAutoWidth":false
      // ordering: false
    });
   $(window).resize(function () {
    var oSettings = oTable.fnSettings();
    oSettings.oScroll.sY = calcDataTableHeight();
    oTable.fnDraw();
  });
  setupToolbar();
  setupSubMenu();
/*  $('#download-button').click(function(){
    $('#download').toggle();
  });*/
} );

var header_dates = new Array();
var rollno = new Array();
var attendance;
var uniquerollno;
var length_col;
var numberdays;

var calcDataTableHeight = function() {
  return $(window).height()*40/100;
};

function setupSubMenu(){
  var subMenuOptions=["download","modify"];
  $('#modify-submit').click(function(){
    $('#modify-form').submit();
  });
  $.each(subMenuOptions,function(i,el){
    $('#'+el+"-button").click(function(){
      $("#"+el).toggle();
    });
    $('#'+el+"-cancel").click(function(){
      $("#"+el).toggle();
    });
  });
};
function setupToolbar(){
  $('#table_id_filter').css('float','left');
  $('#table-container').css('margin-top','5px');
  $('#table-container').css('padding-top','5px');
  $('#table-container').css('padding-left','5px');
};


function dynamictable(){
	generate_header();
	var table = document.getElementById("table_id");
	var header = table.createTHead();
	var row1 = header.insertRow(0);
	row1.insertCell(0).innerHTML = "Roll No";
	row1.insertCell(1).innerHTML = "Count(per TA)";
	for(i=0;i<header_dates.length;i++){
		row1.insertCell(i+2).innerHTML = header_dates[i];
	}
	var temp = document.getElementById("json").value;
	var json_data = JSON.parse(temp);
	for(i=0;i<json_data.attendance.length;i++){
		rollno.push(json_data.attendance[i].rollno);
	}
	uniquerollno = new Array();
	$.each(rollno, function(i, el){
    	if($.inArray(el, uniquerollno) === -1) uniquerollno.push(el);
	});
	uniquerollno.sort();
	console.log(uniquerollno);
	create_2d();
	console.log(attendance);
	var count_array = new Array(numberdays);
	for (i=0;i<numberdays;i++)
		count_array[i] = 0;
	var body = table.appendChild(document.createElement('tbody'));
	for(i=0;i<attendance.length;i++){
		var row_b = body.insertRow(i);
		row_b.insertCell(0).innerHTML = uniquerollno[i];
		row_b.insertCell(1).innerHTML = attendance[i].length;
		for(j=0;j<numberdays;j++){
			if (inArray(attendance[i],header_dates[j])){
				row_b.insertCell(j + 2).innerHTML = "Present";
				count_array[j] = count_array[j] + 1;
			}
			else 
				row_b.insertCell(j + 2).innerHTML = "Absent";
		}
	}
	// var tbody_ref = table.getElementsByTagName('tbody')[0];
	// var count_insert = tbody_ref.insertRow(tbody_ref.rows.length);
	var count_insert = body.insertRow(0);
	count_insert.insertCell(0).innerHTML = "Count(of All TAs)";
	count_insert.insertCell(1).innerHTML = " ";
	for (i=0;i<count_array.length;i++){
		count_insert.insertCell(i+2).innerHTML = count_array[i];
	}
	console.log(count_array);
}

function generate_header(){
	var long_months = new Array(0,2,4,6,7,9,11);
	var head_date = new Date();
	numberdays = head_date.getDate() - 1;
	head_date.setDate(1);
	// if (inArray(long_months,head_date.getMonth()))
	// 	length_col = 31;
	// else length_col = 30;
	for (i=0;i<numberdays;i++){
		header_dates.push(date_to_string(head_date));
			if (head_date.getDate() == length_col){
				head_date.setMonth(parseInt(head_date.getMonth()) + 1);
				head_date.setDate(1);
			}
			else head_date.setDate(parseInt(head_date.getDate()) + 1 );
	}
	// console.log(header_dates);
}

function date_to_string(date){
	var month = parseInt(date.getMonth()) + 1;
	if (String(month).length == 1)
		month = "0" + month
	var date_t = date.getDate();
	if (String(date_t).length == 1)
		date_t = "0" + date_t 
	var ret =date.getFullYear()+'-'+ month+'-'+ date_t;
	return ret;
}

function inArray(array, value) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] == value) return true;
    }
    return false;
}

function create_2d(){
	var temp = document.getElementById("json").value;
	var json_data = JSON.parse(temp);
	attendance = new Array(uniquerollno.length);
	for(i=0;i<uniquerollno.length;i++){
		attendance[i] = new Array();
	}
	for(i=0;i<json_data.attendance.length;i++){
		var index = uniquerollno.indexOf(json_data.attendance[i].rollno);
    for(j=0;j<json_data.attendance[i].present_dates.length;j++){
      attendance[index].push(json_data.attendance[i].present_dates[j]);
    }
	}
	// console.log(attendance);
}
