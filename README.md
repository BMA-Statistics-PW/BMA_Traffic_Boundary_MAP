[README.md](https://github.com/user-attachments/files/31164453/README.md)
# BMA Traffic Boundary Map

แผนที่เชิงโต้ตอบ (interactive web map) แสดงข้อมูลจราจรและขอบเขตความรับผิดชอบในพื้นที่กรุงเทพมหานคร
บนพื้นฐาน [Leaflet](https://leafletjs.com/) + OpenStreetMap — สำหรับกลุ่มงานสถิติและวิจัย กองนโยบายและแผนงาน สำนักการจราจรและขนส่ง กทม.

© Prapawadee_W.

## ชั้นข้อมูล (Map layers)

| Layer | ไฟล์ | รายละเอียด |
|---|---|---|
| ทางแยกสัญญาณไฟ (สีแดง) | `data/junctions.geojson` | 580 จุด จับคู่พิกัดแล้ว |
| จำแนกตามบริษัท/เครื่องควบคุม | `data/junctions.geojson` | สีตามผู้ผลิตอุปกรณ์ (Forth/GeTs/Adaptive/PEEK/SCAE/Siemens/TES) |
| จุดสำรวจเวลาเดินทาง | `data/survey_junctions.geojson` | 314 จุด (พิกัดตรวจสอบแล้ว ทศนิยม=DMS) |
| ถนนสายหลัก (เส้นทาง) | `data/road_corridors.geojson` | 51 สาย (แนวโดยประมาณจากจุดสำรวจ) |
| สถานีตำรวจ | `data/police_stations.geojson` | 89 แห่ง (พื้นที่รับผิดชอบ) |
| สำนักงานเขต 50 เขต | `data/bma_districts.geojson` | ระบายสีได้ตามประชากร/ความหนาแน่น/พื้นที่ถนน/ความยาวถนน/จำนวนทางแยก |
| กลุ่มเขต 6 กลุ่ม | `data/bma_zone_groups.geojson` | ประชากรคำนวณใหม่จากผลรวม 50 เขต |
| สถิติถนนรายเขต | `data/district_road_stats.json` | พื้นที่/ความยาว/จำนวนถนน ต่อเขต (ใช้ join กับ choropleth) |

พิกัดทั้งหมดเป็น **WGS84 / EPSG:4326** (lon, lat) ใช้ได้กับ Leaflet, QGIS, Mapbox, geopandas ฯลฯ

## โครงสร้างโปรเจกต์

```
BMA_traffic_boundary_map/
├── index.html          # แผนที่หลัก (โหลดข้อมูลจาก data/ แบบ fetch) — สำหรับ GitHub Pages
├── standalone.html     # เวอร์ชันฝังข้อมูลในไฟล์เดียว (เปิดด้วย double-click ได้เลย ไม่ต้องมีเซิร์ฟเวอร์)
├── lib/                # Leaflet 1.9.4 (vendored — ไม่ต้องพึ่ง CDN)
├── data/               # ไฟล์ GeoJSON / JSON ทั้งหมด
├── .nojekyll           # ปิดการประมวลผล Jekyll บน GitHub Pages
└── README.md
```

> **สำคัญ:** `index.html` โหลดข้อมูลด้วย `fetch()` จึงต้องเปิดผ่าน **HTTP server** (เช่น GitHub Pages) ไม่สามารถเปิดด้วย `file://` (double-click) ได้
> ถ้าต้องการเปิดแบบ offline ให้ใช้ `standalone.html` แทน

## วิธีนำขึ้น GitHub Pages

```bash
cd D:\GitHub\BMA_traffic_boundary_map
git init
git add .
git commit -m "Initial commit: BMA traffic boundary map"
git branch -M main
git remote add origin https://github.com/<username>/BMA_traffic_boundary_map.git
git push -u origin main
```

จากนั้นที่หน้า repo บน GitHub → **Settings → Pages** → เลือก Source เป็น `Deploy from a branch` → เลือก branch `main` และโฟลเดอร์ `/ (root)` → **Save**

รอสักครู่ แผนที่จะเผยแพร่ที่:
```
https://<username>.github.io/BMA_traffic_boundary_map/
```

## ทดสอบในเครื่อง (local preview)

เนื่องจาก `index.html` ต้องใช้ HTTP server ให้รันคำสั่ง (ต้องมี Python):

```bash
cd D:\GitHub\BMA_traffic_boundary_map
python -m http.server 8000
```

แล้วเปิดเบราว์เซอร์ไปที่ `http://localhost:8000/`

## การนำข้อมูลไปใช้งานต่อ

ไฟล์ในโฟลเดอร์ `data/` เป็น GeoJSON มาตรฐาน สามารถ:
- โหลดใน **QGIS / ArcGIS** เพื่อทำแผนที่/วิเคราะห์เชิงพื้นที่
- อ่านด้วย **Python (geopandas)**: `gpd.read_file('data/junctions.geojson')`
- ใช้เป็น layer ใน **Mapbox / MapLibre / Leaflet** โปรเจกต์อื่น
- join กับข้อมูลจราจร (ปริมาณจราจร/อุบัติเหตุ/CCTV) ผ่านรหัส กทม. หรือชื่อเขต

## หมายเหตุคุณภาพข้อมูล
- กลุ่มเขต "กรุงเทพใต้" ค่าประชากรต้นฉบับผิดปกติ → ใช้ค่าคำนวณใหม่จากผลรวม 50 เขต (ฟิลด์ `*_calc`)
- รหัสสัญญาณไฟ **830** ชนกันระหว่างแหล่งข้อมูล (นวธานี vs เสรีไทย 38) — ควรตรวจสอบ
- เส้นถนน 51 สายเป็นแนวโดยประมาณจากลำดับจุดสำรวจ ไม่ใช่ centerline ที่แม่นยำระดับสำรวจ

## เครดิต
- แผนที่ฐาน: © OpenStreetMap contributors, © CARTO, © Esri
- ไลบรารี: Leaflet 1.9.4
- ข้อมูล: สำนักการจราจรและขนส่ง กรุงเทพมหานคร
