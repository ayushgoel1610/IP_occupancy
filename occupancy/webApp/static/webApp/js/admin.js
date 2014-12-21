var json_data;
var otable;
var rollnos = new Array();
$(document).ready( function () {
	var temp = document.getElementById("json").value;
	json_data = JSON.parse(temp);
	createTable();
  otable =  $('#table_id').DataTable({
      "iDisplayLength":-1,
      "bLengthChange":false,
      "scrollY":calcDataTableHeight(),
      "scrollX":true,
      "bPaginate":false
    	// ordering: false
    });
 	// $('td').click( function() {
  //   console.log("clicked");
  // } );
  setupToolbar();
  setupSubMenu();
} );
var calcDataTableHeight = function() {
  return $(window).height()*40/100;
};
$(window).resize(function () {
  var oSettings = oTable.fnSettings();
  oSettings.oScroll.sY = calcDataTableHeight(); 
  oTable.fnDraw();
});  
function setupSubMenu(){
  setupSubMenuButtons();
  setupSubMenuAutoComplete();
};

function setupSubMenuAutoComplete(){
  var select = document.getElementById('add-mac-rollno');
  var select2 = document.getElementById('del-mac-rollno');
  select.options.length = 0;
  select2.options.length = 0;
  select.options.add(new Option("Select Roll Number","null"));
  select2.options.add(new Option("Select Roll Number","null"));
  for (var i=0;i< rollnos.length;i++){
    var d = rollnos[i];
    select.options.add(new Option(d,i));
    select2.options.add(new Option(d,i));
  }
  select = document.getElementById('del-mac-mac');
  select.options.length = 0;
  select.options.add(new Option("Select Roll number","null"));
  $('#del-mac-rollno').change(function(){
    var index = parseInt($('#del-mac-rollno').val());
    $('#del-mac-mac').empty();
    for(var i=0;i<json_data.TAs[index].macs.length;i++){
      select.options.add(new Option(json_data.TAs[index].macs[i],json_data.TAs[index].macs[i]));
    }
  });
};

function setupSubMenuButtons(){
  var subMenuOptions=["add","add-mac","upload","del-mac"];
  $('#add-submit').click(function(){
    $('#add-form').submit();
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

function toTitleCase(str)
{
  return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function createTable(){
	var table = document.getElementById("table_id");
	var header = table.createTHead();
	var row1 = header.insertRow(0);
	row1.insertCell(0).innerHTML = "Roll Number";
  row1.insertCell(1).innerHTML = "Name";
	row1.insertCell(2).innerHTML = "Batch";
	row1.insertCell(3).innerHTML = "MAC addresses";
  row1.insertCell(4).innerHTML = "Email";
	row1.insertCell(5).innerHTML = "Modify";
	row1.insertCell(6).innerHTML = "Delete";
	var body = table.appendChild(document.createElement('tbody'));
	var mod = document.createElement("input");
	mod.type = "submit";
	mod.value = "modify";
	for(i=0;i<json_data.TAs.length;i++){
		var row = body.insertRow(i);
    var ta = json_data.TAs[i];
		row.insertCell(0).innerHTML = ta.rollno.toUpperCase();rollnos.push(ta.rollno.toUpperCase());
		row.insertCell(1).innerHTML = toTitleCase(ta.name);
    row.insertCell(2).innerHTML = toTitleCase(ta.batch);
    row.insertCell(3).innerHTML = ta.macs;
    row.insertCell(4).innerHTML = ta.email;
		row.insertCell(5).innerHTML = '<button type = "submit" id =' + i +', class="btn btn-default" onClick = "modifyForm(event, this.id)">modify</button>';
		row.insertCell(6).innerHTML = '<button type = "submit" id =' + i +', class="btn btn-default" onClick = "deleteTA(this.id)">delete</button>';

	}
}
var min_tags = 2;
function addMAC(){
	var form_element = document.getElementById("TAform");
	var input = document.createElement("input");
	input.type = "text";
	input.setAttribute("class", "form-control")
	input.placeholder = "M.A.C address";
	// input.required = true;
	form_element.appendChild(input);
	min_tags = min_tags + 1;
	// $('.dropdown-toggle').dropdown().addClass('open');
	// e.stopPropagation();
	
}

function removeMAC(){
	if (min_tags < 3) return;
	var form_element = document.getElementById("TAform");
	form_element.removeChild(form_element.lastChild);
	min_tags = min_tags - 1;	
	// e.stopPropagation();
}

function submitForm(){
		var form_element = document.getElementById("TAform");
		// console.log(form_element.getElementsByTagName("input").length);
		var mac = "";
		for (i=0;i<form_element.getElementsByTagName("input").length;i++){
			if (form_element.getElementsByTagName("input")[i].value == "" || form_element.getElementsByTagName("input")[i].value.length < 4  ){
				alert("Insufficient Data");
				return;
			}
			else{
				if (i==0)
					var roll_number = form_element.getElementsByTagName("input")[i].value;
				else{
					 mac = mac + form_element.getElementsByTagName("input")[i].value;
					 mac = mac + ",";
					}
			}
			
		}
		mac = mac.substring(0, mac.length - 1);
		console.log(roll_number);
		console.log(mac);
		var r = confirm("Submit TA details?");
		if (r == true) {
			window.open("/template/admin_insert/" + roll_number + "/" + mac, "_self");
			// location.href = "/template/admin_insert/" + roll_number + "/" + mac;
			
		}
		else{
			return;
		}
	
}

function modifyForm(e, id){
	//console.log(json);
	var dropdown = document.getElementById("TAdropdown");
	// $("a.dropdown-toggle").dropdown("toggle");
	// $('.dropdown-menu').show();
	// $('.dropdown-toggle').addClass('open');
     // $('.dropdown-toggle').dropdown();  
     // e.stopPropagation();
     // $('[data-toggle="dropdown"]').parent().dropdown('toggle');
     // $('.dropdown-menu').dropdown('toggle');
     // $('#TAdropdown').trigger('click.bs.dropdown');
     console.log(json_data.TA[parseInt(id)]);
     console.log(id);
     var form_element = document.getElementById("TAform");
     form_element.getElementsByTagName("input")[0].value = json_data.TA[parseInt(id)].TA;
     var mac = json_data.TA[parseInt(id)].mac;
     var split_ar = mac.split(",");
     console.log(split_ar.length);
     form_element.getElementsByTagName("input")[1].value = split_ar[0];
     for(i=1;i<split_ar.length;i++){
     	if (split_ar.length +1 != min_tags)
     		addMAC(event);
     	form_element.getElementsByTagName("input")[i+1].value = split_ar[i];
     }
 
     $('.dropdown-toggle').dropdown().dropdown('toggle');
    e.stopPropagation();

}

// $('button').on('click', function (e) {
//     e.stopPropagation();
//     $(this).next('.dropdown').find('[data-toggle=dropdown]').dropdown('toggle');
// });

function deleteTA(id){
	var r = confirm("Do you want remove this TA from database(can be restored later)");
	if (r == true) {
		var ta = json_data.TA[parseInt(id)].TA;
		window.open("/template/admin_delete/" + ta, "_self");
		// window.open("www.google.com", "_self");
	    
	} else {
	    return;
	}
		

}

function testMac(mystring){
	var regex = /^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$/;

	console.log(regex.test(mystring));
}
