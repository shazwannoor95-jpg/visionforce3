# Laporan V4.1 — VISIONFORGE 3 v0.0.0.1

## Keadaan repo dan versi

Baseline `025cb38` pada feat/v35-core-worker. Working tree bersih sebelum kerja. Branch baharu feat/v41-desktop-versioning, checkpoint/v35-before-v41-20261111, ledger vf-version-ledger dan tag vf-reservation-1 menyimpan checkpoint/peruntukan nombor. main dan visionforce2 tidak diubah.

Allocator menggunakan push atomik fast-forward ledger + tag reservation. Konflik dua branch akan ditolak oleh Git dan dicuba semula dengan ledger terkini; tiada force push. Nombor gagal tidak dikurangkan/dipadam. Satu task ID mengembalikan nombor sama untuk semua commit prompt itu. Ujian tempatan dengan remote bare dan 4 job serentak menghasilkan 4 nombor berbeza. Rekod status ialah append-only events; FAILED tidak boleh diluluskan STABLE. Windows FileVersion dan SemVer dipetakan daripada counter (rollover komponen selepas 65535), tanpa mengubah label pengguna v0.0.0.N.

## Fungsi yang benar-benar tersedia

- Electron + React + TypeScript + Vite; chat, projek SQLite, file picker, draft/chat autosave, reopen selepas restart, pustaka media dan eksport manifest.
- Backup projek berchecksum, approval dialog, schema checks dan restore ke salinan baharu. Source checkpoint/compare/restore melalui VersionManager.
- UI Settings → Version History dan About memaparkan versi DRAFT dan source commit. Tiada stable artifact/history download direka kerana release belum wujud.
- 18 skill asal disemak ID/hash/references/scripts/assets; manifest lama dikemas kini. Satu pautan dalam playwright-cli ialah contoh path output trace, bukan dependency hilang. Kedua-dua katalog custom 842/922 diasingkan. Runtime Windows semua 18 belum disahkan; audit lesen per-aset masih diperlukan.
- Router tempatan memilih subset berdasarkan brief. Tidak memasang semua runtime; hasil routing PLANNED, bukan semua READY.
- API keys melalui penyulitan OS, simpanan plaintext ditolak, sambungan model-list rasmi pilihan; tiada panggilan inferens atau bayaran tanpa persetujuan.
- Adapter Cloud sebenar: upload PDF selepas kelulusan native, polling queue, download hasil dan inline MP4 preview. Ujian Linux menghasilkan MP4 sebenar 1920×1080/30fps/6 saat daripada fixture PDF. Planner deterministik, bukan LLM.

## Ujian dan batas penerimaan

| Pemeriksaan | Status |
|---|---|
| Allocator berturutan/idempotent/serentak, tag immutable, source clone recovery | PASS |
| Failed→Stable guard dan rekod lama immutable | PASS |
| Projek restart, backup checksum, restore approval, migrasi dan downgrade guard | PASS |
| 18 instruction registry, router namespace, endpoint security, OS key guard | PASS |
| Typecheck + React build | PASS |
| Electron UI sebenar pada Linux | PASS |
| Electron upload PDF→worker→MP4→inline preview Linux | PASS |
| Remotion/FFmpeg smoke sedia ada | PASS |
| Windows cross-build host/container | FAIL — Wine/rcedit |
| Native Windows installer, portable, install/uninstall dan video | NOT RUN / bukti CI belum disahkan |
| Muat turun Stable Release terdahulu | NOT AVAILABLE — belum ada release diluluskan |
| Google AI Studio TTS / browser video / paid LLM / GPU | NOT RUN / tidak dikonfigurasi |

Oleh itu versi kekal DRAFT; WINDOWS EXE NOT READY. Tiada dakwaan keseluruhan V4.1 siap atau semua 18 runtime berfungsi. Foundation dan MVP core tersedia tetapi AI Director sebenar, desktop native local renderer yang dipaketkan, drag/drop native, per-scene regeneration, subtitle/audio alignment, Keep All dokumen panjang, editor, auto-update stable dan cloud produksi ialah kerja seterusnya. Tiada mock render ditukar menjadi PASS.

## Penyerahan dan backup

Source, checkpoint dan ledger dipush ke GitHub pada branch semakan; tiada merge automatik. Stable release/tag tidak diterbitkan. Artifak Windows gagal kekal dalam folder percubaan UUID untuk diagnosis; log ringkas dalam releases/v0.0.0.1/build-attempts.json. Bukti Linux dan rekod status dalam releases/v0.0.0.1/. Model/runtime besar kekal di workspace; snapshot Codex Cloud dan pemulihan pada mesin baharu belum dibuktikan.

Dua halangan luaran utama: native Windows runner/bukti CI belum tersedia untuk disahkan, dan API GitHub menerima 403 dalam Cloud. Halaman Actions yang dapat dibaca masih menunjukkan halaman setup/generic, jadi tiada run dianggap lulus. Semak/aktifkan Actions dan jalankan workflow Windows; jangan label stable sehingga bukti tersedia. PR creation juga tertakluk akses API; keterangan PR dan pautan branch disediakan berasingan.
