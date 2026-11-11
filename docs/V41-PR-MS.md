# v0.0.0.1 — Asas Windows Studio, versioning dan backup/rollback (DRAFT)

Menambah allocator versi berturutan melalui Git ledger atomik serta reservation tags, checkpoint sumber, rekod status append-only dan perlindungan Stable Release. Semua commit tugasan ini menggunakan versi sama. Source/projek lama tidak direset.

Desktop Electron + React kini mempunyai chat/brief, projek SQLite dengan migrasi dan autosave, 18-skill registry, rule-based router, native file picker, encrypted API key storage dan read-only provider test. Backup projek berchecksum dipulihkan kepada salinan baharu selepas approval; source recovery juga tidak mereset working tree.

Adapter worker core membuktikan PDF → queue → Remotion → MP4 → download → inline preview dan export MP4/SRT/coverage/manifest dalam Electron sebenar di Linux. Planner masih deterministik, tiada paid LLM atau Google AI Studio dipalsukan.

Validasi: 9 ujian Node desktop, 11 ujian Python termasuk 4-way concurrent allocator, TypeScript/build, Electron Linux lifecycle dan pipeline PDF sebenar lulus. Native dialog selection/approval diautomasi untuk smoke; render tidak dimock. MP4 1920×1080/30fps/6 saat.

Windows cross-build gagal: Wine/rcedit tidak dapat dijalankan. Installer/portable dan native Windows acceptance belum disahkan. Workflow Windows dan workflow penerbitan manual diluluskan disediakan; CI API dalam sesi ini disekat 403. Versi kekal DRAFT, bukan STABLE. Tiada merge atau release automatik.

Bukti/status: docs/V41-STATUS-MS.md, docs/V41-SETUP-MS.md dan releases/v0.0.0.1/. Native Windows Actions/installer test ialah prerequisite sebelum EXE dianggap READY. Snapshot Cloud/model besar tidak dianggap persistent pada pemasangan Windows.
