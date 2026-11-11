# CPython asal Argon: pemulihan selesai

Fail gantian `.part0001.gz` berukuran 8,000,000 bait sepadan SHA-256 manifest dependency asal. Ia ialah bahagian mentah, bukan arkib gzip lengkap; dipetakan kepada nama `.part0001` tanpa mengubah bait. Semua lima bahagian digabung dan hash arkib CPython lengkap lulus.

Bundle asal CPython 3.11.18, eSpeak dan wheelhouse dipasang secara offline ke `/workspace/argon-runtime/vo-original-cp31118`, berasingan daripada runtime 3.11.17 yang sudah berfungsi. `pip check`, import dependency dan suara Melayu eSpeak lulus. Konflik LD_LIBRARY_PATH lama ketika dpkg-deb diselesaikan dengan menjalankan installer menggunakan pustaka sistem; runtime suara menggunakan pustaka bundle sendiri selepas pemasangan.

Inferens Melayu MeloTTS-MS + Malay BERT tempatan/offline LULUS menggunakan CPython 3.11.18: WAV 44,100 Hz, 3.568 saat, peak 0.91415; sampel finite dan bukan senyap. Decode penuh FFmpeg lulus. Ujian ini bukan penilaian subjektif sebutan. Bukti: argon-original-voice-dependencies.json, argon-cp31118-voice-proof.json dan artifacts/argon/malay-voice-cp31118.wav.

Gunakan `python3 scripts/argon-original-voice-python.py <skrip/argumen>` untuk Python suara asal. Contoh: `python3 scripts/argon-original-voice-python.py -m pip check`. Wrapper tidak menukar Python atau shared libraries global.

Semua fail gantian yang diminta dalam senarai 13 fail terdahulu kini telah diterima dan disahkan; tiada baki kegagalan yang diketahui dalam senarai itu. Ini tidak membuktikan semua preset, semua model pilihan atau setiap aliran extension sudah diuji. Runtime/model/binary besar kekal dalam workspace, bukan GitHub. Snapshot Codex Cloud dan pemulihan dalam task baharu belum disahkan.
