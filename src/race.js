(function(){
  var sec=document.getElementById("raceSlide");if(!sec)return;
  var cv=document.getElementById("raceCv"),ctx=cv.getContext("2d"),D=JSON.parse(document.getElementById("raceData").textContent),N=D.years.length;
  var pos=0,playing=false,speed=1,last=0,dpr=Math.min(devicePixelRatio||1,2),wasActive=false;
  var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  var S=[{k:"price_idx",c:"#ffc857",n:"דירה"},{k:"wage_idx",c:"#3ddbc4",n:"שכר"},{k:"cpi_idx",c:"#ff6b6b",n:"מחירים"}];
  var yMax=Math.max.apply(null,D.price_idx)*1.06;
  var el=function(i){return document.getElementById(i)},rng=el("rRange"),btn=el("rPlay");
  function size(){var w=cv.clientWidth,h=cv.clientHeight;if(!w)return;cv.width=w*dpr;cv.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
  function X(i,w){return w-34-(i/(N-1))*(w-68)}
  function Y(v,h){return h-28-(v-90)/(yMax-90)*(h-50)}
  function val(k,p){var a=Math.floor(p),b=Math.min(a+1,N-1),t=p-a;return D[k][a]+(D[k][b]-D[k][a])*t}
  function draw(){
    var w=cv.clientWidth,h=cv.clientHeight;if(!w)return;ctx.clearRect(0,0,w,h);
    ctx.font="12px Assistant, sans-serif";ctx.textBaseline="middle";
    [100,200,300].forEach(function(v){var y=Y(v,h);ctx.strokeStyle="rgba(255,255,255,.09)";ctx.beginPath();ctx.moveTo(34,y);ctx.lineTo(w-34,y);ctx.stroke();ctx.fillStyle="rgba(233,236,255,.55)";ctx.textAlign="left";ctx.fillText(String(v),2,y)});
    [0,12,24].forEach(function(i){ctx.fillStyle="rgba(233,236,255,.55)";ctx.textAlign="center";ctx.fillText(String(D.years[i]),X(i,w),h-8)});
    var ip=Math.floor(pos);
    S.forEach(function(s){
      ctx.save();ctx.shadowColor=s.c;ctx.shadowBlur=14;ctx.strokeStyle=s.c;ctx.lineWidth=3.2;ctx.lineJoin="round";ctx.beginPath();
      for(var i=0;i<=ip;i++){var x=X(i,w),y=Y(D[s.k][i],h);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)}
      var hx=X(pos,w),hy=Y(val(s.k,pos),h);ctx.lineTo(hx,hy);ctx.stroke();ctx.restore();
      var pulse=playing?1+.25*Math.sin(performance.now()/160):1;
      ctx.fillStyle=s.c;ctx.beginPath();ctx.arc(hx,hy,5*pulse,0,7);ctx.fill();
      ctx.textAlign="right";ctx.fillStyle=s.c;ctx.fillText(s.n+" "+Math.round(val(s.k,pos)),hx-9,hy-(s.k==="price_idx"?10:(s.k==="wage_idx"?-4:-16)));
    });
    ctx.strokeStyle="rgba(255,255,255,.25)";ctx.setLineDash([3,4]);ctx.beginPath();ctx.moveTo(X(pos,w),12);ctx.lineTo(X(pos,w),h-24);ctx.stroke();ctx.setLineDash([]);
    var lastEv=null;
    (D.events||[]).forEach(function(e){var i=e.year-D.years[0],x=X(i,w),passed=pos>=i-.001;
      ctx.fillStyle=passed?"rgba(255,255,255,.85)":"rgba(255,255,255,.25)";ctx.beginPath();ctx.arc(x,h-22,passed?3.5:2.5,0,7);ctx.fill();
      if(passed)lastEv=e});
    el("rEvent").textContent=lastEv?lastEv.text:"—";
    el("rYear").textContent=D.years[Math.round(pos)];
    el("rPrice").textContent=Math.round(val("price_idx",pos));el("rWage").textContent=Math.round(val("wage_idx",pos));el("rCpi").textContent=Math.round(val("cpi_idx",pos));
    el("rSave").textContent=val("years_to_save",pos).toFixed(1);
    rng.value=Math.round(pos/(N-1)*1000);
  }
  function setPlay(v){playing=v;btn.textContent=v?"⏸":(pos>=N-1?"↻":"▶");btn.setAttribute("aria-label",v?"השהיה":"הפעלה")}
  function loop(ts){
    requestAnimationFrame(loop);
    var act=sec.classList.contains("active");
    if(act&&!wasActive){size();pos=reduce?N-1:0;last=ts;setPlay(!reduce)}
    wasActive=act;if(!act)return;
    var dt=Math.min((ts-last)/1000,.1);last=ts;
    if(playing){pos+=dt*speed*2.4;if(pos>=N-1){pos=N-1;setPlay(false)}}
    draw();
  }
  btn.onclick=function(){if(pos>=N-1)pos=0;setPlay(!playing);btn.blur()};
  rng.oninput=function(){setPlay(false);pos=rng.value/1000*(N-1)};
  el("rSpeed").onchange=function(){speed=+this.value;this.blur()};
  [rng,el("rSpeed")].forEach(function(n){n.addEventListener("keydown",function(e){e.stopPropagation()})});
  addEventListener("resize",size);size();requestAnimationFrame(loop);
})();
