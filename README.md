# visionforce3

## VISIONFORGE 3 — asas V3.5

Worker CPU boleh menerima PDF melalui API tempatan, menyimpan job dalam SQLite, merender motion graphics Remotion dan menghasilkan MP4/SRT/manifest/laporan Source Lock. Planner semasa memetik dokumen secara deterministik; chat UI dan integrasi LLM/browser provider belum dibina.

- [Jalankan dan uji](docs/V35-RUN-MS.md)
- [Laporan Fasa 0/1 dan acceptance](docs/V35-PHASE-0-1-MS.md)
- [Registry sumber](docs/v35-repositories.json)
- [Registry skill](docs/v35-skills.json)

Ujian: `python3 -m unittest discover -s tests -v`, `npm --prefix video run typecheck`, `python3 -m tests.smoke_pipeline`.

Jalankan API pembangunan: `python3 -m core.server`. Bind loopback sahaja; bukan deployment produksi. Model GPU pilihan tidak dipasang automatik.
