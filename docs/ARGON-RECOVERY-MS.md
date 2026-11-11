# Pemulihan bundle Argon — status terkini

12 fail upload gantian semuanya sepadan SHA-256 manifest asal. Bukti: argon-replacement-verification.json. Status dalam laporan terdahulu adalah sejarah sebelum pemulihan ini.

## Selesai

- Malay BERT lengkap digabung dan disahkan bersama MeloTTS-MS. Inferens Melayu offline sebenar LULUS, 44,100 Hz, 3.568 saat, peak 0.90448. Bukti: argon-voice-preflight.json dan `artifacts/argon/malay-voice-proof.wav`. Ujian ini mengesahkan inferens, sampel finite dan isyarat bukan senyap; penilaian subjektif sebutan belum dibuat.
- Node 26.13.0, Chrome Headless 152, FFmpeg/ffprobe 9, HyperFrames 0.9.2 dan 0.8.185 dipasang daripada semua bahagian yang digabung dan disahkan checksum penuh serta integriti fail selepas ekstrak. Lokasi berasingan: `/workspace/argon-runtime/compat`.
- Kedua-dua HyperFrames lama lulus proof render 1920×1080, 30fps, 120 frame/4 saat; decode lulus, 97 frame unik. Bukti: argon-compat-092-test.json dan argon-compat-08185-test.json. Node/browser/FFmpeg aktif yang dipilih helper dicatat dalam laporan tersebut; pemasangan binary tambahan tidak bermaksud semuanya dipilih sebagai default sistem.
- Pek fonts dan vlog_payload_03 lulus hash dan dipasang. Payload vlog lengkap dipulihkan; kesemua 823 aset lulus SHA-256 asal. Bukti: argon-repaired-assets.json dan argon-vlog-verification.json.
- Runtime HyperFrames 0.9.4/Remotion projek sedia ada dikekalkan. Tiada pertukaran global Node/FFmpeg atau reset repo.

## Baki dan persistence

Bahagian pertama CPython 3.11.18 asal masih belum dibekalkan dengan hash yang betul. Ia TIDAK menghalang fungsi suara yang telah lulus menggunakan CPython 3.11.17 berasingan. Hanya perlu upload `Gemini_VO_Deps_2026-11-10__cpython-3.11.18-linux-x86_64.tar.gz.part0001` jika pemulihan tepat bundle CPython asal diperlukan.

Model, Python, wheelhouse dan binary runtime berada di workspace, bukan GitHub. Source, aset skill, laporan, skrip dan audio ujian disimpan dalam repo. Snapshot/pemulihan Codex Cloud pada task baharu belum dibuktikan. Modul mikrofon/Whisper native pilihan yang tiada bukan prasyarat untuk inferens MeloTTS yang diuji; model tambahan tidak dimuat turun.

Suara: `PATH=/workspace/argon-runtime/bin:$PATH python3 scripts/argon-voice-python.py ...` menggunakan selector runtime dalam vo-env.json. Versi keserasian boleh diaktifkan melalui `/workspace/argon-runtime/compat/activate.sh`; ia tidak menggantikan runtime 0.9.4. Setup bundle tepat memerlukan manifest dan bahagian yang disahkan, kekal di `/workspace/argon-repaired` pada mesin ini.
