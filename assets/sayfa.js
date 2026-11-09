/* Noah — alt sayfa davranışları */
(()=>{
"use strict";
const WA="905466328339";
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];

// menü
const bg=$("#burger"),sh=$("#sheet");
if(bg&&sh)bg.addEventListener("click",()=>{const o=sh.classList.toggle("open");bg.setAttribute("aria-expanded",o);bg.textContent=o?"Kapat":"Menü";});
addEventListener("keydown",e=>{if(e.key==="Escape"&&sh&&sh.classList.contains("open"))bg.click();});

// okuma çubuğu
const pr=$("#progress"),art=$(".prose");
if(pr&&art){const f=()=>{const r=art.getBoundingClientRect();const t=Math.min(1,Math.max(0,-r.top/(r.height-innerHeight*.6)));pr.style.transform=`scaleX(${t})`;};addEventListener("scroll",f,{passive:true});f();}

// link kopyala
document.addEventListener("click",async e=>{const b=e.target.closest("[data-copy]");if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent="Kopyalandı ✓";}catch(err){prompt("Linki kopyala:",b.dataset.copy);}setTimeout(()=>b.textContent="Linki kopyala",2200);});

// blog araması (tüm yazılarda)
const q=$("#q"),grid=$("#grid"),none=$("#none");
if(q&&grid){let data=null,orig=grid.innerHTML;const pager=$(".pager");
  const norm=s=>(s||"").toLocaleLowerCase("tr").normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/ı/g,"i");
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const run=()=>{const v=norm(q.value.trim());
    if(!v){grid.innerHTML=orig;none.hidden=true;if(pager)pager.hidden=false;return;}
    const hit=data.filter(p=>v.split(/\s+/).every(w=>norm(p.t+" "+p.x+" "+p.c+" "+p.k).includes(w)));
    if(pager)pager.hidden=true;none.hidden=hit.length>0;
    grid.innerHTML=hit.map(p=>`<a class="card" href="${p.u}"><div class="cv"><img src="${p.u}kapak.svg" alt="" loading="lazy" width="1600" height="900"></div><div class="tx"><div class="meta mono"><b>${esc(p.c)}</b><span>${esc(p.d)} · ${p.m} dk</span></div><h2>${esc(p.t)}</h2><p>${esc(p.x)}</p><span class="rd mono">Oku <i></i></span></div></a>`).join("");};
  q.addEventListener("input",async()=>{if(!data){try{data=await (await fetch("/blog/posts.json")).json();}catch(e){data=[];}}run();});
  const pre=new URLSearchParams(location.search).get("q");if(pre){q.value=pre;q.dispatchEvent(new Event("input"));}
}

// reklam teklif formu → WhatsApp
const qf=$("#qform");
if(qf)qf.addEventListener("submit",e=>{e.preventDefault();
  const pl=$$("input[name=pl]:checked",qf).map(i=>i.value),bu=($("input[name=bu]:checked",qf)||{}).value||"Henüz bilmiyorum",go=($("input[name=go]:checked",qf)||{}).value||"—";
  const name=qf.name.value.trim(),brand=qf.brand.value.trim(),err=$(".err",qf);
  if(!name||!brand||!pl.length){err.hidden=false;err.textContent=!pl.length?"En az bir platform seç.":"Adını ve markanın adını yazman yeterli.";return;}
  err.hidden=true;
  const msg=`Merhaba Noah Reklam Ajansı 👋\nReklam yönetimi için teklif almak istiyorum.\n\nAd: ${name}\nMarka: ${brand}\nPlatformlar: ${pl.join(", ")}\nHedef: ${go}\nAylık reklam bütçesi: ${bu}\n\nNot:\n${qf.msg.value.trim()||"—"}`;
  location.href="https://wa.me/"+WA+"?text="+encodeURIComponent(msg);});

// platform hızlı bağlantıları: hedef liman kısa süre vurgulansın
$$('a[href^="#"]').forEach(a=>a.addEventListener("click",()=>{const t=document.getElementById(a.getAttribute("href").slice(1));if(t&&t.classList.contains("port")){t.style.transition="background .6s";t.style.background="rgba(226,59,43,.07)";setTimeout(()=>t.style.background="",1400);}}));
})();
