---
name: buat-video-motion-grafik-gemini
description: Cipta MP4 atau prompt motion grafik dalam Gemini Task/Spark. Semak cache dan storan VM dahulu, kemudian muat turun hanya pek yang diperlukan dan hilang atau tidak sah. Gunakan 922 preset Atlas termasuk Creator FX 80 melalui runtime Python asal terkunci; Python/FFmpeg untuk suntingan video dan HTML/GSAP + HyperFrames untuk animasi vektor/kartun. Sokong semua gaya terkini termasuk Vox berkanvas bersambung, Cinematic Papercut, Bang Motion, Website Launch, creator reels, subtitle Arab–Melayu, Whisper, RVM serta MeloTTS-MS + Malay BERT daripada Drive dalam bahagian bawah 10 MB. Render offline selepas keperluan projek tersedia.
---

# Buat Video Motion Grafik — Gemini

Ikut arahan pengguna terkini dan bahasa Melayu Malaysia. Hasilkan MP4 sebenar apabila diminta video siap. Jika diminta prompt, tulis prompt lengkap dalam satu code block tanpa memulakan render. Kekalkan kandungan/audio/rujukan yang telah dipersetujui. Gunakan sumber dan fail sebenar; jangan dakwa telah diuji dalam akaun Gemini jika hanya diuji di runtime lain.

Keluaran dan model: baca [pautan Drive versi semasa](references/drive-release.md). Semua fail keluaran, model dan panduan mesti berada terus dalam folder utama Drive yang dinyatakan. Jangan cipta subfolder Drive baharu; gunakan fail dan ID sedia ada apabila mengemas kini.

## Kemas kini lengkap 10 November 2026

Baca [panduan produksi penuh](references/source-production-guide.md) untuk semua fungsi/gaya sumber utama yang dibawa ke Gemini. Gunakan rujukan asal bersama fail kod/aset dalam pek semasa; arahan persekitaran, cache, suara serta lokasi fail dalam SKILL.md Gemini mengatasi contoh khusus ChatGPT. Jangan andaikan alat ChatGPT, Library, path projek lama atau kunci API tersedia di Gemini.

- **Gaya**: Gaya Ekstrem, Salah Label, enam gaya sosial, Cinematic Creator Reel, Dark Tech Editorial, Glass Creator Reel, Motion FX Creator Reel, Cinematic Papercut dan Website Launch. Baca fail gaya masing-masing di `references/`.
- **Empat koleksi**: [Bang Motion](references/collection-bang-motion.md), [Vox Explainer](references/collection-vox-explainer.md), [Huashu Art Motion](references/collection-huashu-art-motion.md), [Claude Drawing](references/collection-claude-drawing.md). `python3 scripts/style_collection.py stats/list/search/show/validate` menggunakan indeks semasa dalam `assets/style_collections/`; label BM/VX/HA/HG/DD berasingan daripada Atlas 922.
- **Vox terkini**: baca [kanvas bersambung dan cutout 3D](references/vox-connected-canvas.md). Kamera ke kanan membuat dunia/kanvas tampak bergerak ke kiri; gunakan objek beraksi, 2.5D, parallax, zoom dramatik dan handoff berantai. Pilih lima gabungan gaya serta nyatakan bilangan imej unik/aksi jika diminta sebelum produksi. Subtitle centre-safe dengan active-word highlights; teks lain pada imej torn-paper, kecuali segmen penerangan infografik yang boleh menggunakan teks/rajah biasa.
- **Cinematic Papercut**: fotografi raster dengan alpha sebenar, tiada prop SVG untuk gaya ini, kamera sinematik dan imej unik. Rujukan 2 minit menggunakan 50 imej/54 mekanisme tipografi; skala mengikut brief, bukan wajib semua projek.
- **Website Launch**: b-roll laman sebenar, perspektif, carousel padat, typography besar dan perubahan layout; ikut kuantiti brief. **Bang Motion** boleh tanpa manusia/VO, poster color block + editorial light seimbang dengan SFX/ASMR pada setiap cue apabila diminta.
- **Produksi**: semua rujukan tambahan untuk showcase, scene panjang, caption tengah, portrait, kinetic typography, live-commerce, Learnfly, peta, rig/IK, planet, fon Arab dan ceramah Arab–Melayu disertakan. Baca bahagian sepadan dalam panduan produksi penuh dan fail rujukannya; kekalkan checkpoint/audio projek semasa.
- **Runtime**: gunakan `assets/runtime-lock.json` serta [toolkit komponen](references/video-component-toolkit.md) daripada semakan 3 November, HyperFrames 0.9.4 + GSAP 3.15.0. Cache/preflight sebenar tetap diperlukan; pemindahan arahan tidak bermakna semua runtime/model sudah terpasang.
- **Voice-over baharu BM**: ikut [MeloTTS-MS + Malay BERT](references/melotts-malay-voiceover.md). Muat turun bahagian model dari Drive, cantum/sahkan dengan `scripts/model_bundle.py`, kemudian pasang/uji dengan `scripts/setup_melotts.py`. Kekalkan suara sedia ada yang telah diluluskan. Jangan menggantikan arahan Google AI Studio yang pengguna tetapkan secara khusus.
- **Katalog**: [Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site). Jangan bina laman baharu untuk permintaan pautan sahaja.

## Dependency VO mesti dipasang bersama skill

Baca [pakej dependency VO offline](references/offline-vo-dependencies.md). Pemasangan penuh skill Gemini kini mesti menyertakan Python 3.11, espeak-ng/libespeak-ng1 + data/library serta wheelhouse torch, torchaudio, transformers, malaya, malaya-speech dan phonemizer beserta dependency transitif. Semak cache dahulu, pulihkan tiga komponen daripada manifest dependency Drive, jalankan `install_vo_dependencies.py`, kemudian `setup_melotts.py --dependency-root` untuk inferens Melayu sebenar. Gunakan profil Linux x86_64/glibc >= 2.35/CPU yang disahkan; jangan menganggap wheel serasi semua OS/Python. Semua fail kekal terus dalam folder utama dan bawah 10 MB. Jangan memasang semula pakej bagi setiap projek atau memerlukan apt/pip online selepas bundle lengkap tersedia.

## 1. Semak cache dan storan VM dahulu

Baca `references/selective-cache.md` serta manifest keluaran terkini. Resolusi root sebenar daripada persekitaran Gemini; jangan andaikan `/root/.codex` atau storan sementara kekal. Gunakan direktori projek berasingan daripada cache toolkit.

1. Kenal pasti fungsi yang diperlukan: preset, kartun HTML, watak, SVG, fon tambahan, montaj, Whisper atau matting. Semak fail pada root skill, cache pakej dan storan VM yang diketahui; jangan mengimbas semua fail pengguna tanpa sebab.
2. Jalankan `scripts/gemini_cache.py plan` dengan manifest dan `--need` untuk kategori yang diperlukan sahaja. Cache sah memerlukan saiz dan SHA-256 fail sepadan, bukan kewujudan folder kosong.
3. Jika fail diekstrak sah tersedia, guna semula. Jika ZIP sah tersedia, ekstrak dari storan tempatan. Muat turun hanya pek bertanda `download-required` melalui saluran Drive yang benar-benar boleh memindahkan bait fail.
4. Jalankan `install` ke root keluaran berasingan. Jangan menimpa fail suntingan pengguna; pemasang menolak konflik. Kemudian `verify` untuk pek terpilih dan preflight runtime khusus. Status pek tersedia tidak membuktikan FFmpeg/model/Chrome sudah berfungsi.
5. Render offline selepas SEMUA keperluan projek terpilih tersedia. Jika perlu aset baharu, kembali ke persediaan dan ambil pek berkaitan sahaja. Jangan wajibkan SEMUA pek katalog pada setiap projek atau pemasangan pertama.
6. Kekalkan cache, ZIP sah, model, dependency serta receipt versi selepas membersihkan frame render. Semak semula selepas sesi/VM bertukar. Jika offline dan fail perlu tiada, laporkan fail tepat yang hilang; jangan mencuba muat turun berulang atau mendakwa berjaya.

Folder keluaran: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF
Rujuk `references/selective-cache.md` untuk pautan manifest dan pek terkini. Pakej lama 22 Oktober bukan lalai bagi runtime Atlas terkunci ini. Jangan mencampur renderer lama dengan kontrak baharu.

## 2. Pilih backend mengikut tugas

Baca `references/hyperframes-nine-workflows.md` untuk explainer, pelancaran produk, motion graphic pendek, muzik/lirik, data/peta, avatar, GitHub PR, slideshow interaktif dan video campuran. Gunakan panduan dan kajian visual 10 contoh dalam `references/hyperframes-codex-examples.md` untuk koreografi; sesuaikan akses dan arahan kepada Gemini. Satu idea boleh dibangunkan dalam scene panjang dengan banyak prop dan pertukaran teks. Untuk MP4 daripada slaid, bina root master timeline penuh; jangan render deck interaktif sehingga hanya slaid pertama dieksport.

- Sunting video sedia ada terus dengan Python/FFmpeg: cut, reframe, subtitle, kinetic title, komposit, muzik, SFX dan eksport.
- Animasi vektor/kartun: HTML/GSAP + HyperFrames dengan SVG berlapis, pivot, rig/IK, kamera/parallax dan timeline seekable. HTML ialah struktur/render; GSAP mengurus animasi.
- Projek campuran: render lapisan yang diperlukan, kemudian komposit melalui Python/FFmpeg. Jangan mewajibkan HTML/GSAP pada setiap video.
- Baca `references/html-hyperframes-production.md` dan `references/hyperframes-motion-bank.md` hanya untuk laluan HTML. Semak dependency/cache dahulu; sediakan Node/Chrome yang serasi jika diperlukan. Gunakan `paused:true`, `window.__timelines`, masa eksplisit dan gate fon/aset, tiada ticker bebas.

### Pasang dan jalankan HyperFrames dalam Gemini

Baca `references/gemini-hyperframes-install.md`. Semak Node.js 22.12+, npm, FFmpeg/ffprobe, runtime HyperFrames 0.9.4, GSAP 3.15.0 dan Chrome sebenar dahulu. Jalankan `node scripts/setup_hyperframes.mjs` sebagai preflight; jika belum ready dan rangkaian tersedia, gunakan `--online` sekali untuk pemasangan terkunci. Gunakan `--install-offline` hanya dengan npm cache lengkap pada OS/CPU yang serasi. Kekalkan cache runtime dan `KM_HYPERFRAMES_RUNTIME`; jangan memuat turun semula dependency yang sah atau menyamakan folder/npm cache dengan browser yang sudah boleh dilancarkan. Laluan produksi ialah `doctor → lint → check → snapshot/proof → render → QA`. Skrip render setempat tidak memasang dependency ketika capture.

## 3. Preset Atlas mesti menggunakan kod asal

Baca `references/atlas-python-runtime.md`, `references/creator-fx-80.md` dan metadata ID yang dipilih. Wajib gunakan `scripts/atlas_preset.py` atau API `AtlasPreset`. `gemini_atlas.py` ialah alias CLI yang sama, bukan renderer berasingan. Jangan membina semula efek berdasarkan nama/preview atau menukar easing/timing dalaman tanpa varian yang diuji.

```bash
python scripts/atlas_preset.py list --search scroll
python scripts/atlas_preset.py describe CFX15
python scripts/atlas_preset.py init CFX15 --output /path/project/job.json
python scripts/atlas_preset.py check /path/project/job.json
python scripts/atlas_preset.py render /path/project/job.json --output /path/project/layer.mp4
python scripts/atlas_preset.py verify /path/project/job.json --video /path/project/layer.mp4 --report /path/project/qa.json
```

Untuk konfigurasi katalog lama, gunakan `import-config old.json --output job.json`. Edit hanya parameter yang disokong. Cue dalam job menggunakan saat output sebenar; jangan menormalisasi dua kali. Wrapper mengesahkan registry, versi kod/aset/fon, baseline dan cache. Jangan membina semula lock untuk memintas kegagalan.

922 entri = 137 asal + 185 demo MS/PL/PV/AD + 120 EV + 400 PX + 80 CFX. MA ialah koleksi berasingan. ID preset bukan teks video; panggil fungsi sebenar bagi setiap frame. Default produksi tanpa label katalog.

Untuk footprint pada footage, pilih mode footage dan bekalkan frame sebenar, alpha subjek, backdrop, tracking atau sejarah frame sebagaimana kontrak ID. CFX15 default footage penuh; kemunculan panel ikut gerakan tangan memerlukan cue/anchor sebenar, bukan andaian tracking automatik. CFX12/40 memerlukan remap source time sebenar; CFX20 memerlukan sejarah echo. Jangan ganti input hilang dengan demo sintetik.

Native canvas 1280×720. Letakkan layer 16:9 secara berkadar atau bina varian portrait yang diuji; jangan meregang atau memotong teks untuk 9:16. Render senyap tidak membawa audio asal: campur audio dalam editor. Baseline bukan jaminan semua teks/layout atau semua preview luaran tepat.

## 4. Gaya, tipografi dan koreografi

Gunakan palet cerah lembut bagi projek baharu tanpa rujukan lain: cream #F8F3E8, panel #E8E0CF, teks #263645, aksen #447891. Jika diminta sama seperti Atlas, kekalkan palet/default Atlas. Tetapkan warna melalui params yang disokong; jangan mengubah fail renderer terpinkan atau fon global secara senyap.

Bezakan subtitle penuh daripada title kinetik. Jika diminta per perkataan, animasikan kemunculan setiap perkataan sambil mengekalkan perkataan terdahulu hingga ayat lengkap apabila sesuai. Variasikan mekanisme mengikut mesej dan ruang bacaan. Gunakan satu aksi utama; jadualkan entrance, hold, exit, handoff dan SFX secara eksplisit.

Untuk gaya **Salah Label**, bina satu ruang berterusan dengan SVG berlapis, campuran flat 2D, 2.5D dan perspektif terpilih. Prop baharu dibina berperingkat; prop selesai mengecil, berpindah atau hilang sambil aksi seterusnya bermula. Teks dan prop boleh bertukar lokasi kiri/kanan/tengah/atas/bawah apabila layout berubah, kemudian teks berhenti untuk dibaca. Variasikan mask, stroke, highlight, shadow, glow/neon atau depth mengikut mesej. Kamera mesti menuju objek atau menunjukkan hubungan. Kekalkan hero antara beat; satu gambar penuh dengan zoom sahaja tidak memenuhi animasi prop. Hormati tanpa VO dan durasi tepat yang pengguna tetapkan.

Jangan wajibkan semua 80 CFX atau bilangan preset tertentu tanpa brief. Untuk projek kompleks, baca `references/director-critic-qa.md`: brief, persistent hero, tiga signature moments, storyboard, timing audio, proof 3–5 saat, critic ledger dan QA sebelum master. Prinsip kreatif tidak mengatasi permintaan pengguna.

## 5. Aset, fon, model dan cache pilihan

| Keperluan | Pek/kandungan |
|---|---|
| Atlas/CFX | core + atlas_locked untuk API terpinkan; presets pilihan bagi kod/katalog asal |
| Vektor/kartun HTML | core; sediakan dependency HTML hanya apabila perlu |
| Watak V3 | core + characters |
| SVG/MA | core + svg atau motion_array |
| Fon tambahan | fonts; gunakan fail TTF dan lesen sebenar |
| Montaj/LUT/SFX | core + hanya vlog_payload yang memuatkan aset terpilih |
| Preview katalog | previews pilihan; tidak wajib untuk render |

Semak indeks untuk menentukan pek aset. Payload VL perlu dipulihkan hanya bagi aset/pek terpilih dengan utiliti yang tersedia; jangan label koleksi penuh tersedia jika sebahagian sahaja dipasang. Model besar tidak dibundel dalam ZIP kod. Semak cache model dan inferens dahulu. Untuk Whisper baca `references/media-tools.md`; gunakan model projek yang disahkan dan jangan turun taraf secara senyap. Untuk matting manusia baca `references/video-background-replacement.md`; RVM temporal, reset pada cut, proof alpha/tepi dan jaga audio. Semak offline dahulu; jika fail perlu hilang, sediakan hanya dependency/model berkaitan semasa online.

## 6. Prompt dan komposisi

Prompt mesti mengandungi objektif, orientasi/resolusi/durasi, scene/timing, teks, aset, preset ID sah, palet, cue audio, backend dan QA. Masukkan aturan cache-first dan muat turun terpilih; jangan menyatakan semua fail sudah dipasang tanpa bukti. Jika indeks tidak tersedia, arahkan semakan ID sebelum render dan jangan cipta ID.

Untuk beberapa preset dalam scene, sediakan setiap job terpinkan, start/end dan rect. Gunakan API `AtlasPreset.frame(t_local)` atau komposit hasil layer yang telah dirender. Gunakan masa `i/fps`, nisbah berkadar, alpha sah dan manifest ID sebenar. `scripts/gemini_compose.py` menerima `layers[].job` sebagai path job terpinkan; ia kompositor native, bukan pengganti penyedia footage/tracking.

## 7. Watak, 2.5D, kamera dan audio

Gunakan bank V3 20 watak sopan tempatan; kekalkan ID, rupa, pakaian dan `height_cm` supaya nisbah antara kanak-kanak/dewasa logik. Baca `references/character-bank-20.md`, `references/local-vector-animation.md` dan `references/vector-cinematic-motion.md`. Pastikan hierarki sendi bersambung, garis aksi, pemindahan berat, tangan menggenggam props, kaki berpijak, overlap dan easing lancar. Render tiga styleframe dan petikan aksi 3–5s secara dalaman sebelum master. Jangan menambah gate kelulusan jika pengguna sudah meminta penghasilan penuh.

Gunakan orientasi `front`, `back`, `side_right`, `side_left`, `three_quarter_right`, `three_quarter_left`; `side` dan `three_quarter` ialah alias kanan. Artwork belakang tidak mempunyai ciri wajah/butang hadapan; sudut kiri memantulkan tubuh, kepala dan props. Asingkan tulisan/logo dan perincian pakaian anatomi yang tidak boleh dipantulkan. Jangan paksa `--view` pada aksi turn yang perlu bertukar sudut.

```bash
python scripts/character_bank.py list --kind motions
python scripts/character_bank.py render --character P04 --motion walk_across --view side_left --width 720 --height 1200 --fps 30 --output /path/project/mira_walk_left.mp4
python scripts/character_bank.py render --character L05 --pose stand_back --output /path/project/amir_back.png
python scripts/vector_character_camera.py --demo --duration 4 --fps 30 --width 1280 --height 720 --output /path/project/camera.mp4
```

`walk_side_left`/`walk_side_right` ialah loop berjalan setempat; `walk_across` dengan view sisi menghasilkan perjalanan merentasi skrin. Gunakan satu viewBox sepanjang shot, skala `height_cm` sebenar dan `t=frame/fps`. Panggil `poseState`/`sampleMotion` diikuti `rigSvg` bagi komposisi tersendiri. Gerakan baharu meliputi turn belakang/hadapan dan kiri/kanan, mengeluh, mengelap air mata, makan/minum, doa, perbualan telefon dan menunggang prop motosikal. Turn ialah pertukaran artwork 2D dengan unjuran mendatar, bukan morph 360°/3D; mulut demo tidak menyediakan lip-sync audio automatik. Periksa kontak, genggaman, kaki dan lipatan pakaian.

Baca `references/vector-camera-engine.md` untuk kamera/IK Python. Demo Python mempunyai tiga role contoh `amir`, `mak`, `abah`; ia bukan pemuat automatik bank 20 ID L/P. Gunakan renderer SVG untuk bank 20, kemudian komposit ke scene. Contoh 16-scene asal ialah mod pilihan yang memerlukan path projek, fon, RMS dan audio eksplisit; jangan menganggap fail projek lama tersedia atau menyalin kandungan khusus itu ke semua video.

Bezakan world space dan screen space; bina foreground/midground/background untuk parallax, kamera dolly/zoom/pan dan fokus subjek. Gunakan `scripts/advanced_planet_engine.py` untuk planet 2.5D serta `references/advanced-planet-rendering.md` jika relevan. Jangan mendakwa 2.5D ialah mesh/rig 3D penuh.

Voice-over BM Malaysia: gunakan MeloTTS-MS + Malay BERT mengikut `references/melotts-malay-voiceover.md` bagi VO baharu apabila tiada penyedia khusus diminta. Baca panduan itu sebelum pemasangan/sintesis. Jangan panggil TTS cloud semasa offline. Arahan tanpa VO, fail diluluskan dan pilihan penyedia eksplisit mengatasi lalai. Sintesis muzik/SFX melalui kod jika diminta; bezakan narasi, muzik, SFX dan ASMR dalam mix.

Jadikan audio akhir jam utama. Ukur durasi sebenar, sediakan cue onset/offset perkataan/frasa dan semak subtitle awal, pertengahan serta akhir. Jangan guna anggaran perkataan semata-mata sebagai bukti sync. Bar waveform/audiogram hendaklah berpunca daripada RMS/envelope audio sebenar jika disebut sebagai bar suara.

## 9. Produksi dan QA wajib

1. Tetapkan orientasi, resolusi, FPS, tempoh, nada, bahasa dan kandungan daripada brief; jika tiada, pilih 1920×1080/30 fps dengan palet krim dan durasi yang sesuai dengan mesej. Had setiap scene mengikut arahan pengguna, bukan sentiasa 3s bagi semua projek.
2. Bina manifest scene: start/end, teks, preset ID sah, ID aset, font path, palet, data, cue audio dan mekanisme gerak. Kira ID unik yang benar-benar digunakan; jangan kira pengulangan sebagai preset baharu.
3. Render petikan beberapa mekanisme, font dan palet; buka frame dan tonton petikan. Baiki ejaan, clipping, alpha, kontras, gerakan kaku serta perkadaran.
4. Render scene menggunakan masa `i/fps`, seed tetap dan aset tempatan. Jangan menahan semua frame video panjang dalam RAM; stream ke FFmpeg atau render segmen dengan saiz/FPS/codec seragam. Simpan checkpoint untuk projek panjang.
5. Gabungkan scene dan audio. Periksa potongan, tiada flash bingkai hitam, subtitle penuh, waveform sebenar, SFX dan penutup. Jangan anggap menukar metadata kepada 60 fps menghasilkan 60 frame animasi unik.
6. Jalankan ffprobe untuk resolusi/FPS/durasi/frame count dan nyahkod seluruh MP4. Ekstrak semula frame daripada fail akhir, bukan hanya frame sebelum encode. Semak awal/akhir setiap scene, puncak animasi, semua teks dan audio pada kelajuan biasa.
7. Serahkan MP4 sebenar serta kod/projek apabila diminta. Nyatakan batas yang benar-benar ditemui. Jangan mendakwa sudah diuji pada Gemini Spark jika hanya diuji pada runtime lain; bezakan ujian portabiliti offline daripada ujian dalam akaun Gemini pengguna.

```bash
ffprobe -v error -show_streams -show_format -of json /path/project/final.mp4
ffmpeg -v error -i /path/project/final.mp4 -f null -
```

Untuk projek kompleks/hingga 30 minit baca `references/master-instruction-v6.md`, `references/advanced-motion-graphics.md`, `references/motion-patterns-envato.md` dan `references/local-video-pipeline.md`. Gunakan isi teknikal yang berkaitan; jangan import tool, path, storan, aturan penerbitan atau andaian akses ChatGPT ke Gemini. Kekalkan semua kerja render sepenuhnya tempatan selepas pemasangan.

## 10. Keluaran Drive dan had fail

Semua fail keluaran baharu mesti **kurang daripada 10,000,000 bait**; sasarkan maksimum **8,000,000 bait** bagi bahagian model dan kurang daripada 8 MiB bagi pek toolkit. Jangan muat naik model mentah yang melebihi had. Keluaran 10 November mempunyai manifest toolkit serta manifest model berasingan; baca panduan setup dalam folder Drive untuk pautan tepat dan hash manifest.

Berat MeloTTS-MS, Malay BERT, tokenizer/config dan source archive diletakkan dalam bahagian bernombor di Drive. Muat turun semua bahagian bagi model terpilih sahaja, cantum secara streaming, semak hash setiap bahagian serta fail penuh, kemudian gunakan path model setempat. Model besar kekal di cache VM, bukan direktori kod skill. `model_bundle.py` menolak fail tidak lengkap, path traversal dan konflik dengan suntingan pengguna. Set `MODEL_ID` kepada direktori Malay BERT setempat **sebelum** mengimport `melo`.

Jangan menggunakan `gemini_install.py` legacy sebagai lalai kerana ia memasang semua pek. Gunakan `gemini_cache.py` untuk toolkit terpilih. Manifest tidak membenam hash dirinya atau fail yang merujuknya secara kitaran. Simpan fail lama; keluaran bertarikh dan manifest semasa menentukan versi yang perlu digunakan.
