function click(n)
{
  var urls=[["topic1.html"],["topic2.html"],["topic3.html"],["topic4.html"],["topic4.html"],["topic5.html"],["topic6.html"]];
  var urls1=["index1.html","index2.html","index3.html","index4.html","index5.html","index.html","index.html"]
  var frame=document.getElementById("frame");
  var frame1=document.getElementById("frame1");
  frame.src=urls[n];
  frame1.src=urls1[n]
}

function MM_jumpMenu(targ,selObj,restore){
eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'"); 
if (restore) selObj.selectedIndex=0; 
} 


		