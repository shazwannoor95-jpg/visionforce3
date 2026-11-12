# VISIONFORGE 3

Aplikasi Windows untuk menghasilkan video penerangan daripada dokumen dan imej. Kerja semasa: **v0.0.0.8 DRAFT**, branch `feat/v41-simple-workflow`. Versi STABLE belum diterbitkan.

1. Buka aplikasi, kemudian **Pilih fail untuk video**. Projek disimpan secara automatik.
2. Tulis arahan, contohnya: `Buat video penerangan 30 saat Bahasa Melayu berdasarkan bahan ini. Format 16:9, gaya motion graphics yang kemas.`
3. Tekan **Jana video**. Jika perlu, login rasmi Codex dengan akaun ChatGPT, atau sambungkan API OpenAI, Claude atau Gemini. Bahan dan prompt dikekalkan semasa menyambung.
4. Tunggu video siap, tonton dan semak, kemudian **Simpan video**.

Narasi ialah pilihan tambahan menggunakan Gemini API; laluan lalai menghasilkan video teks bergerak tanpa narasi. Tetapan teknikal dan aliran lama tersedia melalui **Lanjutan**.

- [Panduan, sambungan agent dan batas sebenar v8](docs/SIMPLE-WORKFLOW-V8-MS.md)
- [Windows Actions: build, ujian native dan muat turun EXE](https://github.com/shazwannoor95-jpg/visionforce3/actions/workflows/windows-desktop.yml)
- [Stickman Studio v7](docs/STICKMAN-STUDIO-V7-MS.md)

Desktop: `npm --prefix desktop ci`, `npm --prefix desktop run build`, `npm --prefix desktop test`, `npm --prefix desktop run smoke`. Smoke memerlukan desktop/display. Semua 19 skills dikekalkan. Semak bukti run bagi commit yang hendak dimuat turun; build sahaja tidak bermaksud penerimaan Windows lulus.

Bahagian di bawah ialah laporan sejarah bagi versi terdahulu.

## VISIONFORGE 3 — asas V3.5

Worker CPU boleh menerima PDF melalui API tempatan, menyimpan job dalam SQLite, merender motion graphics Remotion dan menghasilkan MP4/SRT/manifest/laporan Source Lock. Planner semasa memetik dokumen secara deterministik; chat UI dan integrasi LLM/browser provider belum dibina.

- [Jalankan dan uji](docs/V35-RUN-MS.md)
- [Laporan Fasa 0/1 dan acceptance](docs/V35-PHASE-0-1-MS.md)
- [Registry sumber](docs/v35-repositories.json)
- [Registry skill](docs/v35-skills.json)

Ujian: `python3 -m unittest discover -s tests -v`, `npm --prefix video run typecheck`, `python3 -m tests.smoke_pipeline`.

Jalankan API pembangunan: `python3 -m core.server`. Bind loopback sahaja; bukan deployment produksi. Model GPU pilihan tidak dipasang automatik.

## V4.1 — Windows Desktop & Versioning (DRAFT)

Asas aplikasi Electron, pengurusan projek, 18-skill registry, backup/restore dan adapter Cloud PDF-ke-MP4 berada pada branch feat/v41-desktop-versioning. Ujian Electron/pipeline Linux lulus. Installer dan Portable Windows belum berjaya dibina/disahkan; lihat status sebenar sebelum menggunakan build sebagai release.

- [Setup desktop dan worker](docs/V41-SETUP-MS.md)
- [Laporan v0.0.0.1](docs/V41-STATUS-MS.md)
- [Keperluan V4.1](docs/MASTER-V41-MS.md)
- [Versioning/backup/rollback](docs/REQUIREMENTS-VERSIONING-MS.md)

## Windows CI Recovery — v0.0.0.2

Installer dan Portable UNSIGNED berjaya dibina dan diuji secara native Windows, termasuk install/uninstall dua jenis laluan, data retention, Portable IPC dan MP4 1080p30. Release belum diterbitkan sebagai STABLE.

[Laporan dan pautan muat turun EXE](docs/WINDOWS-CI-RECOVERY-V2-MS.md) · [Windows run lengkap pertama PASS](https://github.com/shazwannoor95-jpg/visionforce3/actions/runs/43037741035)
