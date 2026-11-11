# Jalankan VISIONFORGE 3 v0.0.0.1

Gunakan checkout sedia ada. Tiada worktree tambahan diperlukan. `video/`, `modules/browser/` serta model/runtime Argon terdahulu dikekalkan. Folder desktop ialah aplikasi berasingan, tidak menggantikan engine sedia ada.

## Desktop

Node 24.22.1 digunakan untuk build. `npm --prefix desktop ci` (hanya apabila dependency belum tersedia), kemudian `npm --prefix desktop run build` dan `npm --prefix desktop start`. Electron sebenar diperlukan; membuka Vite dalam browser biasa tidak memberikan bridge native.

Projek Windows disimpan dalam `D:\VISIONFORGE3` jika drive boleh ditulis; jika tidak, direktori data pengguna `VISIONFORGE3/workspace`. Profil berasingan daripada VISIONFORGE 2. SQLite schema 1→2→3 dijejak; sebelum migrasi data lama, snapshot dibuat dalam migration-backups. Draft/chat autosave, file picker, eksport manifest dan backup media tersedia. Drag-and-drop native belum disambungkan; gunakan Lampirkan fail.

Menu Skills membaca 18 SKILL.md asal yang dibundel bersama references/scripts dan runtime-lock terpilih. Model, wheelhouse dan aset besar Linux tidak dipaketkan secara membuta tuli. Registry VERIFIED ialah audit fail, bukan semua fungsi tersedia pada Windows.

## PDF ke MP4

Untuk worker pembangunan sedia ada: `python3 -m core.server --port 8787 --storage .data/jobs`. Dependency PDF worker ada di core/requirements.txt; Remotion menggunakan lockfile video/. Ini bukan server produksi awam. Dalam aplikasi Settings, tetapkan `http://127.0.0.1:8787` hanya apabila worker berada pada komputer sama; worker di mesin lain memerlukan hosting dan HTTPS yang sesuai. Loopback Codex Cloud tidak boleh terus dicapai oleh Windows PC.

Cipta projek → Lampirkan PDF berteks → Hantar brief → Jana video daripada PDF → luluskan dialog penghantaran → tunggu status sebenar → preview MP4. Planner menggunakan petikan tepat dokumen dan peraturan routing, bukan LLM. Had core 20 MiB/50 halaman, 8 petikan, 180 aksara per petikan, 3 saat per scene; baki teks ada dalam coverage.json. Ini bukan sokongan automatik video 5–8 minit atau Keep All penuh. DOCX/PPTX/media boleh disimpan tetapi belum diekstrak oleh worker core.

API key OpenAI/Anthropic disimpan dengan safeStorage OS apabila penyulitan selamat tersedia; backend basic_text ditolak. Butang Uji akses baca API hanya memeriksa authorization model-list. Tiada inferens berbayar dibuat. Login/langganan ChatGPT/Claude tidak dianggap API access. Google AI Studio TTS dan browser video belum disambungkan; import audio manual tersedia, tetapi sync/mastering automatik desktop belum lengkap.

## Backup dan restore

Settings → Backup sekarang menyimpan SQLite dan media beserta SHA-256. Semak pelan sebelum Pulihkan salinan; aplikasi meminta kelulusan native, mencipta backup keselamatan dan memulihkan ke direktori baharu. Data aktif tidak ditimpa. Ini bukan pertukaran automatik ke aplikasi versi lama.

Sumber: `python3 tools/versioning/manager.py compare <ref-lama>`, kemudian `restore-source <ref> <folder-baharu> --approve`. Destinasi sedia ada ditolak; tiada reset. Jangan membuang ledger/tag reservation atau mengubah tag release lama.

## Ujian

- `npm --prefix desktop test` — storan, restore, schema, key safety, skill/router, versi, endpoint.
- `npm --prefix desktop run build` — typecheck + React build + audit sumber.
- `npm --prefix desktop run smoke` — Electron UI native (perlukan paparan; Windows native atau X display Linux).
- `node desktop/tests/pipeline-smoke.cjs` — Electron + worker Python + PDF + Remotion + inline preview; Linux test profile, dialog pemilihan/approval diautomasi.
- `python3 -m unittest discover -s tests -v` — termasuk allocator serentak dan source recovery.

## Windows build

`npm --prefix desktop run pack:win` menghasilkan direktori build unik di desktop/release/v0.0.0.1/<UUID>/; percubaan terdahulu tidak ditimpa. `latest-build.json` hanyalah penunjuk, bukan artifak immutable. Installer/Portable bernama VISIONFORGE-3-v0.0.0.1-Setup-x64.exe dan VISIONFORGE-3-v0.0.0.1-Portable-x64.exe apabila berjaya.

Build Windows dalam Linux memerlukan Wine yang berfungsi; percubaan host dan container Wine di sesi ini FAILED pada rcedit. Tiada installer/portable disahkan siap. Workflow windows-desktop.yml disediakan untuk Windows runner sebenar dan bukti packaged UI, NSIS laluan dengan/tanpa ruang, uninstall, portable, Remotion MP4 serta checksum. Jalankan/semak GitHub Actions pada branch feat/v41-desktop-versioning. Ketersediaan run dan keputusannya belum dapat disahkan dari sesi ini (API 403; halaman Actions setup/generic).

UNSIGNED jika tiada sijil. Jangan anggap Windows 10 disokong penuh sebelum ujian; sasaran utama Windows 11 x64. Stable Release tidak diterbitkan. Workflow publish-approved-release.yml hanya manual, memerlukan evidence lengkap, source SHA, checksum dan input kelulusan serta environment stable-release. Sediakan required reviewer bagi environment itu sebelum penggunaan produksi. Artifak CI pembangunan tamat tempoh; release stabil diluluskan akan disimpan dalam GitHub Releases, bukan bergantung artifact CI sahaja.
