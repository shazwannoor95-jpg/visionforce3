# Pemasangan Skill Argon

Sumber: 63 bahagian RAR dimuat naik pengguna. Semua bahagian berjaya dipindahkan dan arkib dibaca tanpa ralat libarchive. Arkib mengandungi 2730 entri, 2,104,048,925 bait selepas ekstrak.

## Dipasang dalam skop projek Codex

- `.agents/skills/buat-video-motion-grafik`: SKILL.md, scripts, references, assets dan agents daripada Presets. Komponen archive runtime dalam Komponen tidak dipasang.
- `.agents/skills/buat-video-motion-grafik-gemini`: keluaran semasa 10 November 2026 daripada pek core dan pek yang lulus SHA-256/ZIP CRC, termasuk Atlas terkunci. Versi Gemini lama tidak diaktifkan serentak kerana nama skill sama.

16 skill terdahulu tidak diubah. Jumlah kini 18 nama skill unik.

## Semakan dan batas

9 daripada 11 pek Gemini lulus SHA-256 manifest. Pek `fonts` dan `vlog_payload_03` GAGAL padanan SHA-256 dan tidak diekstrak/dipasang daripada pek tersebut. Jangan anggap koleksi Gemini lengkap; bekalkan semula pek yang sepadan atau manifest keluaran yang sah sebelum menggunakannya. Aset yang sudah wujud dalam sumber Presets dikekalkan berasingan; bukan pengganti pengesahan pek Gemini yang gagal.

Semua skrip Python yang disalin lulus parse AST; SKILL.md hadir dengan nama/deskripsi. Ini pengesahan pemasangan fail, bukan bukti inferens suara, render Atlas atau HyperFrames sudah diuji. Tiada skrip daripada arkib dijalankan. Tiada arahan dalam dokumen yang dijadikan autorisasi untuk menulis ke Drive atau servis luar.

Model MeloTTS/MS/Malay BERT dan wheelhouse dependency kekal dalam bahan arkib di luar repo; tidak dipasang atau dicommit. Runtime/VO, HyperFrames dan semua preset belum diuji. Pemasangan fail skill tidak bermaksud semua fungsi READY. Arahan khusus Gemini dan path lama perlu disesuaikan apabila digunakan dalam Codex Cloud.

Arkib asal, model, dependency bundles, cache dan versi lama tidak dimasukkan GitHub. Bukti pek: `argon-install.json`. Fail repo boleh dipulihkan melalui Git; persistence snapshot Cloud masih belum disahkan.
