# VISIONFORGE 3 — AUTOMATIC VERSIONING, BACKUP & ROLLBACK SYSTEM

OpenAI Codex, tambahkan sistem versi automatik kepada keseluruhan projek VISIONFORGE 3.

Keperluan utama saya ialah setiap kali saya memberikan prompt yang menghasilkan perubahan kod, pembetulan bug, penambahan fungsi atau penambahbaikan aplikasi, perubahan tersebut mempunyai nombor versi baharu.

**FORMAT VERSI WAJIB:**

- VISIONFORGE 3 v0.0.0.1
- VISIONFORGE 3 v0.0.0.2
- VISIONFORGE 3 v0.0.0.3
- VISIONFORGE 3 v0.0.0.4
- Dan seterusnya secara automatik.

## 1. AUTOMATIC VERSION INCREMENT

1. Setiap tugasan prompt yang mengubah kod mesti mendapat nombor build unik.
2. Nombor versi meningkat secara automatik.
3. Jangan reset nombor apabila membuka sesi Codex baharu.
4. Jangan menggunakan nombor versi yang pernah digunakan.
5. Jika satu prompt menghasilkan beberapa commit, kumpulkan semuanya di bawah satu versi tugasan.
6. Prompt yang sekadar bertanya atau menganalisis tanpa mengubah kod tidak perlu meningkatkan versi.
7. Jika build gagal, rekod versi tersebut sebagai FAILED/DRAFT dan simpan snapshot perubahan untuk debugging. Jangan terbitkannya sebagai Stable Release.
8. Versi baharu berikutnya tidak boleh menggunakan semula nombor versi gagal.
9. Pastikan penjanaan nombor versi selamat daripada konflik antara branch atau build serentak.
10. Gunakan sumber nombor versi yang konsisten dan boleh disahkan melalui Git/CI.

## 2. PRESERVE PREVIOUS VERSIONS

Sebelum mengubah kod:

- Sahkan git status dan branch.
- Pastikan perubahan belum disimpan tidak hilang.
- Cipta checkpoint yang boleh dipulihkan.
- Gunakan branch atau commit baharu yang sesuai.
- Jangan menggunakan force push atau menulis semula tag release lama.
- Jangan overwrite artifak versi lama.

Untuk setiap versi yang lulus pengesahan, simpan:

- Git commit SHA.
- Immutable Git version tag.
- Release notes.
- Dependency lockfiles.
- Skill manifest.
- Windows Installer.
- Portable EXE.
- SHA-256 checksums.
- Ujian dan status CI.

Jangan mengubah kandungan release yang sudah diterbitkan.

## 3. WINDOWS VERSIONING

Gunakan label versi pengguna empat komponen seperti `v0.0.0.7`.

Pastikan keserasian:
- package.json menggunakan SemVer sah.
- Windows FileVersion menggunakan empat komponen.
- Electron Builder menggunakan konfigurasi versi yang sesuai.
- Nama installer menggunakan nombor versi paparan.

Contoh output:

`VISIONFORGE-3-v0.0.0.7-Setup-x64.exe`

`VISIONFORGE-3-v0.0.0.7-Portable-x64.exe`

Setiap fail release perlu unik dan tidak menimpa fail versi sebelumnya.

Pastikan versi baharu dikenali dengan betul oleh mekanisme naik taraf installer.

## 4. AUTOMATIC BACKUP

Setiap versi mempunyai checkpoint sumber kod melalui Git.

Untuk release stabil, simpan juga artifak Windows secara berasingan.

Jangan bergantung hanya pada GitHub Actions Artifacts yang boleh tamat tempoh.

Gunakan GitHub Releases untuk menyimpan installer, portable, checksum dan release notes bagi versi yang diluluskan untuk diterbitkan.

Semasa pembangunan tanpa kebenaran push, simpan checkpoint dalam Git tempatan terlebih dahulu. Jangan mendakwa backup GitHub tersedia jika belum dipush.

Sediakan sistem backup projek pengguna yang berasingan daripada backup source code.

## 5. ROLLBACK & RECOVERY

Cipta `VersionManager` dan `RecoveryManager`.

Keupayaan:

- View Version History.
- Compare Versions.
- Show Changes.
- Download Previous Release.
- Restore Source Checkpoint.
- Restore Previous Stable Version.
- Backup Project Data.
- Recover After Failed Update.

Jangan membuat rollback destruktif secara automatik.

Sebelum rollback aplikasi:
1. Backup data projek pengguna.
2. Semak keserasian database dan format projek.
3. Paparkan perubahan yang akan berlaku.
4. Dapatkan kelulusan pengguna.
5. Pulihkan versi pilihan tanpa memadam sejarah release lain.

Gunakan database migrations yang boleh dijejak dan lindungi data daripada downgrade tidak serasi.

## 6. VERSION HISTORY DALAM UI

Tambahkan halaman:

**Settings → Version History**

Paparkan:
- Version Number.
- Release Date.
- Changes.
- Commit SHA.
- CI Status.
- Release Status.
- Backup Status.
- Download.
- Restore.

Status yang dibenarkan:
- DRAFT.
- BUILDING.
- FAILED.
- TESTED.
- STABLE.
- ARCHIVED.

Dalam About:

`VISIONFORGE 3 — v0.0.0.X`

## 7. PERATURAN CODEX BAGI SETIAP PROMPT SETERUSNYA

Pada permulaan tugasan yang mengubah kod:
- Baca versi terakhir.
- Sahkan checkpoint.
- Tetapkan versi tugasan baharu yang unik.

Selepas perubahan:
- Jalankan ujian.
- Rekod fail yang diubah.
- Rekod keputusan build.
- Simpan commit/checkpoint.
- Kemas kini changelog.
- Label DRAFT atau FAILED jika belum lulus.
- Label STABLE hanya selepas ujian penerimaan yang ditetapkan lulus.

Sediakan ringkasan dalam Bahasa Melayu:

VERSI: v0.0.0.X

PERUBAHAN: ...

UJIAN: PASS / FAIL / NOT RUN

BACKUP: LOCAL / GITHUB / NOT AVAILABLE

WINDOWS EXE: READY / NOT READY

ROLLBACK: AVAILABLE / NOT AVAILABLE

Jika push atau penerbitan GitHub Release diperlukan, patuhi peraturan kelulusan Git yang telah saya tetapkan.

## 8. UJIAN PENERIMAAN

Buktikan:
1. Dua perubahan kod berturutan menghasilkan dua nombor versi berlainan.
2. Versi terdahulu tidak berubah.
3. Versi yang gagal tidak dilabel STABLE.
4. Build Windows menggunakan nama versi yang betul.
5. Git tag/commit boleh digunakan untuk mendapatkan semula source lama.
6. Artifak release yang disimpan boleh dimuat turun.
7. Restore tidak memadam projek pengguna.
8. Dua job serentak tidak menghasilkan nombor versi sama.

Implementasikan sistem ini sebagai komponen asas VISIONFORGE 3 sebelum pembangunan fasa baharu diteruskan.

Jangan reset kerja yang telah dibuat. Semua komunikasi dalam Bahasa Melayu.