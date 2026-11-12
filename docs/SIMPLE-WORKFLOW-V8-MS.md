# Aliran ringkas — v0.0.0.8 DRAFT

Permintaan tugasan ini ialah membuka aplikasi, upload bahan, tulis prompt, login agent hanya jika perlu, kemudian dapatkan video. Skrin utama kini mengikuti urutan itu. Projek, runtime, skills, sambungan browser dan menu lama dikekalkan melalui Lanjutan; pengguna baharu tidak perlu menyediakan worker atau menamakan projek dahulu.

## Cara guna

1. Tutup aplikasi versi lama, kemudian buka EXE v0.0.0.8. Semak nombor versi di bawah skrin.
2. Pilih fail untuk video. PDF berteks, DOCX, PPTX, TXT/MD dan PNG/JPEG disokong. Nama projek diambil daripada fail pertama. Bahan asal disalin ke ruang projek.
3. Tulis arahan, contohnya:

   `Buat video penerangan 30 saat dalam Bahasa Melayu berdasarkan bahan ini. Pilih isi penting, gunakan motion graphics yang kemas, format 16:9.`

   Untuk potret: `Ringkaskan bahan ini menjadi video 45 saat Bahasa Melayu untuk TikTok, format 9:16.`
4. Tekan Jana video. Jika sesi/key belum tersedia, dialog sambungan muncul tanpa memadam bahan dan prompt. Selepas sambungan disahkan, tugas yang menunggu disambung.
5. Tunggu bacaan bahan, pelan agent dan render setempat selesai. Kemajuan dan ralat sebenar dipaparkan. Cuba semula ialah tindakan pengguna, bukan permintaan berbayar yang diulang secara automatik.
6. Tonton video siap. Semak teks dan sumber boleh dibuka untuk melihat petikan bukti. Pilih Simpan video dan nama MP4 baharu. Projek dan hasil kekal selepas aplikasi dibuka semula.

Projek di bahagian atas membuka sejarah dan Video baharu. Lanjutan membuka alat lama, termasuk Stickman Studio, Browser Automation, Skills dan backup/restore. Tiada menu GPU atau editor baharu ditambah.

## Sambungan yang digunakan

| Pilihan | Apa yang diperlukan | Cara ia digunakan |
|---|---|---|
| Codex · Akaun ChatGPT | Akaun dengan akses Codex dan kuota yang mencukupi | CLI rasmi `@openai/codex` 0.167.2 yang dibundel. Login ChatGPT/Codex memaparkan halaman OpenAI dan kod peranti; alternatif Login melalui browser menggunakan aliran rasmi CLI. |
| OpenAI · API | API key dan akses model API | Responses API rasmi; lalai `gpt-4.1-mini`. |
| Claude · API | Anthropic API key dan akses model | Messages API rasmi; lalai `claude-sonnet-4-5`. |
| Gemini · API | Gemini API key bagi projek yang dibenarkan | Generative Language API rasmi; lalai `gemini-2.5-flash`. |

Model boleh ditukar melalui Model (pilihan) jika akses akaun berbeza. Key baharu diuji melalui akses baca API sebelum menggantikan key tersimpan; ini tidak menjamin inferens atau billing. Akses penjanaan sebenar diperiksa ketika tugas dijalankan. Sesi tersedia tidak ditafsirkan sebagai semua model telah lulus ujian.

Codex menggunakan `CODEX_HOME` khusus dalam data aplikasi dan storan credential OS (`keyring`). Profil Codex/Chrome peribadi tidak diimport. Aplikasi tidak mengendalikan password pengguna atau menyalin cookie daripada browser peribadi. Kod login hanya dipaparkan selepas pengguna memulakan aliran rasmi. Jika kod peranti tidak dibenarkan bagi akaun, gunakan Login melalui browser. Log keluar tersedia untuk menyambung akaun Codex semula.

Langganan web ChatGPT, Claude atau Google tidak memberikan key/kredit API secara automatik. Login Google AI Studio dalam Browser Automation bukan sesi inferens agent ini. Ralat Google `permission denied` perlu diselesaikan pada kebenaran projek/API/akaun Google; aplikasi tidak boleh meluluskan projek Google bagi pihak pengguna. Untuk laluan tanpa key OpenAI, pilih Codex dan lengkapkan login akaun yang mempunyai akses Codex.

API key disulitkan dengan storan OS. Penyimpanan plaintext ditolak jika backend selamat tidak tersedia. Bahan dihantar kepada agent yang dipilih hanya apabila Jana ditekan, mengikut kuota/caj akaun/API itu. Tiada fallback provider atau panggilan berulang secara automatik.

## Apa yang terhasil

Agent membaca teks dokumen dan imej yang dibekalkan, kemudian menghasilkan pelan babak JSON. Adapter memeriksa ID sumber, petikan bukti, ID imej, saiz teks dan durasi. Pelan ialah data; kod/perintah model tidak dijalankan. Codex exec menggunakan sandbox read-only, tools pelaksanaan dimatikan dan tidak membaca arahan profil/skills peribadi.

Renderer tetap menggunakan Canvas/font yang telah dibundel dan FFmpeg setempat untuk tajuk, teks, imej pengguna serta animasi ringkas. Output MP4 H.264 ialah 1920×1080 atau 1080×1920 pada 30fps, dengan SRT, pelan, peta sumber, log, SHA-256 dan bukti FFprobe/decode. Aliran ini tidak memerlukan worker Cloud lama. Worker Remotion lama kekal berasingan melalui Lanjutan dan terus diuji dalam CI.

Lalai ialah video teks bergerak tanpa narasi. Untuk suara, buka Pilihan suara → Tambah narasi Gemini, atau nyatakan narasi/voice-over dalam prompt. Gemini API yang berasingan diperlukan walaupun agent teks ialah Codex. Key suara tidak menukar agent teks pilihan. Narasi dijana setiap babak, dicantumkan dan diselaraskan kepada frame; durasi mengikut audio sebenar, tanpa mempercepat suara untuk memaksa sasaran. Audio yang sudah siap boleh digunakan semula pada retry yang sama. Ujian automatik audio menggunakan nada sintetik, bukan bukti kualiti suara model sebenar.

## Batas semasa

- Durasi sasaran 2–120 saat, sehingga 8 babak. Narasi sebenar boleh mengubah panjang; hasil terlalu panjang ditolak dengan ralat jelas.
- Sehingga 20 bahan, 50 MiB setiap lampiran. Bacaan PDF maksimum 60 halaman dan jumlah teks maksimum 60,000 aksara. PDF imbasan memerlukan OCR di luar laluan ini; dokumen terlalu panjang tidak dipotong secara senyap.
- Sehingga 4 imej, setiap satu maksimum 5 MiB sebelum pemprosesan. Imej dipadankan ke ruang yang tersedia, metadata dibuang sebelum dihantar.
- Tiada transkripsi audio/video atau penjanaan klip AI/GPU dalam aliran ringkas ini. Gaya Stickman khusus menggunakan Lanjutan → Stickman Studio; permintaan gaya itu tidak diganti dengan motion graphics biasa secara senyap.
- Petikan bukti diperiksa secara tepat selepas normalisasi aksara/ruang. Semakan petikan bukan jaminan bahawa setiap parafrasa model tepat; pengguna masih perlu menyemak fakta dan menonton hasil sebelum berkongsi.

## Data, versioning dan pemulihan

Satu versi diperuntukkan: v0.0.0.8, task `simple-video-workflow-20261112`. Branch `feat/v41-simple-workflow`; checkpoint `checkpoint/simple-video-workflow-20261112` menunjuk source v7 yang telah diuji, `bca7bfa61330b4a258b8dcf44fd7a7deb004515f`. v1–v7 serta tag dan artifak lama dikekalkan. Tiada reset, force push, merge main atau Stable Release automatik.

SQLite schema 4→5 menambah keadaan workflow. Snapshot database dibuat sebelum ALTER; draf, mesej, media dan data Stickman dipelihara. Backup projek merangkumi SQLite, media dan renders. Sesi/key agent berada dalam data aplikasi, di luar backup projek dan Git. Selepas pindah mesin, sambungkan akaun/key pada mesin itu.

EXE lama tidak boleh membuka schema yang lebih baharu. Untuk rollback, gunakan checkpoint source dan salinan backup/snapshot yang sepadan melalui pemulihan sedia ada; jangan tukar database aktif dengan salinan lama secara terus. Job terputus ditandakan gagal, bahan/pelan kekal, dan tiada tugas dihantar semula automatik. Pembatalan menamatkan proses render milik tugas.

## Bukti ujian dan cara muat turun

Tempatan Linux: 80 unit tests PASS, typecheck/build PASS, Electron UI smoke PASS. Smoke menjalankan upload → permintaan login → kod peranti fixture → sambung automatik → render MP4 sebenar → playback → simpan → restart. Ujian proses Portable tempatan turut menghasilkan MP4 1080p30 dengan audio sintetik dan memeriksa full decode. Semua 19 skill kekal disahkan; ujian lama Stickman, worker, backup dan IPC turut dikekalkan.

Login OAuth akaun sebenar, inferens berbayar dan Gemini TTS sebenar: **NOT RUN** dalam ujian automatik ini, kerana tiada credential pengguna digunakan. Fixture tidak dilabel sebagai login/inferens sebenar.

Keputusan Windows mesti dirujuk pada run bagi source commit berkenaan dalam [GitHub Actions](https://github.com/shazwannoor95-jpg/visionforce3/actions?query=branch%3Afeat%2Fv41-simple-workflow), serta branch laporan `ci/windows-evidence-v0.0.0.8`. Workflow tidak melangkau penerimaan: unit, typecheck, build NSIS/Portable, native development/packaged/installed UI, install/uninstall dua jenis laluan, Portable sebenar, Remotion MP4 dan checksum. Status Linux tidak dianggap Windows PASS.

Artifacts dipisahkan untuk muat turun mudah: `VISIONFORGE3-<run>-<attempt>-Portable`, `…-Installer` dan `…-Proof`. Pilih run yang semua langkah penerimaannya PASS. EXE bernama `VISIONFORGE-3-v0.0.0.8-Portable-x64.exe` atau `…-Setup-x64.exe`; keluarkan EXE daripada ZIP sebelum dibuka. Proof mengandungi screenshot, MP4, laporan unit/FFprobe dan checksum. Artifacts disimpan 30 hari. Binaan kekal DRAFT/UNSIGNED sehingga penerbitan diluluskan.
