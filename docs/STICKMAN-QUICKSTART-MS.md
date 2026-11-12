# directing-stickman-videos — pemasangan v0.0.0.6 DRAFT

Skill dipasang pada .agents/skills/directing-stickman-videos dari kaomei/stickman-video-director, commit 7af3957dff97914b2d762fb248ee2427d7fca72c. Semua 448 fail asal dipelihara dan disemak hash; lesen serta manifest sumber disertakan. SKILL.md dibaca sejurus pemasangan. 18 skill terdahulu dikekalkan; registry kini 19. Routing perkataan stickman/stick figure mengenali skill baharu. Ini menambah arahan Codex, bukan integrasi agent video penuh dalam EXE.

A1–A5 Director: hasil ialah cadangan, skrip, storyboard dan prompt video berasingan (lazimnya klip 10 saat). A1 minimalis, A2 moden, A3 komedi prasejarah, A4 cerita santai, A5 sejarah. Merancang tidak memerlukan API; menghasilkan klip memerlukan penjana video seperti Flow dan editor/compositor. Cadangan disemak pengguna sebelum prompt akhir.

A6 Amber Noir: visual bersuasana ambar/gelap, rujukan imej, klip video, narasi Gemini Puck dan finishing MP4; kontrak berasingan daripada A1–A5. Perlu penjana imej/video, laluan Flow/browser atau Renoise yang dikonfigurasi, TTS dan compositor. Akaun/quota dan keserasian mesti disahkan.

B Autopilot: agent menyediakan skrip, imej, suara, sari kata, animasi kecil dan bunyi; runtime tempatan menyusun MP4. B1 garis minimalis, B2 lukisan berwarna, B3 TV retro, B4 thriller survival, B5 pengacara penerangan dengan pentas animasi. B4 menggunakan Brian yang ditetapkan (ai33/ElevenLabs), kecuali pengguna memilih perubahan secara jelas. B5 menggunakan renderer sendiri dan memerlukan imej presenter yang diterima bagi wajah sebenar/kompleks. B3 mempunyai contoh implementasi, tetapi perbandingan dengan video asal peribadi belum tersedia.

Node 20+, FFmpeg, FFprobe, canvas, sharp dan font: doctor PASS pada Linux. Runtime npm dipasang dengan lockfile, --ignore-scripts dan cache /tmp yang boleh ditulis; node_modules tidak di-commit. Install pertama gagal kerana cache home tidak boleh ditulis; cubaan cache /tmp berjaya. 55 unit tests projek, typecheck/build dan Electron smoke Linux PASS. Tiada filem stickman baharu dirender; penjanaan langsung/provider Windows belum diuji. Tiada GPU/model besar atau panggilan berbayar dibuat. EXE v0.0.0.5 pada PC pengguna tidak dikemas kini secara automatik; Windows EXE v0.0.0.6 NOT RUN.

Untuk video penerangan PDF bersuara BM, mulakan B1 untuk rintis ringkas; B5 jika mahu pengacara. Sediakan sumber, sasaran penonton, nisbah/durasi dan gaya. Suara: guna WAV yang sudah diterima atau konfigurasikan laluan TTS yang sah. Key Gemini tidak tersedia dalam persekitaran Codex ini; key yang disimpan dalam aplikasi Windows bukan automatik tersedia di Cloud. Semak akaun/projek/quota Google; jangan tampal rahsia dalam chat. Tool imej tersedia dalam sesi ini, tetapi tidak automatik dipautkan kepada EXE.

Contoh permintaan:

Gunakan directing-stickman-videos, mod A1 tema cerah. Sumber: [teks]. Video 16:9, 60 saat, Bahasa Melayu. Sediakan cadangan dan storyboard dahulu, kemudian prompt selepas saya menyemak cadangan.

Gunakan directing-stickman-videos, mod B1. Tukar sumber berikut menjadi video penerangan BM 60 saat, 1920x1080 30fps, suara jelas dan sari kata BM. Sumber: [teks]. Sediakan skrip dan sampel 15–20 saat dahulu. Gunakan audio saya jika diberi; nyatakan kekurangan sebelum sebarang penjanaan berbayar. Jangan reka fakta di luar sumber.

Lihat sampel A: https://github.com/kaomei/stickman-video-director/blob/main/README.en.md#a-styles
Lihat sampel B: https://github.com/kaomei/stickman-video-director/blob/main/README.en.md#b-styles

Semakan runtime: dari direktori skill jalankan node scripts/autopilot.mjs doctor. Projek pengeluaran mesti di luar direktori skill. Inisialisasi B1: node .agents/skills/directing-stickman-videos/scripts/autopilot.mjs init /workspace/stickman-project-pertama --style B1 . Ini hanya scaffold; perlukan skrip, audio sebenar, caption alignment dan visual sebelum preview/render.

Checkpoint: checkpoint/install-stickman-skill-20261112. Branch: feat/skills-stickman. Tiada merge main atau stable release. Sumber/lockfile kekal dalam Git; dependency cache/node_modules perlu dipasang semula jika persekitaran Cloud diganti.
