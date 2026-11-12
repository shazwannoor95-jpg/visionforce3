# Stickman Studio dalam aplikasi — v0.0.0.7 DRAFT

Menu Stickman Studio kini dihubungkan kepada projek aktif, SQLite, skill directing-stickman-videos asal dan runtime B1 asal. Semua 19 skill dikekalkan. Fail upstream tidak diubah; adapter aplikasi berada dalam desktop/electron/stickman.cjs. Aplikasi membundel runtime, aset/font, Canvas/Sharp, FFmpeg dan FFprobe yang diperlukan. Dependency dikunci dalam desktop/package-lock.json, dengan fail dan notis pihak ketiga dibundel ke resources/third-party.

## Laluan pengguna

1. Cipta/buka projek. Lampirkan PDF berteks/TXT/MD, audio WAV/MP3, imej watak dan prop PNG/JPEG. Audio Gemini TTS atau import browser daripada aliran sedia ada juga boleh digunakan.
2. Buka Stickman Studio. Pilih gaya, nisbah dan durasi; baca teks sumber atau gunakan brief projek. PDF sehingga 40 halaman disokong, dengan maksimum 10000 aksara sumber; dokumen panjang tidak dipotong senyap. PDF imbasan memerlukan OCR atau teks pengguna.
3. Susun draf tempatan (susunan sumber, bukan inferens AI) atau jana cadangan Gemini selepas pengesahan penghantaran/kuota. Edit narasi/storyboard dan simpan.
4. Director A1–A6: semak/luluskan cadangan terkini, simpan pakej Director atau jana prompt akhir Gemini berasaskan kontrak gaya yang dibundel. Tema A1 mesti dipilih. Perubahan draf membatalkan kelulusan. Penjanaan klip AI/Flow tidak dilakukan oleh butang ini. Hasil Gemini masih memerlukan semakan; ia tidak automatik diisytiharkan patuh setiap syarat kreatif. Pakej Director tempatan ialah handoff cadangan/kontrak, bukan prompt siap universal.
5. B1: pilih audio narasi dan ambien yang sesuai/berlesen, atau nyatakan audio sedia ada ialah master campuran yang sudah diterima. Master tidak dilapis semula. Ambien mesti sekurang-kurangnya sepanjang narasi; tiada loop automatik. Gain ambien 0.06, SFX pilihan per babak 0.08. Jangan pilih narasi yang sama sebagai ambien.
6. Bina babak berturutan dengan masa mula/tamat, tajuk, sari kata tepat, imej watak, imej prop, sebab aksi dan arah prop. Pergerakan prop setempat ialah adapter asas; ia bukan rigging anggota penuh atau penjanaan imej automatik. Gunakan aset baharu yang sesuai dengan cerita, bukan contoh watak lama secara automatik. Selaraskan masa kepada audio sebenar; runtime tidak mempercepat narasi untuk memaksa durasi sasaran.
7. Render preview maksimum 20 saat. Tonton/dengar, luluskan preview terkini dan render video penuh. Audio, aset, manifest, laporan dan log disimpan dalam folder run unik. Hasil lama tidak ditimpa. MP4 dilampirkan kepada projek, boleh dimainkan dan dieksport bersama SRT/VTT, contact sheet dan log.

B2–B5 boleh dipilih untuk cadangan dan simpanan projek, tetapi render dalam aplikasi belum disambungkan untuk gaya itu. B4 memerlukan kontrak Brian/pembukaan/bunyi dan B5 mempunyai renderer presenter tersendiri. Tiada gaya diganti dengan B1 secara senyap. Ini integrasi modular, bukan dakwaan semua fungsi Autopilot sudah automatik.

## Keadaan dan pemulihan

Schema SQLite 3→4 menambah medan Stickman; backup migration dibuat sebelum ALTER pada projek sedia ada. Data sumber, draf dan mesej lama dipelihara. Backup projek sedia ada merangkumi database, media dan folder renders. Jangan buka database schema 4 menggunakan EXE lama; downgrade ditolak. Gunakan snapshot/backup yang sesuai melalui salinan pemulihan, bukan reset data aktif.

Job render berjalan dalam proses Node terasing menggunakan Electron RunAsNode dan binary setempat, tanpa shell atau perintah pengguna. Satu render tempatan pada satu masa. Output dan media yang boleh dipilih diturunkan daripada ID projek. Perubahan semasa render ditolak. Batalkan render menghentikan proses milik job; app quit turut menghentikannya. Job terputus ditandakan BLOCKED dan boleh dibuat preview baharu; tidak mengaku COMPLETE. Timeout proses 15 minit. Hasil projek dibatasi 50 MiB setiap lampiran oleh store sedia ada.

Kelulusan draf mengikat konfigurasi. Preview menggunakan salinan media, hash input dan fingerprint upstream; render penuh menyemak laporan/MP4 preview sebelum meneruskan. Render teknikal PASS bukan kelulusan seni atau pengesahan sumber/lesen audio. Pengguna perlu menonton, mendengar dan menyemak fakta.

## Pengesahan

Tempatan Linux: 62 unit tests PASS, typecheck/build PASS, Electron smoke PASS. Unit tests meliputi sumber PDF berteks sebenar, ID sumber, mod/timing tidak sah, persistensi, schema 3 dengan data asal dan snapshot, kelulusan/pembatalannya, tiada alias gaya dan job terputus.

Electron smoke melalui menu sebenar mengimport imej dan audio fixture sintetik, menyunting babak, membuat preview, memberi kelulusan automatik khusus fixture dan merender MP4 B1. FFprobe mengesahkan 1920×1080, 30fps, 60 frame, trek audio. Full decode upstream PASS; metadata mengandungi bukti perubahan piksel prop setempat. Restart mengekalkan hasil dan draf. Audio fixture ialah nada ujian/ambien sintetik, bukan narasi AI atau filem pelanggan yang telah diluluskan. Tiada panggilan penjanaan berbayar.

Pembetulan semasa QA: dependency FFprobe memerlukan postinstall permission executable pada Linux (install awal --ignore-scripts diperbaiki dengan postinstall rasmi). Loop ambien FFmpeg lama boleh tergantung; adapter menggunakan bed tanpa loop dan pengesahan panjang. Nama output upstream sebenar ialah film.mp4/film-report.json; adapter kini menggunakan nama itu. Fail sumber upstream kekal asal.

Windows: workflow feat/v41-stickman-studio menjalankan suite sama untuk development, packaged, installed path tanpa/dengan ruang, serta Portable/uninstall dan render Remotion. Keputusan native dirujuk pada Actions dan branch ci/windows-evidence-v0.0.0.7; jangan anggap bukti Linux sebagai Windows PASS. Bukti Stickman ada sebagai stickman-proof.json, stickman-b1-fixture.mp4 dan stickman-studio.png dalam artifact run.

Panggilan Gemini, akses akaun Google/Flow dan kesetiaan gaya untuk filem pelanggan belum disahkan oleh fixture. Masalah permission denied pada projek Google tidak diubah oleh integrasi ini. B1 tempatan boleh menggunakan audio/imej pengguna tanpa API.

Checkpoint sumber: checkpoint/stickman-app-integration-20261112 pada v0.0.0.6. Branch kerja feat/v41-stickman-studio. Tiada reset, force push, perubahan VISIONFORGE 2, merge main atau Stable Release automatik. Versi penerbitan kekal DRAFT/UNSIGNED.
