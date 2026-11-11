# Suara dan baki bundle Argon

## Kerja yang telah dilakukan

- Semua bahagian suara yang dibekalkan telah diperiksa terhadap saiz/SHA-256 manifest. Nama tambahan `.zip`/`.gz` pada beberapa bahagian pertama dikenal pasti; hanya bahagian yang baitnya sepadan hash asal dipetakan semula. Tiada hash diubah.
- Model MeloTTS-MS `model.pth`, config dan README serta source archive berjaya digabung dan disahkan. Lokasi: `/workspace/argon-runtime/vo-models`.
- Metadata/tokenizer Malay BERT disahkan dan dipasang; weight BERT BELUM lengkap.
- Bundle eSpeak dan wheelhouse CPython 3.11 berjaya digabung, disahkan dan diekstrak. Semua dependency wheelhouse dipasang menggunakan `pip --no-index --require-hashes` ke `/workspace/argon-runtime/vo-venv`. `pip check` lulus. Dependency termasuk Torch CPU, torchaudio, transformers, malaya, malaya-speech, phonemizer dan MeloTTS.
- Bundle CPython asal gagal hash bahagian pertama. CPython 3.11.17 dipasang melalui uv daripada python-build-standalone sebagai runtime CP311 berasingan. Ini bukan dakwaan bundle CPython 3.11.18 asal berjaya.
- eSpeak dipasang dalam prefix pengguna tanpa mengubah sistem. Senarai suara Melayu lulus; pustaka pulseaudio dibekalkan pada path runtime yang betul.
- Support/browser-libs yang lulus hash diekstrak ke prefix berasingan. Chromium sistem kekal browser aktif. Node/FFmpeg sistem dan HyperFrames 0.9.4 yang diuji dikekalkan.

## Blok luaran: inferens MeloTTS Melayu belum boleh diuji

`malay-bert__pytorch_model.bin.part0001` tidak dibekalkan dengan bait yang sepadan manifest. Fail bernama `.part0001.zip` dalam RAR mempunyai 8,000,653 bait, sedangkan manifest menjangkakan 8,000,000 bait; hash tidak sepadan. Bahagian 2–56 lulus. Pemetaan nama sahaja tidak membaiki kandungannya.

Perlu muat naik semula SATU bahagian asal yang betul: `malay-bert__pytorch_model.bin.part0001` (8 MB; boleh dibungkus ZIP biasa). Tidak perlu ulang semua 63 RAR. Manifest yang digunakan ialah Gemini_VO_Models_Manifest_2026-11-10.json. Alternatif: akses rangkaian HTTPS ke huggingface.co dan domain CDN redirect bagi revision mesolitica/bert-base-standard-bahasa-cased `7e5ef50008a66002b205828de3828e68ffee2887`; percubaan semasa disekat HTTP 403. Jangan menggantikan checkpoint atau hash tanpa sumber keluaran yang disahkan.

Preflight terkini: argon-voice-preflight.json. `ready: false` kerana weight BERT hilang. Tiada audio MeloTTS dilaporkan berjaya; suara eSpeak bukan pengganti senyap.

## Bundle lain yang masih disekat

Pek fonts/vlog_payload_03 dan arkib lama Node 26/Chrome 152/FFmpeg 9/HyperFrames 0.8.185/0.9.2 gagal hash. Bahagian ZIP pemulihannya turut diperiksa dan beberapa gagal hash/header ZIP. Ini memerlukan salinan sumber yang betul, bukan reinstall berulang. Status terperinci lama: argon-runtime-bundles.json dan ARGON-EXTENSIONS-MS.md. Runtime render semasa yang lulus ujian kekal tersedia.

## Penggunaan dan persistence

`python3 scripts/argon-voice-python.py -m pip check` menggunakan Python terasing dan selector cache yang boleh ditulis. Model/bundle/node_modules kekal di `/workspace/argon-runtime`, di luar Git. Source/skrip/laporan berada dalam Git; snapshot Cloud dan pemulihan runtime pada task baharu masih belum disahkan. Tidak semua extension mempunyai inferens ujian yang lulus. Tiada GPU disewa atau proses berbayar dimulakan.
