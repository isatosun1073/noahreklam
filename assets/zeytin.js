/* Zeytin — Noah sohbet asistanı */
(()=>{"use strict";
if(window.__zt)return;window.__zt=1;
const API="/api/zeytin/chat",WA="905466328339";
const ss={get(k){try{return JSON.parse(sessionStorage.getItem(k))}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const bird=()=>`<svg class="zt-b" viewBox="0 0 120 84" aria-hidden="true"><g class="za">
<path d="M12 42 L30 40 L28 54 Z" fill="#c9c2b6"/><path d="M22 52 C26 36 56 30 74 38 C78 31 96 27 101 40 C103 48 96 53 88 53 C78 63 46 67 30 60 Z" fill="#ede8df"/><path d="M30 60 C46 67 78 63 88 53 C80 58 50 62 34 56 Z" fill="#d6d0c5"/>
<path d="M50 66 L48 72 M58 66 L58 72" stroke="#e23b2b" stroke-width="2.4" stroke-linecap="round"/>
<g class="zh"><circle cx="89" cy="39" r="11.5" fill="#ede8df"/><circle cx="85" cy="43" r="4" fill="#f2c2b8" opacity=".55"/><g class="ze"><circle cx="92" cy="35.5" r="2.3" fill="#06080a"/><circle cx="92.7" cy="34.8" r=".7" fill="#fff"/></g>
<path d="M99 36 L111 39.5 L99 41 Z" fill="#e23b2b"/><path class="zk" d="M99 41 L108.5 41 L99 44.5 Z" fill="#a8261a"/>
<g class="zo"><path d="M107 41 C114 47 117 54 115 62" stroke="#5d7a39" stroke-width="1.8" fill="none"/><ellipse cx="112" cy="50" rx="4.6" ry="1.9" transform="rotate(50 112 50)" fill="#7d9a52"/><ellipse cx="116" cy="57" rx="4.6" ry="1.9" transform="rotate(84 116 57)" fill="#7d9a52"/><ellipse cx="110.5" cy="58" rx="3.8" ry="1.6" transform="rotate(130 110.5 58)" fill="#93ad66"/></g></g>
<path class="zw" d="M44 44 C46 20 68 10 84 8 C80 20 70 36 58 48 Z" fill="#d6d0c5"/><path class="zw" d="M48 42 C54 26 66 18 76 16" stroke="#bfb7aa" stroke-width="1.2" fill="none"/></g></svg>`;
const HELLO="Selam! Ben Zeytin 🕊 Noah'ın güvercini. Reklam, paketler, sosyal medya ya da İsa hakkında ne merak ediyorsan sor, kısa ve net anlatayım.";
const CHIPS=["Paketler neler?","İşletmeme ne önerirsin?","İsa kimdir?","Reklam bütçesi ne kadar olmalı?"];

const L=document.createElement("button");L.className="zt-l";L.type="button";L.setAttribute("aria-label","Zeytin ile sohbet et");L.innerHTML=bird();
const tip=document.createElement("div");tip.className="zt-tip";tip.textContent="Aklında bir soru mu var? Bana yaz 🕊";
const P=document.createElement("section");P.className="zt-p";P.setAttribute("aria-label","Zeytin sohbet");P.setAttribute("role","dialog");
P.innerHTML=`<div class="zt-sky"><div class="zt-fly">${bird()}</div><div class="zt-hd"><div><b>Zeytin</b><span>Noah'ın asistanı · çevrimiçi</span></div><button class="zt-x" type="button" aria-label="Kapat">✕</button></div></div>
<div class="zt-ms" aria-live="polite"></div><div class="zt-ch"></div>
<form class="zt-f"><input id="zt-in" maxlength="600" placeholder="Zeytin'e sor…" autocomplete="off" aria-label="Mesajın"><button type="submit" aria-label="Gönder">↑</button></form>
<div class="zt-note">Zeytin bir yapay zekâ asistanı; önemli konularda İsa'ya danış.</div>`;
document.body.append(L,tip,P);if(!document.querySelector(".snd")){L.classList.add("low");tip.classList.add("low");}
const ld=document.getElementById("loader");if(ld&&!ld.hidden){L.hidden=true;const iv=setInterval(()=>{if(ld.hidden){L.hidden=false;clearInterval(iv);}},400);}
const ms=P.querySelector(".zt-ms"),ch=P.querySelector(".zt-ch"),form=P.querySelector("form"),inp=P.querySelector("input"),btn=form.querySelector("button"),fly=P.querySelector(".zt-fly");
const birds=()=>[...document.querySelectorAll(".zt-b")];
const state=s=>{birds().forEach(b=>{b.classList.remove("think","talk");if(s)b.classList.add(s);});fly.classList.toggle("busy",!!s);};
const hop=()=>birds().forEach(b=>{b.classList.remove("hop");void b.getBoundingClientRect();b.classList.add("hop");});

const esc=s=>s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const okUrl=u=>/^\/[^\s]*$/.test(u)||/^https:\/\/(www\.)?(noahreklam\.com|behance\.net|wa\.me)\//.test(u)||/^behance\.net\//.test(u);
function md(t,partial){
  let wa=null;t=t.replace(/\[\[WA:\s*([\s\S]*?)\]\]/g,(m,x)=>{wa=x.trim();return"";}).trim();
  if(partial)t=t.replace(/\[\[[\s\S]*$/,"");
  let h=esc(t).replace(/\*\*([^*\n]+)\*\*/g,"<b>$1</b>").replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g,(m,a,u)=>{u=u.replace(/&amp;/g,"&");if(!okUrl(u))return a;if(/^behance/.test(u))u="https://"+u;return`<a href="${esc(u)}"${/^https?:/.test(u)?' target="_blank" rel="noopener"':""}>${a}</a>`;})
    .replace(/^[-*] /gm,"• ");
  if(wa&&!partial)h+=`\n<a class="zt-wa" href="https://wa.me/${WA}?text=${encodeURIComponent(wa)}" target="_blank" rel="noopener">WhatsApp'tan İsa'ya gönder →</a>`;
  return h;
}
let H=ss.get("zt_h")||[],busy=false;
const save=()=>ss.set("zt_h",H.slice(-30));
function bubble(cls,html){const d=document.createElement("div");d.className="zt-m "+cls;d.innerHTML=html;ms.appendChild(d);ms.scrollTop=ms.scrollHeight;return d;}
function render(){ms.innerHTML="";bubble("z",esc(HELLO));H.forEach(m=>bubble(m.r,m.r==="u"?esc(m.t):md(m.t)));ch.innerHTML=H.length?"":CHIPS.map(c=>`<button type="button">${esc(c)}</button>`).join("");}
ch.addEventListener("click",e=>{const b=e.target.closest("button");if(b)send(b.textContent);});
const wait=ms=>new Promise(r=>setTimeout(r,ms));
function where(){
  if(location.pathname!=="/")return document.title.split("|")[0].trim().slice(0,70);
  const el=document.elementFromPoint(innerWidth/2,innerHeight/2),s=el&&el.closest("[data-k]");
  return "Ana sayfa · "+(s?s.dataset.k:"giriş");
}
async function send(q){
  q=(q||"").trim();if(!q||busy)return;busy=true;btn.disabled=true;ch.innerHTML="";
  H.push({r:"u",t:q});save();bubble("u",esc(q));inp.value="";
  state("think");const th=bubble("z",'<span class="zt-dots"><i></i><i></i><i></i></span>');
  let t;const t0=Date.now();
  try{const r=await fetch(API,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({h:H.slice(-14),p:where()})});t=(await r.json()).t;}catch(e){}
  if(!t)t="Telsizde parazit var 🌊 Bir daha dener misin? Acelen varsa İsa'ya yaz: 0546 632 83 39.";
  const left=700-(Date.now()-t0);if(left>0)await wait(left);
  th.remove();const m=bubble("z","");state("talk");
  const step=Math.max(2,Math.round(t.length/220));
  for(let i=0;i<t.length;i+=step){m.innerHTML=md(t.slice(0,i+step),true);ms.scrollTop=ms.scrollHeight;await wait(16);}
  m.innerHTML=md(t);ms.scrollTop=ms.scrollHeight;
  H.push({r:"z",t});save();state("");hop();busy=false;btn.disabled=false;
  typeof SND!=="undefined"&&SND.fx&&SND.fx("tick");
}
form.addEventListener("submit",e=>{e.preventDefault();send(inp.value);});
function open(){render();P.classList.add("on");document.body.classList.add("zt-open");tip.classList.remove("on");ss.set("zt_seen",1);
  typeof SND!=="undefined"&&SND.fx&&SND.fx("pop");hop();if(matchMedia("(min-width:601px)").matches)setTimeout(()=>inp.focus(),350);}
function close(){P.classList.remove("on");document.body.classList.remove("zt-open");L.focus();}
L.addEventListener("click",open);P.querySelector(".zt-x").addEventListener("click",close);
addEventListener("keydown",e=>{if(e.key==="Escape"&&P.classList.contains("on"))close();});
window.Zeytin={open,close,ask:q=>{open();send(q);}};
if(!ss.get("zt_seen"))setTimeout(()=>{if(P.classList.contains("on")||document.body.classList.contains("kp-talking"))return;tip.classList.add("on");setTimeout(()=>tip.classList.remove("on"),7000);},25000);
})();
