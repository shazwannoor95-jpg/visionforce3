# VISIONFORGE 3 — arahan pembangunan

- Kekalkan semua skill dan kerja sedia ada. Jangan ubah visionforce2.
- Pada prompt yang mengubah kod: semak git status/branch/HEAD dan version.json. Checkpoint perubahan pengguna sebelum mengubahnya; jangan auto-stage rahsia atau reset.
- Peruntukkan SATU nombor tugasan melalui `python3 tools/versioning/manager.py reserve --task <id-unik> --title <tajuk> --output <fail-baharu>` menggunakan ledger Git remote yang dikongsi. Semua commit prompt sama guna nombor sama. Jangan buat nombor sendiri pada branch lain. Tanpa akses ledger, kerja versi baharu BLOCKED; jangan guna semula nombor terakhir.
- Hanya prompt analisis/read-only tidak menaikkan versi. Kegagalan kekal DRAFT/FAILED dan nombor tidak diguna semula. Tag lama/artefak lama tidak ditimpa; tiada force push.
- package.json SemVer dan Windows FileVersion datang daripada version.json melalui skrip sync. Paparan pengguna `v0.0.0.N`.
- STABLE memerlukan bukti penerimaan Windows dan kelulusan penerbitan. Jangan anggap cross-build Linux ialah Windows smoke PASS.
- Branch pembangunan khusus, jangan merge main automatik. Pengguna telah membenarkan push kerja projek ke GitHub; kekalkan branch review kecuali diminta sebaliknya. Jangan terbit stable release tanpa arahan.
- Jalankan ujian berkaitan, rekod status dan checkpoint. Backup data projek berasingan daripada Git. Restore mesti buat backup dahulu, semak schema dan minta kelulusan di UI; jangan rollback destruktif automatik.
- Bahasa Melayu untuk UI/laporan. Jangan simpan token/kata laluan/cookie atau model besar dalam repo.
