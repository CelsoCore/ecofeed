"""Mini juego de pausa: un brote que salta residuos electrónicos. Dibujo y código propios (no es copia de ningún juego)."""

HTML = """
<div style="font-family:system-ui,sans-serif;color:#e8fff1">
<canvas id="c" width="720" height="240" style="width:100%;max-width:720px;border-radius:16px;background:linear-gradient(#0b3d2e,#145c43);touch-action:manipulation;display:block;margin:auto"></canvas>
<p id="m" style="text-align:center;margin:8px 0 0;font-size:15px">Toca la pantalla o pulsa la barra espaciadora para saltar los residuos</p>
</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),m=document.getElementById('m');
const G=190;let y,vy,obs,pts,vel,vivo,t,rec=0,nubes=[{x:120,y:40},{x:420,y:70},{x:640,y:30}];
try{rec=+localStorage.getItem('ecofeed_rec')||0}catch(e){}
function reinicia(){y=G;vy=0;obs=[];pts=0;vel=5;vivo=true;t=0}
function salta(){if(!vivo){reinicia();return}if(y>=G){vy=-13}}
addEventListener('keydown',e=>{if(e.code==='Space'||e.code==='ArrowUp'){e.preventDefault();salta()}});
c.addEventListener('pointerdown',salta);
function brote(px,py){x.fillStyle='#8b5a2b';x.fillRect(px,py-14,26,14);x.fillStyle='#22c55e';x.fillRect(px+11,py-30,4,16);
 x.beginPath();x.ellipse(px+4,py-30,9,5,-0.5,0,7);x.ellipse(px+22,py-34,9,5,0.5,0,7);x.fill()}
function residuo(o){if(o.k){x.fillStyle='#e5e7eb';x.fillRect(o.x,G-o.h,o.w,o.h);x.fillStyle='#facc15';x.fillRect(o.x+o.w/2-3,G-o.h-6,6,6);x.fillStyle='#ef4444';x.fillRect(o.x,G-o.h+8,o.w,5)}
 else{x.fillStyle='#374151';x.fillRect(o.x,G-o.h,o.w,o.h);x.strokeStyle='#9ca3af';x.lineWidth=3;x.beginPath();x.moveTo(o.x+o.w/2,G-o.h);x.quadraticCurveTo(o.x+o.w/2+20,G-o.h-26,o.x+o.w/2+34,G-o.h-8);x.stroke()}}
function paso(){t++;
 if(vivo){vy+=0.7;y=Math.min(G,y+vy);if(y>=G){y=G;vy=0}
  if(t%Math.max(48,95-Math.floor(vel*4))===0&&Math.random()<.9){const k=Math.random()<.5;obs.push({x:740,w:k?22:30,h:k?40:28,k})}
  obs.forEach(o=>o.x-=vel);obs=obs.filter(o=>o.x>-50);pts+=0.12;vel=5+pts/60;
  for(const o of obs){if(o.x<54&&o.x+o.w>30&&y>G-o.h-2){vivo=false;if(pts>rec){rec=Math.floor(pts);try{localStorage.setItem('ecofeed_rec',rec)}catch(e){}}}}}
 x.clearRect(0,0,720,240);
 x.fillStyle='rgba(255,255,255,.12)';nubes.forEach(n=>{n.x-=0.4;if(n.x<-60)n.x=760;x.fillRect(n.x,n.y,50,10);x.fillRect(n.x+10,n.y-8,30,10)});
 x.fillStyle='#052e22';x.fillRect(0,G,720,50);x.fillStyle='#22c55e';for(let i=0;i<24;i++){x.fillRect(((i*34-t*vel)%816+816)%816-40,G+14,16,3)}
 obs.forEach(residuo);brote(32,y);
 x.fillStyle='#fff';x.font='bold 16px system-ui';x.fillText('Puntos '+Math.floor(pts)+'   Récord '+rec,14,24);
 if(!vivo){x.font='bold 22px system-ui';x.fillText('Choque con un residuo. Toca para reintentar',130,110)}
 requestAnimationFrame(paso)}
reinicia();paso();
</script>
"""
