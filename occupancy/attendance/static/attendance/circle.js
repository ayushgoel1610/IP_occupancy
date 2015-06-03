//window.onload = main();
var radius = 200;
var defaultVelocities = [[1,-1],[-1,1],[1.5,1]]
var velocities = [[1,-1],[-1,1],[1.5,1]]
var coords;
var stop=false;
var stop_centre=false;
var collision=true;
var speed=50;
var updateTimer, centreTimer;
var disturbance=5;
var TIME = 10;
function main(){
  var c = document.getElementById("main-canvas");
  var ctx = c.getContext("2d");
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
  init_coords(c);
  do_move_circles();
}
function do_centre_circles(){
  clearInterval(updateTimer);
  centreTimer = setInterval(centre_circles,TIME);
}

function centre_circles(){
  collision=false;
  var close_enough = 0;
  for(var i=0;i<coords.length;i++){
    var targetY=window.innerHeight/2 - coords[i][1];
    var targetX=window.innerWidth/2 - coords[i][0];
    var dist = Math.sqrt(coords[i][0]*coords[i][1]+coords[i][1]*coords[i][1]);
    /*var rad = Math.atan2(coords[i][1],coords[i][0]);
    angle = rad / Math.PI * 180;*/
    velocities[i][0] = (targetX/dist)*speed;
    velocities[i][1] = (targetY/dist)*speed;
    console.log(targetX);
    if(Math.abs(velocities[i][0]) < 0.1 && Math.abs(velocities[i][1]) < 0.1){
      close_enough++;
    }
  }
//  clear_circles();
  add_disturbance();
  update();
 // centreTimer = setTimeout(centre_circles,10);
}
function add_disturbance(){
  for(var i=0;i<coords.length;i++){
    for(var j=0;j<2;j++){
      var rand = Math.random();
      if(rand < 0.5){
        coords[i][j] += (disturbance * Math.random());
      }
      else{
        coords[i][j] -= (disturbance * Math.random());
      }
    }
  }
}
function do_move_circles(){
  clearInterval(centreTimer);
  move_circles();
}
function move_circles(){
  collision=true;
  for(var i=0;i<velocities.length;i++){
    for(var j=0;j<2;j++){
      velocities[i][j] = defaultVelocities[i][j];
    }
  }
  draw_circles();
  updateTimer = setInterval(update,TIME);
}
function update(){
  clear_circles();
  for(var i=0;i<coords.length;i++){
    for(var j=0;j<2;j++){
      coords[i][j] += velocities[i][j];
    }
  }
  draw_circles();
  if(collision){
    for(var i=0;i<coords.length;i++){
      for(var j=0;j<2;j++){
        if(coords[i][j]<0){
          velocities[i][j] *= -1;
        }
        else if(coords[i][j]>window.innerHeight && j==1){
          velocities[i][j] *= -1;
        }
        else if(coords[i][j]>window.innerWidth && j==0){
          velocities[i][j] *= -1;
        }
      }
    }
  }
}
function init_coords(c){
  var xpos = (c.width / 2);
  var ypos = (c.height / 2);
  var delta = (radius*2)/3;
  coords = [[xpos,ypos-delta],[xpos-delta,ypos],[xpos+delta,ypos]]
}
function clear_circles(){
  var c = document.getElementById("main-canvas");
  var ctx = c.getContext("2d");
  for(var i=0;i<coords.length;i++){
    ctx.clearRect(coords[i][0]-radius-5,coords[i][1]-radius-5,radius*2+10,radius*2+10);
  }
}
function draw_circles(){
  var c = document.getElementById("main-canvas");
  var ctx = c.getContext("2d");
  var colors = ["rgba(255,92,92,0.8)","rgba(59,163,163,0.8)","rgba(189,240,86,0.8)"]
  //clear_circles();
  for( var i =0;i<coords.length; i++){
    ctx.beginPath();
    ctx.arc(coords[i][0],coords[i][1],radius,0,2*Math.PI,false);
    ctx.fillStyle = colors[i];
    ctx.fill();   
  }
  return coords;
}
