// var text ='{"size":"60","occupancy_information":[{"building":"Academic","floor":"0","wing":"C","room":"C01","count":"93"},{"building":"Academic","floor":"0","wing":"C","room":"C02","count":"13"},{"building":"Academic","floor":"0","wing":"C","room":"C03","count":"13"},{"building":"Academic","floor":"0","wing":"Cafeteria","room":"CCD","count":"1"},{"building":"Academic","floor":"0","wing":"Cafeteria","room":"GlassRoom","count":"2"},{"building":"Academic","floor":"1","wing":"A","room":"","count":"2"},{"building":"Academic","floor":"1","wing":"B","room":"","count":"4"},{"building":"Academic","floor":"1","wing":"C","room":"C11","count":"53"},{"building":"Academic","floor":"1","wing":"C","room":"C12","count":"11"},{"building":"Academic","floor":"1","wing":"C","room":"C13","count":"7"},{"building":"Academic","floor":"1","wing":"Middle","room":"","count":"8"},{"building":"Academic","floor":"2","wing":"A","room":"","count":"9"},{"building":"Academic","floor":"2","wing":"B","room":"","count":"6"},{"building":"Academic","floor":"2","wing":"C","room":"C21","count":"39"},{"building":"Academic","floor":"2","wing":"C","room":"C22","count":"6"},{"building":"Academic","floor":"2","wing":"C","room":"C23","count":"8"},{"building":"Academic","floor":"2","wing":"C","room":"C24","count":"11"},{"building":"Academic","floor":"2","wing":"Middle","room":"","count":"1"},{"building":"Academic","floor":"3","wing":"A","room":"","count":"10"},{"building":"Academic","floor":"3","wing":"B","room":"","count":"9"},{"building":"Academic","floor":"3","wing":"Middle","room":"","count":"1"},{"building":"Academic","floor":"4","wing":"A","room":"","count":"15"},{"building":"Academic","floor":"4","wing":"B","room":"","count":"4"},{"building":"Academic","floor":"5","wing":"A","room":"","count":"4"},{"building":"Academic","floor":"5","wing":"B","room":"","count":"2"},{"building":"Boy sHostel","floor":"0","wing":"A","room":"","count":"1"},{"building":"Boy sHostel","floor":"0","wing":"C","room":"","count":"6"},{"building":"Boy sHostel","floor":"1","wing":"A","room":"","count":"10"},{"building":"Boy sHostel","floor":"1","wing":"C","room":"","count":"1"},{"building":"Boy sHostel","floor":"2","wing":"A","room":"","count":"2"},{"building":"Boy sHostel","floor":"2","wing":"B","room":"","count":"9"},{"building":"Boy sHostel","floor":"2","wing":"C","room":"","count":"12"},{"building":"Boy sHostel","floor":"3","wing":"A","room":"","count":"2"},{"building":"Boy sHostel","floor":"3","wing":"B","room":"","count":"8"},{"building":"Boy sHostel","floor":"3","wing":"C","room":"","count":"16"},{"building":"Boy sHostel","floor":"4","wing":"A","room":"","count":"4"},{"building":"Boy sHostel","floor":"4","wing":"B","room":"","count":"4"},{"building":"Boy sHostel","floor":"4","wing":"C","room":"","count":"11"},{"building":"Boy sHostel","floor":"5","wing":"A","room":"","count":"7"},{"building":"Boy sHostel","floor":"5","wing":"C","room":"","count":"15"},{"building":"Boy sHostel","floor":"6","wing":"A","room":"","count":"15"},{"building":"Boy sHostel","floor":"6","wing":"C","room":"","count":"10"},{"building":"Girl sHostel","floor":"0","wing":"A","room":"","count":"2"},{"building":"Girl sHostel","floor":"1","wing":"A","room":"","count":"2"},{"building":"Girl sHostel","floor":"1","wing":"B","room":"","count":"10"},{"building":"Girl sHostel","floor":"1","wing":"C","room":"","count":"2"},{"building":"Girl sHostel","floor":"2","wing":"A","room":"","count":"2"},{"building":"Girl sHostel","floor":"2","wing":"B","room":"","count":"4"},{"building":"Girl sHostel","floor":"3","wing":"A","room":"","count":"7"},{"building":"Girl sHostel","floor":"3","wing":"B","room":"","count":"6"},{"building":"Girl sHostel","floor":"3","wing":"C","room":"","count":"6"},{"building":"Girl sHostel","floor":"4","wing":"A","room":"","count":"2"},{"building":"Library","floor":"0","wing":"","room":"","count":"12"},{"building":"Library","floor":"1","wing":"","room":"","count":"8"},{"building":"Library","floor":"2","wing":"","room":"","count":"7"},{"building":"Library","floor":"3","wing":"","room":"","count":"4"},{"building":"Residence","floor":"","wing":"","room":"","count":"3"},{"building":"ServiceBlock","floor":"0","wing":"","room":"","count":"4"},{"building":"StudentCentre","floor":"0","wing":"","room":"","count":"7"},{"building":"StudentCentre","floor":"3","wing":"","room":"","count":"2"}]}';

// obj = JSON.parse(text);
var obj;
var weekday = new Array(7);
var param_time, t;
var chart_dates = new Array(7);
var x_axis_params = new Array(7);
var minDate = "";
$(document).ready(function(){
  
  var flag = document.getElementById("hidden").value;
  if(flag == "on")
    displaychart1();
  else{
    displaychart2();
    // while (minDate == ""){
    //   // console.log("entered");
    // }
    $('#overlay').fadeOut(6000);
  }
});

// window.onload = displaychart;
function print_filter(filter){
  var f=eval(filter);
  if (typeof(f.length) != "undefined") {}
  else{}
  if (typeof(f.top) != "undefined") {f=f.top(Infinity);}
  else{}
  if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}
  else{}
  console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
}
//function initCounts(){
var curr_building;
var curr_floor;
var all_building;
var all_floor;
var buildingDim;
var BuildingChart;
var floorDim;
var wingDim;
var FloorChart;
var WingChart;
var class_count;
var classDim;
var classChart;
var filter_again = false;
var ndx;
var titles = document.getElementsByClassName('chart-title');
var title_text = ["Building","Floor","Wing","Room"];

function building_helper(chart,filter){
    var elem = document.getElementById("building-helper");
    var sum = buildingDim.groupAll().reduceSum(function(d){
      for(i=0;i<chart.filters().length;i++){
        if(d.building == chart.filters()[i])
          return d.count;
      }
      return 0;
    }).value();
    if(sum == 0) sum = all_building;
    elem.innerHTML= "Building: "+ sum; 
    console.log(sum);
    curr_building = sum;
    floor_helper(FloorChart,filter);
};
function floor_helper(chart,filter){
  var elem = document.getElementById("floor-helper");
  var sum = floorDim.groupAll().reduceSum(function(d){
    for(i=0;i<chart.filters().length;i++){
      if(d.floor == chart.filters()[i] || (chart.filters()[i] == 'N/A' && d.floor == ''))
        return d.count;
    }
    return 0;
  }).value();
  if(sum == 0) sum = curr_building;
  elem.innerHTML= "Floor: "+ sum; 
  curr_floor = sum;
  wing_helper(WingChart,filter);
};
function wing_helper(chart,filter){
    var elem = document.getElementById("wing-helper");
    var sum = wingDim.groupAll().reduceSum(function(d){
      for(i=0;i<chart.filters().length;i++){
        if(d.wing == chart.filters()[i] || (chart.filters()[i] == 'N/A' && d.wing == ''))
          return d.count;
      }
      return 0;
    }).value();
    if(sum == 0) sum = curr_floor;
    elem.innerHTML= "Wing: "+ sum; 
    curr_floor = sum;
};
function hide_chart(chart){
      Dim = ndx.dimension(function(d){;});
      var count = Dim.group().reduceCount(function(d){return 0;});
      chart.dimension(Dim);
      chart.group(count);
      chart.render();
}

function chain_chart(schart){
  var node;
  var ParentChart;var child = null;
  var Dim;var oldDim;
  var chart;
  if(schart == "Floor"){
    chart = FloorChart;
    FloorChart.filterAll();
    FloorChart.dimension().dispose();
    node = 1;
    ParentChart = BuildingChart;
    child = WingChart;
    oldDim = floorDim;
    if(ParentChart.filters().length>0)
      Dim =  ndx.dimension(function(d){ if(d.building == ParentChart.filters()[0]) return d.floor; });
    else{
      Dim = null;
    }
  }
  else if(schart =="Wing"){
    chart = WingChart;
    WingChart.filterAll();
    WingChart.dimension().dispose();
    node = 2;
    ParentChart = FloorChart;
    child = classChart;
    oldDim = wingDim;
    if(ParentChart.filters().length>0){
      Dim = ndx.dimension(function(d){ console.log(">>"+ParentChart.filters()[0]);if(d.floor == ParentChart.filters()[0] && d.building == BuildingChart.filters()[0]){console.log(d.wing +" "+d.floor); if(d.wing == "") return "N/A"; else return d.wing; }});
    }
    else {
      Dim = null;
    }
  }
  else if(schart == "Room"){
    chart = classChart;
    classChart.filterAll();
    classChart.dimension().dispose();
    node = 3;
    ParentChart = WingChart;
    oldDim = classDim;
    if(ParentChart.filters().length >0){
      Dim =  ndx.dimension(function(d){ if((d.wing == ParentChart.filters()[0] || (d.wing == "" && ParentChart.filters()[0] ==  "N/A")) && d.floor == FloorChart.filters()[0] && d.building == BuildingChart.filters()[0]) { if(d.room == "") return "N/A"; else return d.room; }});
    }
    else{
      Dim = null;
    }
  }
  else{
    return;
  }
  if( Dim != null){
    var count = Dim.group().reduceSum(function(d){return d.count;});
    //chart.filterAll();
    chart.dimension(Dim);
    chart.group(count);
    chart.render();
    titles[node].innerHTML = title_text[node];
  }
  else {
    titles[node].innerHTML = "Select " + title_text[node-1];
    hide_chart(chart);
  }
  if(node+1<title_text.length)
    chain_chart(title_text[node+1]);
}

function displaychart2(){
  t = $('input[name=userTime]');
  var current_time = new Date();
  var month = parseInt(current_time.getMonth()) + 1;
  if (t.val() == ""){
    param_time = current_time.getFullYear()+'-'+ month+'-'+current_time.getDate()+'-'+current_time.getHours()+':'+current_time.getMinutes()+':'+current_time.getSeconds();
  }
  else {
    param_time = current_time.getFullYear()+'-'+ month+'-'+current_time.getDate()
    param_time = param_time +'-' + t.val();
    param_time = param_time.replace('T','-');
    param_time = param_time + ":00";
  }
  console.log(param_time);
  d3.csv("/template/month_average/" + param_time, function(error,data){
    ndx = crossfilter(data);
    // print_filter(ndx);
    var BH = "Boy's Hostel";
    var format = d3.time.format("%Y-%m-%d %H:%M:%S");
    var dayDim = ndx.dimension(function(d) {return format.parse(d.day);});
    var A_day_count = dayDim.group().reduceSum(function(d){return d.Acad;});
    var BH_day_count = dayDim.group().reduceSum(function(d){return d.BH;});
    var GH_day_count = dayDim.group().reduceSum(function(d){return d.GH;});
    var L_day_count = dayDim.group().reduceSum(function(d){return d.L;});
    var R_day_count = dayDim.group().reduceSum(function(d){return d.R;});
    var SC_day_count = dayDim.group().reduceSum(function(d){return d.SC;});
    var SB_day_count = dayDim.group().reduceSum(function(d){return d.SB;});
    // print_filter(BH_day_count);
    minDate = (new Date(dayDim.bottom(1)[0].day));
    var maxDate = (new Date(dayDim.top(1)[0].day));
    console.log(minDate);
    console.log(maxDate);
    var past_linechart = dc.compositeChart("#past-linechart");
    past_linechart
      // .xUnits(dc.units.ordinal)
      .width(1100).height(300)
      // .margins({top: 5, left: 10, right: 10, bottom: 20})
      // .useYBaseline(true)
      .dimension(dayDim)
      // .x(d3.time.scale().domain(d3.extent(data, function(d) { return d.day; })))
      // .x(d3.scale.ordinal().range([minDate,maxDate]))
      .x(d3.time.scale().domain([minDate,maxDate]))
      .y(d3.scale.linear())
      .brushOn(false)
      .title(function(d){
      return d.key
      + "\nNumber of People: " + d.value;
      })
      .xAxisLabel("Date")
      .yAxisLabel("Devices in Campus (approx)")
      .transitionDuration(500)
      // .renderArea(true)
      .legend(dc.legend().x(1100).y(10).itemHeight(13).gap(5))
      // .centerBar(true)    
      // .gap(60)
      .elasticY(true)
      .valueAccessor(function (d) {
        return d.value;
      });
      // .xAxisPadding(10)
      // .xAxis();
      past_linechart.compose([
        dc.lineChart(past_linechart).group(A_day_count, "Academic").colors('red'),
        dc.lineChart(past_linechart).group(BH_day_count,"Boy's Hostel").colors('blue'),
        dc.lineChart(past_linechart).group(GH_day_count,"Girl's Hostel").colors('green'),
        dc.lineChart(past_linechart).group(R_day_count,"Residence").colors('yellow'),
        dc.lineChart(past_linechart).group(L_day_count,"Library").colors('black'),
        dc.lineChart(past_linechart).group(SC_day_count,"Service Block").colors('orange'),
        dc.lineChart(past_linechart).group(SB_day_count,"Service Centre").colors('gray')
      ])
      ;

      dc.renderAll();
  });
  
// console.log("done");
}

function displaychart1(){
  
  weekday[0]=  "Sun";
  weekday[1] = "Mon";
  weekday[2] = "Tues";
  weekday[3] = "Wed";
  weekday[4] = "Thurs";
  weekday[5] = "Fri";
  weekday[6] = "Sat";
  t = $('input[name=userTime]');
  type = $('#ChooseType').val();
  // console.log(type);
  var week_day;
  
  var current_time = new Date();
  var month = parseInt(current_time.getMonth()) + 1;
  if (t.val() == ""){
    param_time = current_time.getFullYear()+'-'+ month+'-'+current_time.getDate()+'-'+current_time.getHours()+':'+current_time.getMinutes()+':'+current_time.getSeconds();
    week_day = current_time.getDay();
    x_axis_params =  gen_xaxis(week_day,0);
    console.log(Date(param_time));
  }
  else {
    param_time = t.val();
    param_time = param_time.replace('T','-');
    param_time = param_time + ":00";
    var for_day = new Date(t.val());
     console.log(for_day);
     console.log(param_time);
    week_day = for_day.getDay();
    x_axis_params =  gen_xaxis(week_day,1);
  }
  console.log(param_time);
  
  if (type == "W" || type == "")
    url = "/template/past_week_data/";
  else url = "/template/past_same_day/";

  d3.csv(url+param_time, function(error, data){

      // console.log(data);
      ndx = crossfilter(data);
      var dayDim = ndx.dimension(function(d) {return d.day;});
      var day_count = dayDim.group().reduceSum(function(d){return d.count;});
      var past_linechart = dc.barChart("#past-barchart");
      buildingDim = ndx.dimension(function(d){ return d.building;});
      var total_count = buildingDim.group().reduceSum(function(d){ return d.count;});
      BuildingChart = dc.pieChart("#chart-building");
      floorDim = ndx.dimension(function(d){ return d.floor;});
      var floor_count = floorDim.group().reduceSum(function(d){return d.count;});
      FloorChart = dc.pieChart("#chart-floor");

      wingDim = ndx.dimension(function(d){  if(d.wing == "") return "N/A";return d.wing;});
      var wing_count = wingDim.group().reduceSum(function(d){return d.count;});
      WingChart = dc.pieChart("#chart-wing");

      classDim = ndx.dimension(function(d){ if(d.room == "") return "N/A"; return d.room;});
      class_count = classDim.group().reduceSum(function(d){return d.count;});
      classChart = dc.pieChart("#chart-room");
      d3.select('#past-barchart').selectAll("rect.bar").append("text").text(function(d){return d.count;})

      // document.getElementById("building-helper").innerHTML = "Building: " + all;
      // document.getElementById("floor-helper").innerHTML = "Floor: " + all ;
      // document.getElementById("wing-helper").innerHTML = "Wing: " + all ;
      // document.getElementById("room-helper").innerHTML = "Room: " + all ;

      past_linechart
      .xUnits(dc.units.ordinal)
      //.xUnits(d3.time.hours)
      //.xUnits(dc.units.ordinal)
      .width(900).height(300)
      .dimension(dayDim)
      .group(day_count)
      .filter(chart_dates[6])
       // .x(d3.time.scale().domain([minDate,maxDate]))
      .x(d3.scale.ordinal().domain(chart_dates))
      .y(d3.scale.linear())
      //.brushOn(false)
      // .onClick(function(chart){chart.filter("Monday")})
      .xAxisLabel("Date")
      .yAxisLabel("Devices in Campus (approx)")
      .transitionDuration(500)
      // .centerBar(true)    
      .gap(60)
      .elasticY(true)
      .elasticX(true)
      .xAxisPadding(10)
      .on("filtered",function(chart,filter){
            if(filter != null){
              //console.log(chart.filters());
              if(chart.filters().length == 0){
                chart.filterAll();
              }
              else if(!filter_again){
                filter_again = true;
                chart.filterAll();
                chart.filter(filter);
              }
              else{
                filter_again = false;
              }
            }
              
      })
      .renderlet(function (chart) {
        
        //Check if labels exist
        var gLabels = chart.select(".labels");
        if (gLabels.empty()){
            gLabels = chart.select(".chart-body").append('g').classed('labels', true);
        }
        
        var gLabelsData = gLabels.selectAll("text").data(chart.selectAll(".bar")[0]);
        
        gLabelsData.exit().remove(); //Remove unused elements
        
        gLabelsData.enter().append("text") //Add new elements
        
        gLabelsData
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .text(function(d){
            if (type == "" || type == "W"){
              var ind = chart_dates.indexOf(d3.select(d).data()[0].data.key);
              return x_axis_params[ind];
            }
            else return weekday[week_day];
        })
        .attr('x', function(d){ 
            return +d.getAttribute('x') + (d.getAttribute('width')/2); 
        })
        .attr('y', function(d){ return +d.getAttribute('y') + 15; })
        .attr('style', function(d){
            if (+d.getAttribute('height') < 18) return "display:none";
        });
        
    })
      
      .xAxis().tickFormat();
      // .selectAll("rect.bar").append("text").text(function(d){return d;});
      var filter_again_building = false;

      BuildingChart
        .width(200).height(200)
        .dimension(buildingDim)
        .group(total_count)
        .innerRadius(50)
        .renderLabel(true)
        .label(function (d){
          label = d.value;
          return label;
        })
        .legend(dc.legend().x(205).y(20).itemHeight(200/9).gap(2))
        .ordinalColors(["#ffcccc", "#ff9999", "#ff6666", "#ff3333","#ff0000","#cc0000","#990000"])
        .on("filtered",function(chart,filter){
            if(filter != null){
              //console.log(chart.filters());
              if(chart.filters().length == 0){
                chart.filterAll();
                chain_chart("Floor");
//                reset_chart(chart,filter,"floor");
/*                var select = 0;
                floorDim = ndx.dimension(function(d){ if(select == 0){select++;return "Building";}else if (select == 1) { select++; return "1st Select";} });
                var fcount =floorDim.group().reduceSum(function(d){return 1;});
                FloorChart.dimension(floorDim);
                FloorChart.group(fcount);
                FloorChart.render();*/
             }
              else if(!filter_again_building){
                filter_again_building = true;
                chart.filterAll();
                chart.filter(filter);
//                reset_chart(chart,filter,"floor");
            }
              else{
                filter_again_building=false;
                chain_chart("Floor");
              }
            }
          });
        var filter_again_floor = false;

        FloorChart
          .width(200).height(230)
          .dimension(floorDim)
          .group(floor_count)
          .innerRadius(50)
          .renderLabel(true)
          .label(function (d){ return d.value;})
          //.label(buildingDim)
          .legend(dc.legend().x(205).y(20).itemHeight(200/9).gap(2))
          .ordinalColors(["#99ccff", "#66b3ff", "#3399ff", "#0080ff","#0066cc","#004d99","#003366"])
          .on("filtered",function(chart,filter){
            if(filter != null){
              //console.log(chart.filters());
              if(chart.filters().length == 0){
                chart.filterAll();
                chain_chart("Wing");
              }
              else if(!filter_again_floor){
                filter_again_floor = true;
                chart.filterAll();
                chart.filter(filter);
//                wingDim = 
              }
              else{
                filter_again_floor = false;
                chain_chart("Wing");
              }
            }
          });
          var filter_again_wing = false;

          WingChart
            .width(200).height(230)
            .dimension(wingDim)
            .group(wing_count)
            .innerRadius(50)
            .renderLabel(true)
            //.label(buildingDim)
            .label(function (d){ return d.value;})
            .legend(dc.legend().x(205).y(20).itemHeight(200/9).gap(2))
            .ordinalColors(["#1a3300", "#336600", "#4c9900", "#66cc00","#339900","#008000"])
            .on("filtered",function(chart,filter){
            if(filter != null){
              // console.log(chart.filters());
              if(chart.filters().length == 0){
                chart.filterAll();
                chain_chart("Room");
              }
              else if(!filter_again_wing){
                filter_again_wing = true;
                chart.filterAll();
                chart.filter(filter);
              }
              else{
                filter_again_wing = false;
                chain_chart("Room");
              }
            }
          });
            var filter_again_class = false;
            classChart
             .width(200).height(200)
             .dimension(classDim)
             .group(class_count)
             .innerRadius(50)
             .renderLabel(true)
             //.label(buildingDim)
             .label(function (d){ return d.value;})
             .legend(dc.legend().x(205).y(20).itemHeight(200/9).gap(2))
             .on("filtered",function(chart,filter){
              if(filter != null){
                // console.log(chart.filters());
                if(chart.filters().length == 0){
                  chart.filterAll();
                  }
                  else if(!filter_again_class){
                    filter_again_class = true;
                    chart.filterAll();
                    chart.filter(filter);
                  }
                  else{
                    filter_again_class = false;
                  }
                }
              });
             // .colors(d3.scale.category10());
             // .ordinalColors(["#1a3300", "#336600", "#4c9900", "#66cc00","#339900","#008000"]);

      dc.renderAll();
      chain_chart("Floor");
      past_linechart.renderlet(function(chart){
        //displayDateChart();
      });
  });
}

function gen_xaxis(day,flag){
  var i = 0;
  var index;
  var temparray = new Array(7);
  if (type != "M"){
    for (i=0;i<7;i++){
      if (flag==0){
        var temp = Date(param_time);
        temp = new Date(temp);
      }
      else var temp = new Date(t.val());
      //console.log(temp);
      if ((day-i)<0)
        index = 7 + (day-i);
      else index = day - i;
      temparray[6 - i] = weekday[index];
      temp.setDate(temp.getDate() - i);;
      chart_dates[6-i] = formattime(temp);
    }
 }
 else {
  for (i=0;i<7;i++){
      if (flag==0){
        var temp = Date(param_time);
        temp = new Date(temp);
      }
      else var temp = new Date(t.val());
      temp.setDate(temp.getDate() - i*7);;
      chart_dates[6-i] = formattime(temp);
    }
 }
  // console.log(temparray);
  // console.log(chart_dates);
  return temparray;
}
function formattime(time){
  var dd = time.getDate();
  var mm = time.getMonth()+1; //January is 0!

    var yyyy = time.getFullYear();
    if(dd<10){
        dd='0'+dd
    } 
    if(mm<10){
        mm='0'+mm
    } 
    var today = mm+'/'+dd+'/'+yyyy;
    return today;

}
// function displayDateChart() {
//   console.log("entered");
//    var $chart = $('#past-linechart'),
//    bar  = $chart.find('.bar');
   
//     bar.each(function (i, item) {
//         var bar_top    = 300;
//         var bar_left   = this.width.baseVal.value + this.width.baseVal.value/100 + 30;
//         var bar_offset_x = 30;
//         var bar_offset_y = 33;
        
//         //var bar_val = $(this).find('title').html().split(':')[1];
//         var bar_val = chart_dates[i];
        
//         $chart.append('<div class="val" style="bottom:'+(bar_top+bar_offset_y)+'px;left:'+((bar_left*i)+(bar_offset_x))+'px;width:'+bar_left+'px">'+bar_val+'</div>');
                
//     });
// }


