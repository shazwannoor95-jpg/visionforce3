# Sejarah perubahan VISIONFORGE 3

## v0.0.0.1 — DRAFT

- Memulakan ledger versi remote atomik dan immutable reservation tags; checkpoint source sebelum kerja.
- Menambah Electron + React, projek SQLite, autosave, backup data dan pemulihan tidak destruktif.
- Audit dan registry UI bagi 18 skill; router tempatan dan API key OS-safe storage.
- Adapter worker sebenar: PDF → Remotion → MP4/SRT/manifest/coverage → preview dan eksport dalam aplikasi.
- Ujian Linux lulus. Windows cross-build gagal pada Wine/rcedit; installer/portable/native CI belum disahkan. Tiada Stable Release diterbitkan.

Kerja sebelum ledger versi ini kekal dalam sejarah Git sedia ada; tidak diberi nombor rekaan secara retrospektif.

## v0.0.0.2 — DRAFT

Pulihkan CI Windows, audit frontmatter dan build EXE

Pembetulan v0.0.0.2: safe frontmatter UTF-8/BOM/LF/CRLF dan diagnostic 18 IDs; fail-fast unit/typecheck; IPC Windows percent-encoding; quoting NSIS directory; portable IPC dan data retention; decoder QA menggunakan rawvideo yang disokong. Windows Installer/Portable serta MP4 lulus penerimaan native pada run 43037741035. Release belum diterbitkan sebagai STABLE.

## v0.0.0.3 — DRAFT

Tambah kawalan sesi browser dan login manual AI Studio
