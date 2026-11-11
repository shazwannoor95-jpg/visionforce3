# Integrasi Atlas yang benar-benar bergerak

## Kandungan

- Jam dan dispatch
- Layer dan tipografi
- Data, maps dan radar
- Ujian hasil export

## Jam dan dispatch

Panggil API awam `render.frame(pid, t_seconds, cfg, labels=False)`. Jangan memanggil dispatch dalaman dengan saat output melainkan telah membaca kontrak modul. API mengurus 0–5 versus jam saat bagi L01–L06. `gemini_compose.py` menggunakan jam layer `t_global-start`; setiap layer mempunyai duration `end-start`.

Gunakan masa frame deterministik dan seed tetap. Untuk gerak tangan/karakter atau proses panjang, koreografikan aksi setempat dalam scene; jangan hanya melanjutkan satu entrance selama 30 saat. Frame rate ialah kekerapan sampel gerakan, bukannya bilangan tween yang berbeza.

## Layer dan tipografi

Gunakan alpha sebenar dan kanvas berukuran projek. Atlas raster direka 1280×720; eksport 1920 tidak mencipta detail vektor baharu. Jangan crop bounding box berbeza setiap frame kerana ia menyebabkan jitter. Pilih bounds stabil bagi seluruh entrance/hold/exit.

Adapter `--font` mengikat roles sans/bold kepada TTF sebenar. Preset yang menggunakan role mono/serif atau font hardcoded mungkin memerlukan olahan sumber. Menukar medan JSON yang tidak dibaca oleh modul tidak mengubah font. Uji bentuk glyph dan layout pada MP4 akhir.

Ketelusan preset berbeza: latar hardcoded boleh masih memenuhi frame. Semak sebelum menggunakan beberapa preset penuh sebagai overlay. Untuk scene yang padat, gabungkan komponen kecil, crop kawasan yang stabil dan reka letak setiap layer supaya satu focal point kekal jelas.

## Data, maps dan radar

Cari registry dengan nama/mekanisme/tag. Jangan mengandaikan ID rawak mewakili radar. Buka modul dan periksa parameter sebelum menggunakannya. Peta mesti sepadan lokasi/geografi cerita; peta dekoratif tidak menjadi bukti kedudukan sebenar. Radar memerlukan paksi, unit/skala dan data yang diterangkan. Gunakan demo hanya jika ditanda dan sesuai dengan tugas.

Untuk counter, gunakan satu progress yang sama untuk bar/digit dan cue bunyi. Semak nilai akhir. Jangan kira beberapa label/perubahan warna sebagai ID preset baharu. Manifest mencatat ID yang dirancang semasa prompt dan ID yang benar-benar dirender selepas produksi.

## Ujian hasil export

Proof enam sampel adapter membuktikan perbezaan frame, bukan kesempurnaan visual. Buka contact sheet dan tonton potongan MP4 sebenar; periksa gesture/reveal dan bukan overlay progress katalog yang memberi perbezaan palsu. Semak frame daripada fail export setelah encode.

Jalankan full decode dan metadata. Untuk subtitle, semak perkataan yang didengar dengan perkataan yang dipaparkan pada awal/pertengahan/akhir; gunakan audio final sebagai jam. Untuk transition, pastikan frame awal A dan frame akhir B serta tempoh timeline tidak berganda. Untuk overlay, semak Screen tidak memutihkan teks pada latar pastel.

Semua ujian/render menggunakan fail dalam skill yang sudah dipasang. Tiada network fetch, CDN, Google Drive, TTS cloud atau pemasangan package semasa render offline. Jika dependency tiada, laporkan komponen yang terjejas; jangan menggantikan video dengan paparan kod sambil mengaku render berjaya.
