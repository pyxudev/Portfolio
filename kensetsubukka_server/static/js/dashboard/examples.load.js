document.onreadystatechange = function() { 
    if (document.readyState !== "complete") { 
        document.querySelector(".body").style.visibility = "none"; 
        document.querySelector(".body").style.filter = "blur(100px)";
        // document.querySelector(".loading").style.visibility = "visible"; 
    } else { 
        var delaytime = 0;
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(10px)";
        }, delaytime);
        
        // for (var i=0;i<=10;i++){
        //     blur_num = (10-i).toString();
        //     blur_val = "blur("+blur_num+"px)";
        //     setTimeout(function() {
        //         console.log(blur_val);
        //         document.querySelector(".body").style.filter = blur_val;
        //     },i*1000);
        // }
        // NOT WORKED

        // TODO : REMOVE HARDCODED
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(9px)";
        },50);
        
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(8px)";
        }, 100);
      
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(7px)";
        }, 150);

        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(6px)";
        }, 200);
      
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(5px)";
        }, 250);
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(4px)";
        }, 300);
        
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(3px)";
        }, 350);
      
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(2px)";
        }, 400);
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(1px)";
        }, 450);
        setTimeout(function() {
            document.querySelector(".body").style.filter = "blur(0px)";
        }, 500);

        document.querySelector(".body").style.visibility = "visible"; 
    } 
}; 

