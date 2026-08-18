[README.md](https://github.com/user-attachments/files/31164453/README.md)
# BMA Traffic Boundary Map

แผนที่ Interactive Web Map แสดงข้อมูลด้านการจราจรและขอบเขตความรับผิดชอบในพื้นที่กรุงเทพมหานคร
บนพื้นฐาน [Leaflet](https://leafletjs.com/) + OpenStreetMap

จัดทำและเป็นลิขสิทธิ์ของ PRAPAWADEE WACHIRAPUT
นักวิชาการสถิติชำนาญการ กลุ่มงานสถิติและวิจัย กองนโยบายและแผนงาน สำนักการจราจรและขนส่ง กรุงเทพมหานคร
© Prapawadee_W.
*ไม่อนุญาตให้นำไปใช้เพื่อผลประโยชน์ส่วนบุคคล*

## ชั้นข้อมูล (Map layers)

| Layer | ไฟล์ | รายละเอียด |
|---|---|---|
| ทางแยกสัญญาณไฟ (สีแดง) | `data/junctions.geojson` | 580 จุด จับคู่พิกัดแล้ว |
| จำแนกตามบริษัท/เครื่องควบคุม | `data/junctions.geojson` | สีตามผู้ให้บริการ (Forth/GeTs/Adaptive/PEEK/SCAE/Siemens/TES) |
| จุดสำรวจเวลาเดินทาง | `data/survey_junctions.geojson` | 314 จุด (พิกัดตรวจสอบแล้ว ทศนิยม=DMS) |
| ถนนสายหลัก (เส้นทาง) | `data/road_corridors.geojson` | 51 สาย (แนวโดยประมาณจากจุดสำรวจ) |
| สถานีตำรวจ | `data/police_stations.geojson` | 89 แห่ง (พื้นที่รับผิดชอบ) |
| สำนักงานเขต 50 เขต | `data/bma_districts.geojson` | ระบายสีได้ตามประชากร/ความหนาแน่น/พื้นที่ถนน/ความยาวถนน/จำนวนทางแยก |
| กลุ่มเขต 6 กลุ่ม | `data/bma_zone_groups.geojson` | ประชากรคำนวณจากผลรวม 50 เขต |
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

## เครดิต
- แผนที่ฐาน: © OpenStreetMap contributors, © CARTO, © Esri
- ไลบรารี: Leaflet 1.9.4
- ข้อมูล: PRAPAWADEE WACHIRAPUT นักวิชาการสถิติชำนาญการ กลุ่มงานสถิติและวิจัย กองนโยบายและแผนงาน สำนักการจราจรและขนส่ง กรุงเทพมหานคร
