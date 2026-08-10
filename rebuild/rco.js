/* ============================================================================
   Shared behaviour for every rebuilt page. Vanilla, no libraries - nine
   competitor sites were measured across this project and every one of them
   runs zero animation libraries, so the motion here is CSS plus this file.
   ========================================================================= */
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header state + mobile menu */
  var hd=document.querySelector('.hd');
  if(hd){
    var onScroll=function(){hd.classList.toggle('scrolled',scrollY>12);};
    onScroll(); addEventListener('scroll',onScroll,{passive:true});
    var btn=hd.querySelector('.menu'), nav=hd.querySelector('nav');
    if(btn&&nav){btn.addEventListener('click',function(){
      var open=nav.classList.toggle('open');
      btn.setAttribute('aria-expanded',String(open));});}
  }

  /* Reveals. IntersectionObserver PLUS a plain rect check: IO callbacks
     provably never fire in the preview pane this site is verified in, and a
     page opened at a #fragment jumps without dispatching a scroll event.
     The rect check costs nothing and works everywhere. */
  var targets=[].slice.call(document.querySelectorAll('[data-rv]'));
  if(targets.length){
    if(reduce){targets.forEach(function(t){t.classList.add('inview');});}
    else{
      var check=function(){
        targets=targets.filter(function(t){
          var r=t.getBoundingClientRect();
          if(r.top<innerHeight*.85&&r.bottom>0){t.classList.add('inview');return false;}
          return true;});
        if(!targets.length) removeEventListener('scroll',check);
      };
      if('IntersectionObserver' in window){
        var io=new IntersectionObserver(function(es){es.forEach(function(e){
          if(e.isIntersecting){e.target.classList.add('inview');io.unobserve(e.target);}});},{threshold:.12});
        targets.forEach(function(t){io.observe(t);});
      }
      addEventListener('scroll',check,{passive:true});
      check(); setTimeout(check,300); setTimeout(check,1200);
    }
  }

  /* Gold particle constellation. The centrepiece device from the approved
     hero: fibonacci sphere, links precomputed in 3D so the wireframe is
     stable, cursor leans the axis. Any page can opt in with <canvas
     data-field>. */
  var cv=document.querySelector('canvas[data-field]');
  if(cv){
    var cx=cv.getContext('2d'), mouse={x:.5,y:.5};
    var size=function(){cv.width=cv.offsetWidth*devicePixelRatio;cv.height=cv.offsetHeight*devicePixelRatio;
      cx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);};
    size(); addEventListener('resize',size);
    addEventListener('pointermove',function(e){mouse.x=e.clientX/innerWidth;mouse.y=e.clientY/innerHeight;},{passive:true});
    var N=innerWidth<760?110:170, P=[], phi=Math.PI*(3-Math.sqrt(5));
    for(var i=0;i<N;i++){var y=1-(i/(N-1))*2,r=Math.sqrt(1-y*y),th=phi*i;
      P.push([Math.cos(th)*r,y,Math.sin(th)*r]);}
    var links=[];
    for(i=0;i<N;i++)for(var j=i+1;j<N;j++){
      var dx=P[i][0]-P[j][0],dy=P[i][1]-P[j][1],dz=P[i][2]-P[j][2];
      if(dx*dx+dy*dy+dz*dz<.075)links.push([i,j]);}
    var rotY=reduce?.7:0, tiltX=reduce?.18:0;
    var draw=function(){
      var w=cv.offsetWidth,h=cv.offsetHeight; cx.clearRect(0,0,w,h);
      if(!reduce){rotY+=.0022; tiltX+=(((mouse.y-.5)*.55)-tiltX)*.04;}
      var rotZ=reduce?0:(mouse.x-.5)*.25, big=innerWidth>960;
      var cxp=big?w*.68:w*.5, cyp=big?h*.46:h*.30, R=Math.min(w,h)*(big?.44:.5);
      var sy=Math.sin(rotY),cy2=Math.cos(rotY),sx=Math.sin(tiltX),cx2=Math.cos(tiltX),
          sz=Math.sin(rotZ),cz=Math.cos(rotZ), pr=[];
      for(var k=0;k<N;k++){var p=P[k];
        var x=p[0]*cy2+p[2]*sy, z1=-p[0]*sy+p[2]*cy2;
        var y1=p[1]*cx2-z1*sx,  z=p[1]*sx+z1*cx2;
        var x2=x*cz-y1*sz, y2=x*sz+y1*cz, s=1.6/(1.6+z);
        pr.push([cxp+x2*R*s, cyp+y2*R*s, z, s]);}
      for(k=0;k<links.length;k++){var a=pr[links[k][0]],b=pr[links[k][1]];
        var d=1-((a[2]+b[2])/2+1)/2;
        cx.strokeStyle='rgba(178,140,74,'+(.04+d*.16)+')';
        cx.beginPath();cx.moveTo(a[0],a[1]);cx.lineTo(b[0],b[1]);cx.stroke();}
      for(k=0;k<N;k++){var q=pr[k], dd=1-(q[2]+1)/2;
        cx.fillStyle='rgba(140,107,50,'+(.18+dd*.5)+')';
        cx.beginPath();cx.arc(q[0],q[1],(0.6+dd*1.7)*q[3],0,7);cx.fill();}
      if(!reduce) requestAnimationFrame(draw);
    };
    draw();
  }

  /* Coverage instrument. Any page can carry one; ids are shared. */
  var inc=document.getElementById('inc');
  if(inc){
    var need=document.getElementById('need'), out=document.getElementById('incOut'),
        full=document.getElementById('full'),
        chips=[].slice.call(document.querySelectorAll('.chip')),
        base=full?full.getAttribute('href'):'';
    var money=function(n){return '$'+Math.round(n).toLocaleString('en-US');};
    var paint=function(r){r.style.setProperty('--p',(r.value-r.min)/(r.max-r.min));};
    var run=function(anim){
      var extras=0;
      chips.forEach(function(c){if(c.getAttribute('aria-pressed')==='true')extras+=+c.dataset.add;});
      var v=(+inc.value)*10+extras;
      if(out) out.textContent=money(+inc.value);
      if(need&&need.textContent!==money(v)){
        need.textContent=money(v);
        if(anim&&!reduce){need.classList.remove('roll');void need.offsetWidth;need.classList.add('roll');}}
      if(full) full.href=base+'?income='+inc.value+
        (chips[0]&&chips[0].getAttribute('aria-pressed')==='true'?'&mortgage=250000':'&mortgage=0');
      paint(inc);
    };
    chips.forEach(function(c){c.addEventListener('click',function(){
      c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');run(true);});});
    inc.addEventListener('input',function(){run(true);});
    run(false);
  }

  /* ---- protection explorer (protection.html) ----
     Copy is lifted verbatim from types-of-life-insurance.html, which has already
     been through a compliance read. Nothing new is claimed. Term is the default
     panel and IUL sits below it in the list on purpose: leading a cold visitor
     with a permanent product is exactly what the original rule guarded against. */
  var PROD={
    term:{h:'Term life',
      l:'Coverage for a set number of years, usually 10, 20 or 30. If you die during the term, it pays. If you outlive it, it ends and pays nothing. That is the entire product, and it is why it costs the least per dollar of coverage by a wide margin.',
      s:'A mortgage, the years until children are grown, a business loan, an income that other people depend on.',
      c:'Nothing builds up. When the term ends you have paid for protection you did not use, which is how insurance is supposed to work.',
      w:'For most households under 50 with a mortgage and dependents, term does the job. We say that even though it pays us the least.'},
    di:{h:'Disability income',
      l:'Life insurance protects your family from losing you. Disability income protects them from losing your paycheck while you are still here, which is the likelier event during working years.',
      s:'The mortgage and the groceries during a long recovery, when the income stops but the bills do not.',
      c:'Premium rises with how quickly benefits start, how long they last, and how strictly the policy defines disability.',
      w:'The usual mistake is assuming a small group policy at work is enough. It typically replaces about 60% of base pay, often excludes bonus and commission, and ends the day you leave.'},
    perm:{h:'Whole and universal life',
      l:'Whole life is coverage for your whole life at a premium that does not change, with cash value growing at a rate the insurer sets. Universal life is permanent coverage with a flexible premium, which is both the feature and the risk.',
      s:'A need that does not expire: estate liquidity, a special-needs dependent, business continuity, final costs.',
      c:'Premium is several times term for the same benefit, and early years are heavily front-loaded with costs.',
      w:'When it is bought as an investment, or when a flexible policy is left unreviewed. Underfund universal life long enough and it can lapse.'},
    iul:{h:'Indexed universal life',
      l:'Universal life where cash value is credited based on a market index, subject to a cap on the upside and a floor against index losses. It is the most oversold product in this industry, so here is the plain version.',
      s:'A permanent need for someone who wants index-linked crediting with a floor, and who will actually review the policy.',
      c:'Caps, participation rates and spreads limit the credited amount, insurance charges rise with age, and the carrier can change some terms.',
      w:'When you have term needs, unused 401(k) or IRA space, or no emergency reserve. Those come first. Illustration projections are not a forecast and are not guaranteed.'},
    ltc:{h:'Long-term care, and hybrids',
      l:'Standalone long-term care insurance pays for care at home or in a facility. A hybrid, sometimes called linked-benefit, combines that with life insurance: if care is never needed, it pays a death benefit instead.',
      s:'Care costs that Medicare largely does not pay for, and the burden that otherwise lands on adult children.',
      c:'Standalone premiums can be raised by the carrier. Hybrids fix that by charging more up front.',
      w:'When protection and retirement income are not handled first, or when assets are small enough that Medicaid is the realistic path.'},
    fe:{h:'Final expense',
      l:'A small whole life policy, commonly $10,000 to $25,000, meant to cover a funeral, burial and the immediate bills that land on a family in the first few weeks. Underwriting is limited, which is the point.',
      s:'End-of-life costs for someone who cannot get, or does not need, a larger fully underwritten policy.',
      c:'A high price per dollar of coverage, and many policies have a graded benefit for the first two years.',
      w:'When you are healthy enough to qualify for a normal policy, or when savings already cover it.'}
  };
  var panel=document.getElementById('ppanel'), pbtns=[].slice.call(document.querySelectorAll('.pbtn'));
  function paintP(key,animate){
    var d=PROD[key]; if(!d||!panel) return;
    panel.innerHTML='<div class="'+(animate&&!reduce?'pfade':'')+'">'+
      '<h3>'+d.h+'</h3><p class="lead2">'+d.l+'</p><div class="pboxes">'+
      '<div class="pbox"><b>What it solves</b><span>'+d.s+'</span></div>'+
      '<div class="pbox"><b>What it costs you</b><span>'+d.c+'</span></div>'+
      '<div class="pbox"><b>Worth knowing</b><span>'+d.w+'</span></div></div></div>';
    pbtns.forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.p===key));});
  }
  pbtns.forEach(function(b){b.addEventListener('click',function(){paintP(b.dataset.p,true);});});
  if(panel) paintP('term',false);


  /* ---- full calculator (calculator.html) ----
     Ported wholesale, including the parse fix that was a LIVE defect: the money
     fields are type=text so they can carry thousands separators, and a bare
     parseFloat on "$75,000" returns NaN, which silently counted that entire
     field as ZERO. Strip to digits before parsing, always. */
  var calcIds=["income","years","mortgage","debts","kids","percollege","final","existing"];
  if(document.getElementById("gapOut")){
    var f=function(n){return "$"+Math.round(n).toLocaleString("en-US");};
    var num=function(v){var x=parseFloat(String(v).replace(/[^0-9.]/g,""));return isNaN(x)||x<0?0:x;};
    var get=function(id){var el=document.getElementById(id);return el?num(el.value):0;};
    var moneyFields=["income","mortgage","debts","percollege","final","existing"];
    var fmt=function(el){var v=num(el.value);
      if(moneyFields.indexOf(el.id)>=0) el.value=Math.round(v).toLocaleString("en-US");};
    var card=document.getElementById("resultCard");
    function calc(){
      var need=get("income")*get("years")+get("mortgage")+get("debts")+get("kids")*get("percollege")+get("final");
      var have=get("existing"), gap=need-have;
      document.getElementById("needOut").textContent=f(need);
      document.getElementById("haveOut").textContent=f(have);
      if(gap>0){card.classList.remove("covered");
        document.getElementById("gapOut").textContent=f(gap);
        document.getElementById("gapNote").textContent="This is roughly what you are short by today.";
      }else{card.classList.add("covered");
        document.getElementById("gapOut").textContent="Covered";
        document.getElementById("gapNote").textContent="Your current coverage meets the estimate. Worth confirming it is not tied to your job.";}
    }
    var paintR=function(r){r.style.setProperty("--p",(+r.value-+r.min)/(+r.max-+r.min));};
    [].slice.call(document.querySelectorAll(".sf-range")).forEach(function(r){
      var t=document.getElementById(r.getAttribute("data-for")); if(!t) return;
      r.addEventListener("input",function(){t.value=r.value;fmt(t);calc();paintR(r);});
      t.addEventListener("input",function(){var v=num(t.value);
        if(!isNaN(v)) r.value=v;   /* thumb parks at the end if the typed value is out of range */
        calc();paintR(r);});
      t.addEventListener("blur",function(){fmt(t);});
      paintR(r);
    });
    /* values handed over from a homepage instrument */
    (function(){var q=new URLSearchParams(location.search);
      ["income","mortgage"].forEach(function(id){
        var v=parseFloat(q.get(id)); if(isNaN(v)||v<0) return;
        var el=document.getElementById(id); if(!el) return;
        el.value=v; fmt(el);
        var r=document.querySelector('.sf-range[data-for="'+id+'"]');
        if(r){r.value=v;paintR(r);}});})();
    calc();
  }

  /* Retirement income check. The AUM-side twin of the coverage instrument:
     wealth was the only pillar with no self-service tool, which structurally
     pushed every self-guided visitor toward insurance.

     The growth rate is a USER input on purpose. A calculator that quietly
     assumes 8% is making a performance claim on the firm's behalf; making the
     visitor set it turns the same maths into their assumption, and dragging it
     teaches the real lesson - how much the answer moves on a guess. */
  var wAge=document.getElementById('wAge');
  if(wAge){
    var wPot=document.getElementById('wPot'),wAdd=document.getElementById('wAdd'),
        wRet=document.getElementById('wRet'),wWant=document.getElementById('wWant'),
        wNum=document.getElementById('wNum'),wLabel=document.getElementById('wLabel'),
        wFill=document.getElementById('wFill'),wCta=document.getElementById('wCta'),
        chips=[].slice.call(document.querySelectorAll('.rchip')),
        retAge=65;
    var money=function(n){return '$'+Math.round(n).toLocaleString('en-US');};

    function wCalc(){
      var age=+wAge.value, pot=+wPot.value, add=+wAdd.value,
          r=(+wRet.value)/100, want=+wWant.value,
          yrs=Math.max(0,retAge-age);
      document.getElementById('wAgeOut').textContent=age;
      document.getElementById('wPotOut').textContent=money(pot);
      document.getElementById('wAddOut').textContent=money(add);
      document.getElementById('wRetOut').textContent=(+wRet.value).toFixed(1)+'%';
      document.getElementById('wWantOut').textContent=money(want)+'/mo';

      /* monthly compounding, contributions at period end */
      var m=r/12, n=yrs*12,
          fv=m===0 ? pot+add*n
                   : pot*Math.pow(1+m,n) + add*(Math.pow(1+m,n)-1)/m;
      var supports=fv*0.04/12;                       /* 4% rule, monthly */
      var pct=want>0 ? Math.max(0,Math.min(1,supports/want)) : 1;

      if(wNum.textContent!==money(supports)){
        wNum.textContent=money(supports);
        wNum.classList.remove('roll');void wNum.offsetWidth;wNum.classList.add('roll');
      }
      wFill.style.width=(pct*100).toFixed(1)+'%';
      wFill.style.background=pct>=1?'var(--gold)':(pct>=.7?'#c8a15a':'#b4763f');

      if(yrs===0){
        wLabel.textContent='Retiring now, this supports';
      } else if(supports>=want){
        wLabel.textContent='Covers your target, with room';
      } else {
        wLabel.textContent='Short of your target by '+money(want-supports)+' a month';
      }
      wCta.textContent = supports>=want ? 'Keep it that way →' : 'Close the gap →';
    }

    chips.forEach(function(c){
      c.addEventListener('click',function(){
        chips.forEach(function(x){x.setAttribute('aria-pressed','false');});
        c.setAttribute('aria-pressed','true');
        retAge=+c.getAttribute('data-age');
        if(+wAge.value>=retAge) wAge.value=retAge-1;
        wCalc();
      });
    });
    [wAge,wPot,wAdd,wRet,wWant].forEach(function(el){
      el.addEventListener('input',wCalc);
    });
    wCalc();
  }

  /* "See all carriers" reveals the full roster in place. No new page, and the
     label stays honest because the names really are all there. */
  var ctog=document.querySelector('[data-carriers]'),clist=document.getElementById('carrierlist');
  if(ctog&&clist){
    ctog.addEventListener('click',function(){
      var open=clist.classList.toggle('open');
      ctog.setAttribute('aria-expanded',open?'true':'false');
      ctog.textContent=open?'Hide carrier list':'See all carriers';
    });
  }

  /* Magnetic primary CTA, fine pointers only. */
  if(!reduce && matchMedia('(pointer:fine)').matches){
    var mag=document.querySelector('[data-magnetic]');
    if(mag){
      mag.addEventListener('pointermove',function(e){var r=mag.getBoundingClientRect();
        mag.style.transform='translate('+((e.clientX-r.left-r.width/2)*.16)+'px,'+((e.clientY-r.top-r.height/2)*.28)+'px)';});
      mag.addEventListener('pointerleave',function(){mag.style.transform='';});
    }
  }
})();
