(function(){
  var root=document.getElementById("sumSlide");if(!root)return;
  var C=JSON.parse(document.getElementById("calcData").textContent);
  var el=function(i){return document.getElementById(i)};
  var rate=el("cRate"),down=el("cDown"),wage=el("cWage");
  function calc(){
    var r=+rate.value/100,d=+down.value/100,w=1+(+wage.value)/100;
    var years=C.price*1000*d/(C.wage*w*12*r);
    el("cRateV").textContent=rate.value+"%";el("cDownV").textContent=down.value+"%";el("cWageV").textContent="+"+wage.value+"%";
    el("cYears").textContent=years.toFixed(1);el("cV2").textContent=years.toFixed(1);
    var need=C.price*1000*d/(C.wage*w*12*C.years2000)*100;
    el("cNeed").textContent=need.toFixed(0)+"%";
    var max=Math.max(C.years2024*1.12,years*1.08,C.years2000*1.1);
    el("cB0").style.width=(C.years2000/max*100)+"%";el("cB1").style.width=(C.years2024/max*100)+"%";el("cB2").style.width=Math.max(years/max*100,1)+"%";
    el("cB2").style.background=years<=C.years2000*1.001?"#3ddbc4":"#ffc857";
    if(window.__scn)window.__scn(years);
  }
  [rate,down,wage].forEach(function(n){n.addEventListener("input",calc);n.addEventListener("keydown",function(e){e.stopPropagation()})});
  el("cReset").addEventListener("click",function(){rate.value=20;down.value=25;wage.value=0;calc();this.blur()});
  calc();
  new MutationObserver(function(){if(root.classList.contains("active"))calc()}).observe(root,{attributes:true,attributeFilter:["class"]});
})();
