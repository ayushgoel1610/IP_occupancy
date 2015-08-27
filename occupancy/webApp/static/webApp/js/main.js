var x = [1,1,1];

$(document).ready(function(){
  // parseTime();
    var max_fields= [3,3,3]; //maximum input boxes allowed
    // var wrapper         = $(".time_div"); //Fields wrapper
    // var add_button      = $(".add_button"); //Add button ID
    var valid = false;
    var position,inputName;

     //initlal text box count
    // $("button").click(function(e){ //on add input button click
    //     e.preventDefault();
    //     if(x < max_fields){ //max input box allowed
    //         x++; //text box increment
    //         $(wrapper).append('<div><input class = "time_dialog" type="datetime-local" name="userTime'+x+'"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
    //     }
    // });
    
    // $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
    //     e.preventDefault(); $(this).parent('div').remove(); x--;
    // });
    var wrapper;
    $("button").click(function(e){ //on add input button click
      if(this.id == "add_button0")
      {
        position=0;
        valid = true;
        inputName="courseTime0";
      }
      else if(this.id == "add_button1")
      {
        position=1;
        valid=true;
        inputName="courseTime1";
      }
      else if(this.id == "add_button2")
      {
        position=2;
        valid=true;
        inputName="courseTime2";
      }

      if(valid)
        {
          wrapper = $(this).parent('div');
            e.preventDefault();
            if(x[position] < max_fields[position]){ //max input box allowed
                x[position]++; //text box increment
                console.log(inputName);
                $(wrapper).append('<input class = "time_dialog" type = "datetime-local" name = '+inputName+'>'); //add input box
            }
            valid=false;
        }
      });

      $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        console.log("remove called");
          e.preventDefault(); $(this).parent('div').remove(); x[position]--;
      })
      
});
