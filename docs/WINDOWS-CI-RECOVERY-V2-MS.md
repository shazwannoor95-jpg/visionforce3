# Windows CI Recovery — v0.0.0.2

## Keputusan penerimaan sebenar

Run lengkap pertama yang lulus: https://github.com/shazwannoor95-jpg/visionforce3/actions/runs/43037741035

Source SHA: `0e0e625ec6c5918986415cea258121078f45f7b2`. Platform runner: Windows (`win32`, windows-2025). Ini bukan cross-build Linux. Bukti per-run terkini juga disimpan secara append-only pada branch `ci/windows-evidence-v0.0.0.2` kerana API GitHub dalam Cloud menerima 403.

| Pemeriksaan | Keputusan |
|---|---|
| 18 SKILL.md, termasuk kedua-dua custom | PASS |
| Unit test: 39, skipped 0 | PASS |
| Typecheck | PASS |
| Electron Windows build | PASS |
| NSIS Installer | PASS |
| Portable EXE | PASS |
| Native development dan packaged smoke | PASS |
| Silent install dan app pada VFPlain | PASS |
| Silent install dan app pada VF With Spaces | PASS |
| Silent uninstall kedua-dua laluan | PASS |
| Data pengguna dikekalkan selepas uninstall | PASS |
| Portable process, UI, SQLite, backup, IPC bootstrap | PASS |
| Remotion MP4 H.264 1920×1080, 30fps, 120 frame | PASS |
| FFprobe dan full decode FFmpeg -xerror | PASS |
| SHA-256 kedua-dua EXE | PASS |

Artifak run: `VISIONFORGE3-43037741035-1` (sekitar 185 MB), pada bahagian Artifacts halaman run. Log masuk GitHub untuk muat turun. Mengandungi `VISIONFORGE-3-v0.0.0.2-Setup-x64.exe`, `VISIONFORGE-3-v0.0.0.2-Portable-x64.exe`, log, video Windows dan SHA256SUMS. Kedua-duanya `NotSigned`/UNSIGNED berdasarkan Get-AuthenticodeSignature; tiada dakwaan sijil signing tersedia.

## Punca tepat dan pembetulan

1. **CRLF**: Windows checkout mempunyai `core.autocrlf=true`. Semua 18 header sebenar bermula `2d2d2d0d0a`; parser lama mensyaratkan `---\n`, maka semuanya ditolak. UTF-8 BOM turut tidak ditangani. Parser baharu mendekod UTF-8 secara fatal, menerima BOM dan menormalkan newline hanya untuk parsing, bukan untuk checksum. YAML core schema, unique keys dan alias limit digunakan; mapping, description dan ID direktori tetap wajib. Metadata dalam body tidak boleh memalsukan header. Fail skill asal tidak diubah.
2. **CI exit code tersembunyi**: `npm test` diikuti typecheck dalam satu blok PowerShell boleh mengembalikan exit code arahan akhir. Kini kedua-duanya langkah berasingan; wrapper merekod log dan memulangkan exit code child yang sebenar. Tiada continue-on-error/skipped assertion digunakan untuk acceptance.
3. **Installed-app IPC**: diagnostic native menunjukkan Node URL `RUNNER%7E1` tetapi Chromium `RUNNER~1` untuk dokumen sama. Perbandingan URL mentah menolak bootstrap/createProject selepas install. Matcher kini membandingkan decoded normalized file paths. WebContents, main frame, file protocol dan path yang tepat masih wajib; iframe, origin luar, query dan fail lain ditolak serta diuji.
4. **NSIS laluan beruang**: nilai `/D` tanpa quote dipecah oleh StdUtils.GetParameter dalam template electron-builder. Quote nilai directory memulihkan install ke destinasi diminta. Ujian app dan uninstall dijalankan pada kedua-dua folder; sentinel membuktikan data pengguna tidak dipadam.
5. **QA decode, bukan render**: MP4 berjaya dirender, tetapi FFmpeg Remotion dibina tanpa encoder `wrapped_avframe` yang dipilih secara lalai oleh null output. Encoder `rawvideo` yang tersedia dipilih secara eksplisit, masih menyahkod seluruh video dengan `-xerror` dan gagal jika decoder memberi ralat. Ujian tidak dibuang.

## Perlindungan versi dan backup

Versi 2 diperuntukkan ledger remote, bukan digunakan semula. Baseline ialah merge main `859139c`; checkpoint `checkpoint/windows-ci-recovery-20261111`. v0.0.0.1, tag dan evidence lama dikekalkan. Main dan visionforce2 tidak diubah oleh tugasan ini; tiada reset, force push atau merge automatik.

Source/lockfile/YAML dependency dipin, manifest dan evidence ada dalam Git. Rekod TESTED disimpan dalam releases; status penerbitan kekal DRAFT, bukan STABLE. Artifak Actions disimpan 30 hari untuk build pembangunan. Stable Release/GitHub Releases tidak diterbitkan tanpa kelulusan. Backup model/runtime Cloud tidak dianggap tersedia secara automatik di Windows.

Rollback sumber kekal melalui clone/checkpoint berasingan, bukan reset. Pemulihan projek masih membuat backup, menyemak schema/checksum, meminta approval dan menulis salinan baharu. Pemasangan Windows dan fungsi asas telah diuji; ini tidak mendakwa semua fungsi 18 skills, AI provider, browser TTS atau renderer tambahan telah siap.

## Evidence

`releases/v0.0.0.2/evidence/`: skill diagnostic Windows, 39 ujian, log acceptance, Portable proof, FFprobe, decoder proof, checksums dan source provenance. Branch bukti CI mengandungi semua run gagal dan lulus; laporan tidak menukar kegagalan lama menjadi PASS. GitHub Actions selepas commit dokumentasi boleh menghasilkan run tambahan; semak source SHA/run ID pada setiap artifact.
