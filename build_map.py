# -*- coding: utf-8 -*-
"""Build index.html (fetch-based) and standalone.html (self-contained) from one source."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(HERE,"data"); LIB=os.path.join(HERE,"lib")

DATASETS={
 "DIST":"bma_districts.geojson","ZONE":"bma_zone_groups.geojson","POLICE":"police_stations.geojson",
 "JUN":"junctions.geojson","SUR":"survey_junctions.geojson","ROAD":"road_corridors.geojson",
 "INTER":"interchanges.geojson","RAIL":"rail_stations.geojson","DRS":"district_road_stats.json"}

STYLE = r"""
 :root{--ink:#1f2933;--mut:#6b7280;--line:#e5e7eb;--bg:#f8fafc;}
 *{box-sizing:border-box;} html,body{height:100%;margin:0;font-family:"Segoe UI",Tahoma,"Sarabun",sans-serif;color:var(--ink);}
 #app{display:flex;height:100vh;}
 #side{width:326px;flex:0 0 326px;background:#fff;border-right:1px solid var(--line);display:flex;flex-direction:column;overflow-y:auto;}
 header{padding:14px 16px;background:linear-gradient(135deg,#0d3b66,#1b6ca8);color:#fff;}
 header h1{font-size:15px;margin:0 0 3px;line-height:1.3;} header p{font-size:11px;margin:0;opacity:.85;}
 .sec{padding:12px 16px;border-bottom:1px solid var(--line);}
 .sec h2{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 9px;}
 .lyr{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:13px;cursor:pointer;}
 .sw{width:16px;height:16px;border-radius:3px;flex:0 0 16px;border:1px solid rgba(0,0,0,.25);}
 .dot{width:13px;height:13px;border-radius:50%;flex:0 0 13px;border:1px solid #fff;box-shadow:0 0 0 1px rgba(0,0,0,.25);}
 .dotc{width:13px;height:13px;border-radius:50%;flex:0 0 13px;background:conic-gradient(#e63946 0 25%,#2a9d8f 0 50%,#3a86ff 0 75%,#8338ec 0);border:1px solid #fff;}
 .ring{width:13px;height:13px;border-radius:50%;flex:0 0 13px;border:2.5px solid #0f766e;background:transparent;}
 .line{width:16px;height:0;flex:0 0 16px;border-top:3px solid #334155;}
 .diamond{width:11px;height:11px;flex:0 0 11px;background:#0091ea;border:1.5px solid #fff;transform:rotate(45deg);box-shadow:0 0 0 1px #0091ea;margin-left:2px;}
 .tri{width:0;height:0;flex:0 0 14px;border-left:7px solid transparent;border-right:7px solid transparent;border-top:12px solid #1565C0;}
 select{font-family:inherit;font-size:13px;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:#fff;width:100%;}
 .legend div{display:flex;align-items:center;gap:8px;font-size:12px;margin:3px 0;}
 .legend i{width:22px;height:12px;border-radius:2px;display:inline-block;}
 #map{flex:1;position:relative;} #loading{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#f8fafc;z-index:9999;font-size:14px;color:#0d3b66;}
 .note{font-size:11px;color:var(--mut);line-height:1.5;}
 .badge{display:inline-block;background:#e0f2fe;color:#0369a1;border-radius:4px;padding:1px 6px;font-size:10px;}
 .leaflet-popup-content{font-family:"Segoe UI",Tahoma,sans-serif;font-size:13px;line-height:1.5;margin:10px 12px;max-width:260px;}
 .pt{font-weight:700;font-size:14px;margin-bottom:4px;color:#0d3b66;} .pk{color:var(--mut);}
 table.pp{border-collapse:collapse;margin-top:4px;} table.pp td{padding:1px 4px;vertical-align:top;}
 .foot{padding:12px 16px;font-size:11px;color:var(--mut);margin-top:auto;}
 .stat{font-size:12px;margin:2px 0;} .stat b{color:#0d3b66;}
 #companyBox{display:none;}
"""

BODY = r"""
<div id="app"><div id="side">
 <header><h1>ทางแยกสัญญาณไฟ · ถนน · ระบบราง · ขอบเขต กทม.</h1>
 <p>สัญญาณไฟ 580 · ต่างระดับ 31 · สถานีรถไฟฟ้า 190 · ถนน 51 · เขต 50</p></header>
 <div class="sec"><h2>ชั้นข้อมูล (Layers)</h2>
   <label class="lyr"><input type="checkbox" id="ck_zone"><span class="sw" style="background:#8ecae6;opacity:.6"></span> กลุ่มเขต 6 กลุ่ม</label>
   <label class="lyr"><input type="checkbox" id="ck_dist" checked><span class="sw" style="background:#fdae6b"></span> สำนักงานเขต 50 เขต</label>
   <label class="lyr"><input type="checkbox" id="ck_road"><span class="line"></span> ถนนสายหลัก 51 สาย</label>
   <label class="lyr"><input type="checkbox" id="ck_pol"><span class="sw" style="background:#5a4fcf;opacity:.55"></span> สถานีตำรวจ 89 แห่ง</label>
   <label class="lyr"><input type="checkbox" id="ck_jun" checked><span class="dot" style="background:#e10600"></span> ทางแยกสัญญาณไฟ 580 จุด (แดง)</label>
   <label class="lyr"><input type="checkbox" id="ck_company"><span class="dotc"></span> จำแนกตามบริษัท/เครื่องควบคุม</label>
   <label class="lyr"><input type="checkbox" id="ck_inter" checked><span class="diamond"></span> ทางแยกต่างระดับ 31 จุด (ฟ้า)</label>
   <label class="lyr"><input type="checkbox" id="ck_rail" checked><span class="tri"></span> สถานีรถไฟฟ้า 190 (▽ ทุกสาย)</label>
   <label class="lyr"><input type="checkbox" id="ck_sur"><span class="ring"></span> จุดสำรวจเวลาเดินทาง 314</label>
 </div>
 <div class="sec" id="railBox"><h2>สีสถานี = สายรถไฟฟ้า</h2><div class="legend" id="railleg"></div></div>
 <div class="sec" id="companyBox"><h2>สีจุด = บริษัท / เครื่องควบคุม</h2><div class="legend" id="companyleg"></div></div>
 <div class="sec"><h2>ระบายสีเขตตามข้อมูล</h2>
   <select id="chmode">
     <option value="none">— ไม่ระบายสี —</option>
     <option value="pop">ประชากรรวม (คน)</option>
     <option value="den">ความหนาแน่น (คน/ตร.กม.)</option>
     <option value="jcount">จำนวนทางแยกสัญญาณไฟในเขต</option>
     <option value="road_area">พื้นที่ถนนรายเขต (ตร.ม.)</option>
     <option value="road_len_km">ความยาวถนนรายเขต (กม.)</option>
   </select>
   <div class="legend" id="legend" style="margin-top:10px;"></div>
 </div>
 <div class="sec"><h2>ภาพรวม</h2>
   <div class="stat">ทางแยกสัญญาณไฟ: <b id="s_jun"></b> จุด</div>
   <div class="stat">ต่างระดับ: <b id="s_inter"></b> · สถานีรถไฟฟ้า: <b id="s_rail"></b></div>
   <div class="stat">พื้นที่ถนนรวม: <b>28.49</b> ตร.กม.</div>
 </div>
 <div class="sec"><h2>แผนที่ฐาน (Basemap)</h2>
   <select id="base">
     <option value="osm">OpenStreetMap มาตรฐาน</option>
     <option value="carto">Carto Positron (สว่าง)</option>
     <option value="cartodark">Carto Dark</option>
     <option value="esri">ภาพถ่ายดาวเทียม (Esri)</option>
   </select>
 </div>
 <div class="foot">
   <p class="note"><span class="badge">ข้อมูล</span> ต่างระดับจากไฟล์ทางแยก 2567 · สถานีเชื่อมต่อรถไฟฟ้าเป็นชุดคัดเลือก (พิกัดโดยประมาณ ควรตรวจกับแหล่งทางการ) · เส้นถนนเป็นแนวโดยประมาณ</p>
   <p style="margin-top:8px;">© Prapawadee_W. · Traffic &amp; Transportation Dept., BMA<br>Basemap © OpenStreetMap contributors</p>
 </div>
</div><div id="map"><div id="loading">กำลังโหลดข้อมูลแผนที่…</div></div></div>
"""

APP = r"""
const RED='#e10600';
const CTRL={'Forth':'#e63946','GeTs':'#2a9d8f','Adaptive':'#f4a261','PEEK':'#8338ec','SCAE':'#3a86ff','Siemens':'#ff006e','TES':'#606c38'};
const ctrlColor=c=>CTRL[c]||'#8d99ae';
const fmt=n=>(n==null?'-':Number(n).toLocaleString('en-US'));
const RAMP=['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#b10026'];
const GREENS=['#f7fcf5','#e5f5e0','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32'];

function init(D){
 const POLICE=D.POLICE,DIST=D.DIST,ZONE=D.ZONE,JUN=D.JUN,SUR=D.SUR,ROAD=D.ROAD,INTER=D.INTER,RAIL=D.RAIL,DRS=D.DRS;
 const lo=document.getElementById('loading'); if(lo) lo.remove();
 const map=L.map('map',{preferCanvas:true}).setView([13.75,100.52],11);
 const bases={
  osm:L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}),
  carto:L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{maxZoom:20,attribution:'© OpenStreetMap © CARTO'}),
  cartodark:L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{maxZoom:20,attribution:'© OpenStreetMap © CARTO'}),
  esri:L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'© Esri'})};
 let curBase=bases.osm.addTo(map);
 document.getElementById('base').onchange=e=>{map.removeLayer(curBase);curBase=bases[e.target.value].addTo(map);curBase.bringToBack();relayer();};

 function quantile(v){const s=v.filter(x=>x!=null).sort((a,b)=>a-b);const q=[];for(let i=1;i<8;i++)q.push(s[Math.floor(i*s.length/8)]);return q;}
 function colFor(v,br,ramp){if(v==null)return '#ddd';for(let i=0;i<br.length;i++)if(v<=br[i])return ramp[i];return ramp[7];}
 const jcount={};JUN.features.forEach(f=>{const d=f.properties.district;if(d)jcount[d]=(jcount[d]||0)+1;});
 function dval(p,m){const s=DRS[p.dname_th]||{};
  if(m==='pop')return p.pop_total;if(m==='den')return(p.pop_total&&p.area_km2)?p.pop_total/p.area_km2:null;
  if(m==='jcount')return jcount[p.dname_th]||0;
  if(m==='road_area')return s.road_area||0;if(m==='road_len_km')return s.road_len_km||0;return null;}
 function baseDist(){return{color:'#c2560f',weight:1,fillColor:'#fdae6b',fillOpacity:.15};}
 function restyle(){const m=document.getElementById('chmode').value;
  if(m==='none'){distLayer.setStyle(baseDist);document.getElementById('legend').innerHTML='';return;}
  const roadMode=(m==='road_area'||m==='road_len_km');const ramp=roadMode?GREENS:RAMP;const border=roadMode?'#1b5e20':'#c2560f';
  const vals=DIST.features.map(f=>dval(f.properties,m));const br=quantile(vals);
  distLayer.setStyle(f=>({color:border,weight:1,fillColor:colFor(dval(f.properties,m),br,ramp),fillOpacity:.75}));
  const U={pop:'คน',den:'คน/ตร.กม.',jcount:'แยก',road_area:'ตร.ม.',road_len_km:'กม.'};
  const T={pop:'ประชากร',den:'ความหนาแน่น',jcount:'ทางแยกในเขต',road_area:'พื้นที่ถนน',road_len_km:'ความยาวถนน'};
  let h=`<div style="font-weight:600;margin-bottom:4px">${T[m]} (${U[m]})</div>`;let pv=0;
  for(let i=0;i<ramp.length;i++){const hi=i<br.length?br[i]:null;h+=`<div><i style="background:${ramp[i]}"></i>${hi==null?'> '+Math.round(pv).toLocaleString():Math.round(pv).toLocaleString()+' – '+Math.round(hi).toLocaleString()}</div>`;pv=hi;}
  document.getElementById('legend').innerHTML=h;}
 document.getElementById('chmode').onchange=restyle;

 const distLayer=L.geoJSON(DIST,{style:baseDist,onEachFeature:(f,l)=>{const p=f.properties;const s=DRS[p.dname_th]||{};
  const den=(p.pop_total&&p.area_km2)?Math.round(p.pop_total/p.area_km2).toLocaleString():'-';
  l.bindPopup(`<div class="pt">${p.dname||('เขต'+p.dname_th)}</div><div class="pk">${p.dname_en||''} · รหัส ${p.dcode||'-'}</div>
   <table class="pp"><tr><td class="pk">ประชากร</td><td><b>${fmt(p.pop_total)}</b> คน</td></tr>
   <tr><td class="pk">พื้นที่เขต</td><td>${p.area_km2} ตร.กม. (${den} คน/ตร.กม.)</td></tr>
   <tr><td class="pk">ทางแยกสัญญาณไฟ</td><td>${jcount[p.dname_th]||0} แยก</td></tr>
   <tr><td class="pk">ถนน</td><td>${s.road_count||0} สาย · ${s.road_len_km||0} กม.</td></tr>
   <tr><td class="pk">พื้นที่ถนน</td><td>${fmt(s.road_area)} ตร.ม.</td></tr></table>`);
  l.on('mouseover',()=>l.setStyle({weight:2.5}));l.on('mouseout',()=>{const m=document.getElementById('chmode').value;if(m==='none')distLayer.resetStyle(l);else restyle();});}});

 const zoneLayer=L.geoJSON(ZONE,{style:{color:'#1b6ca8',weight:2.5,dashArray:'6 4',fillColor:'#8ecae6',fillOpacity:.12},
  onEachFeature:(f,l)=>{const p=f.properties;const flag=p.data_flag==='population_src_anomaly'?`<div class="pk" style="color:#b91c1c">⚠ ค่าต้นฉบับผิดปกติ</div>`:'';
  l.bindPopup(`<div class="pt">กลุ่ม${p.z_name}</div><div class="pk">${p.z_name_en} · ${p.n_districts} เขต</div>${flag}<table class="pp"><tr><td class="pk">ประชากร</td><td><b>${fmt(p.pop_total_calc)}</b> คน</td></tr></table>`);}});

 const roadLayer=L.geoJSON(ROAD,{style:{color:'#334155',weight:3,opacity:.85},
  onEachFeature:(f,l)=>{l.bindPopup(`<div class="pt">${f.properties.road}</div><div class="pk">ถนนสายหลัก · ${f.properties.n_points} จุดพิกัด</div>`);
   l.on('mouseover',()=>l.setStyle({color:'#f59e0b',weight:5}));l.on('mouseout',()=>l.setStyle({color:'#334155',weight:3}));}});

 const polLayer=L.geoJSON(POLICE,{style:{color:'#5a4fcf',weight:1.2,fillColor:'#7c6ff0',fillOpacity:.25},
  onEachFeature:(f,l)=>{const p=f.properties;l.bindPopup(`<div class="pt">${p.name_th}</div><div class="pk">${p.name_en||''} · ${p.type}</div>`);}});

 function junPopup(p){return `<div class="pt">แยก${p.name||''}</div><div class="pk">รหัส กทม. ${p.code||'-'}</div>
   <table class="pp"><tr><td class="pk">ถนน</td><td>${p.road_main||'-'} × ${p.road_sub||'-'}</td></tr>
   <tr><td class="pk">บริษัท/เครื่องควบคุม</td><td><b>${p.controller||'-'}</b></td></tr>
   <tr><td class="pk">สน.</td><td>${p.police||'-'}</td></tr><tr><td class="pk">เขต</td><td>${p.district||'-'}</td></tr></table>`;}
 const junLayer=L.geoJSON(JUN,{pointToLayer:(f,ll)=>L.circleMarker(ll,{radius:5,weight:1,color:'#fff',fillColor:RED,fillOpacity:.95}),
  onEachFeature:(f,l)=>{l.bindPopup(junPopup(f.properties));l.on('mouseover',()=>l.setStyle({radius:8}));l.on('mouseout',()=>l.setStyle({radius:5}));}});
 const companyLayer=L.geoJSON(JUN,{pointToLayer:(f,ll)=>L.circleMarker(ll,{radius:5,weight:1,color:'#fff',fillColor:ctrlColor(f.properties.controller),fillOpacity:.95}),
  onEachFeature:(f,l)=>{l.bindPopup(junPopup(f.properties));l.on('mouseover',()=>l.setStyle({radius:8}));l.on('mouseout',()=>l.setStyle({radius:5}));}});
 const surLayer=L.geoJSON(SUR,{pointToLayer:(f,ll)=>L.circleMarker(ll,{radius:6,weight:2.5,color:'#0f766e',fillColor:'#14b8a6',fillOpacity:.15}),
  onEachFeature:(f,l)=>{const p=f.properties;l.bindPopup(`<div class="pt">แยก${p.name||''}</div><div class="pk">รหัสสัญญาณไฟ ${p.signal_code||'-'} · สำรวจ ${p.n_corridors} เส้นทาง</div><table class="pp"><tr><td class="pk">เส้นทาง</td><td>${p.corridors||'-'}</td></tr></table>`);}});

 // NEW: interchanges (blue diamond)
 const interIcon=L.divIcon({className:'',iconSize:[16,16],iconAnchor:[8,8],
   html:'<div style="width:12px;height:12px;background:#0091ea;border:1.5px solid #fff;transform:rotate(45deg);box-shadow:0 0 0 1px #0091ea"></div>'});
 const interLayer=L.geoJSON(INTER,{pointToLayer:(f,ll)=>L.marker(ll,{icon:interIcon}),
  onEachFeature:(f,l)=>{const p=f.properties;l.bindPopup(`<div class="pt">${p.name||''}</div><div class="pk">ทางแยกต่างระดับ${p.name_en?' · '+p.name_en:''}</div>
   <table class="pp"><tr><td class="pk">ถนน</td><td>${p.road||'-'}</td></tr><tr><td class="pk">เขต</td><td>${p.district||'-'}</td></tr>${p.note?`<tr><td class="pk">หมายเหตุ</td><td>${p.note}</td></tr>`:''}</table>`);}});

 // NEW: rail stations (all lines) — inverted equilateral triangle (▽), colored by line; interchange = dark stroke
 function railTri(color,big){const w=big?18:15,h=big?16:13,sw=big?2.2:1.4,st=big?'#111':'#fff';
   return L.divIcon({className:'rail-tri',iconSize:[w,h],iconAnchor:[w/2,h/2],
     html:`<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="display:block;overflow:visible"><polygon points="${w/2},${h-1} 1,1.5 ${w-1},1.5" fill="${color}" stroke="${st}" stroke-width="${sw}" stroke-linejoin="round"/></svg>`});}
 const railLayer=L.geoJSON(RAIL,{pointToLayer:(f,ll)=>L.marker(ll,{icon:railTri(f.properties.color||'#607D8B',f.properties.interchange),keyboard:false,riseOnHover:true}),
  onEachFeature:(f,l)=>{const p=f.properties;
   l.bindPopup(`<div class="pt">สถานี${p.name_th||''}</div><div class="pk">${p.name_en||''} · ${p.code||''}</div>
   <table class="pp"><tr><td class="pk">สาย</td><td><b style="color:${p.color}">${p.line||'-'}</b></td></tr>
   ${p.network?`<tr><td class="pk">ผู้ให้บริการ</td><td>${p.network}</td></tr>`:''}
   ${p.interchange?`<tr><td class="pk">สถานีเปลี่ยนสาย</td><td>${p.xchg_lines||'ใช่'}</td></tr>`:''}</table>`);}});
 // rail line legend (triangle swatches)
 (function(){const ord=[],seen={};RAIL.features.forEach(f=>{const p=f.properties;if(!seen[p.line]){seen[p.line]={c:p.color,n:0};ord.push(p.line);}seen[p.line].n++;});
  const tri=c=>`display:inline-block;width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-top:11px solid ${c};background:transparent;border-radius:0`;
  let h='';ord.forEach(k=>{h+=`<div><i style="${tri(seen[k].c)}"></i>${k} (${seen[k].n})</div>`;});
  h+=`<div style="margin-top:5px"><i style="${tri('#9aa')}"></i>▽ สามเหลี่ยมกลับหัว = สถานีรถไฟฟ้า (ขอบเข้ม = สถานีเปลี่ยนสาย)</div>`;
  document.getElementById('railleg').innerHTML=h;})();

 (function(){const cnt={};JUN.features.forEach(f=>{const c=f.properties.controller||'ไม่ระบุ';cnt[c]=(cnt[c]||0)+1;});
  let h='';Object.entries(cnt).sort((a,b)=>b[1]-a[1]).forEach(([c,n])=>{h+=`<div><i style="background:${ctrlColor(c==='ไม่ระบุ'?null:c)};border-radius:50%"></i>${c} (${n})</div>`;});
  document.getElementById('companyleg').innerHTML=h;})();

 function relayer(){if(document.getElementById('ck_zone').checked)zoneLayer.bringToBack();curBase.bringToBack();
  if(document.getElementById('ck_road').checked)roadLayer.bringToFront();
  if(document.getElementById('ck_jun').checked)junLayer.bringToFront();
  if(document.getElementById('ck_company').checked)companyLayer.bringToFront();
  if(document.getElementById('ck_sur').checked)surLayer.bringToFront();}
 function bind(ck,layer,def,cb){const el=document.getElementById(ck);if(def)layer.addTo(map);
  el.onchange=()=>{el.checked?layer.addTo(map):map.removeLayer(layer);relayer();if(cb)cb(el.checked);};}
 bind('ck_zone',zoneLayer,false);bind('ck_dist',distLayer,true);bind('ck_road',roadLayer,false);
 bind('ck_pol',polLayer,false);bind('ck_jun',junLayer,true);
 bind('ck_company',companyLayer,false,on=>{document.getElementById('companyBox').style.display=on?'block':'none';});
 bind('ck_inter',interLayer,true);
 bind('ck_rail',railLayer,true,on=>{document.getElementById('railBox').style.display=on?'block':'none';});
 bind('ck_sur',surLayer,false);
 document.getElementById('railBox').style.display='block';
 junLayer.bringToFront();
 map.fitBounds(distLayer.getBounds(),{padding:[10,10]});
 document.getElementById('s_jun').textContent=JUN.features.length.toLocaleString();
 document.getElementById('s_inter').textContent=INTER.features.length.toLocaleString();
 document.getElementById('s_rail').textContent=RAIL.features.length.toLocaleString();
}
"""

def build_index():
    files_js="const FILES={"+",".join(f'{k}:"data/{v}"' for k,v in DATASETS.items())+"};"
    loader=(files_js+"""
Promise.all(Object.values(FILES).map(u=>fetch(u).then(r=>{if(!r.ok)throw new Error(u+' '+r.status);return r.json()})))
 .then(arr=>{const K=Object.keys(FILES);const D={};K.forEach((k,i)=>D[k]=arr[i]);init(D);})
 .catch(e=>{document.getElementById('loading').textContent='โหลดข้อมูลไม่สำเร็จ: '+e.message+' — เปิดผ่าน GitHub Pages หรือเว็บเซิร์ฟเวอร์ (ไม่ใช่ file://)';});
""")
    html=f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>แผนที่ทางแยกสัญญาณไฟ · ถนน · ระบบราง · ขอบเขต กทม.</title>
<link rel="stylesheet" href="lib/leaflet.css"/><script src="lib/leaflet.js"></script>
<style>{STYLE}</style></head><body>{BODY}
<script>{APP}
{loader}
</script></body></html>"""
    open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(html)
    return len(html)

def build_standalone():
    css=open(os.path.join(LIB,"leaflet.css")).read()
    js=open(os.path.join(LIB,"leaflet.js")).read()
    consts=[]
    for k,v in DATASETS.items():
        consts.append(f"const {k}=" + open(os.path.join(DATA,v)).read() + ";")
    dobj="{"+",".join(f"{k}:{k}" for k in DATASETS)+"}"
    html=f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>แผนที่ทางแยกสัญญาณไฟ · ถนน · ระบบราง · ขอบเขต กทม. (standalone)</title>
<style>{css}</style><style>{STYLE}</style><script>{js}</script></head><body>{BODY}
<script>{APP}
{''.join(consts)}
init({dobj});
</script></body></html>"""
    open(os.path.join(HERE,"standalone.html"),"w",encoding="utf-8").write(html)
    return len(html)

a=build_index(); b=build_standalone()
print(f"index.html {a/1024:.1f} KB | standalone.html {b/1024:.1f} KB")
