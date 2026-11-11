# Dependency VO offline daripada Drive

## Kandungan

1. Platform dan profil
2. Pasang bersama skill
3. Semakan dan pemulihan
4. Provenance dan batas ujian

## 1. Platform dan profil

Semua fail berada terus dalam folder utama: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF . Jangan cipta subfolder Drive. Muat turun manifest `Gemini_VO_Dependencies_Manifest_2026-11-10.json` dan bahagian yang dinyatakan di dalamnya; setiap bahagian maksimum 8,000,000 bait, sentiasa bawah 10 MB. Hash manifest disimpan dalam panduan setup berasingan supaya tiada kitaran hash dengan core.

Profil ini untuk **Linux x86_64, glibc >= 2.35, CPU, ABI CPython 3.11**. Ia membawa Python 3.11.18 sendiri, jadi versi Python aktif VM tidak perlu diturunkan. `dpkg-deb` diperlukan untuk mengekstrak pakej Ubuntu ke prefix pengguna; pemasang tidak mengubah libc atau memasang pakej sistem secara global. Semak platform sebelum memuat turun; ARM64, Windows, macOS atau musl memerlukan profil berasingan dan tidak boleh dianggap serasi.

| Kandungan | Key komponen | Butiran |
|---|---|---|
| Python | python_cp311 | Runtime lengkap Python 3.11.18 beserta stdlib, ensurepip dan lesen |
| eSpeak | espeak_linux | espeak-ng/libespeak-ng1 1.50, data suara dan dependency .deb Ubuntu 22.04 amd64 termasuk pcaudio, sonic dan library berkaitan |
| Wheelhouse | wheelhouse_cp311_cpu | 104 wheel, requirements.lock.txt berhash, metadata/provenance dan kamus Demoji asal untuk normalisasi offline |

Versi teras: torch **2.5.1+cpu**, torchaudio **2.5.1+cpu**, transformers **4.38.2**, malaya **5.1.1**, malaya-speech **1.4.0rc2**, phonemizer **3.3.0**. Torch dan torchaudio mesti sepadan. Baca `assets/vo-dependencies/profile.json` serta lock untuk semua versi dan SHA-256; jangan menukar pin melalui `pip install latest` ketika render.

Wheel `melotts==0.1.2+geminims2` ialah adaptasi metadata dependency untuk inferens Melayu sahaja daripada fork Mesolitica yang sama. Ia tidak memerlukan Gradio atau komponen bahasa Jepun/Korea untuk laluan MS. Kod Melayu dan berat model dikekalkan, dengan adapter import malas serta kamus normalisasi setempat. Pin Transformers asal 4.27.4 bercanggah dengan import LlamaModel oleh Malaya; profil ini diuji dengan 4.38.2. Jangan memasang source ZIP asal di atas wheel profil dan kemudian menganggap lock masih sah.

## 2. Pasang bersama skill

Bagi pemasangan penuh skill Gemini yang merangkumi VO, pasang ketiga-tiga komponen dependency bersama core dalam fasa persediaan pertama. Semak cache dan guna semula yang sah; jangan memuat turun atau memasangnya semula bagi setiap video. Model MeloTTS/BERT menggunakan manifest model berasingan dan tidak digandakan dalam wheelhouse.

```bash
# Core skill mesti tersedia dahulu supaya helper dan adapter lengkap tersedia.
python3 scripts/dependency_bundle.py restore --manifest /path/Gemini_VO_Dependencies_Manifest_2026-11-10.json --parts-dir /path/downloaded-parts --root /persistent-cache/vo-deps --need python_cp311 espeak_linux wheelhouse_cp311_cpu
python3 scripts/dependency_bundle.py verify --manifest /path/Gemini_VO_Dependencies_Manifest_2026-11-10.json --root /persistent-cache/vo-deps

# Semua pemasangan berikut menggunakan fail setempat, tanpa pip/apt online.
python3 scripts/install_vo_dependencies.py --manifest /path/Gemini_VO_Dependencies_Manifest_2026-11-10.json --bundle-root /persistent-cache/vo-deps --prefix /persistent-cache/vo-runtime-cp311 --report /path/project/vo-dependencies-ready.json

# Selepas model dipulihkan dengan model_bundle.py:
python3 scripts/setup_melotts.py --offline --dependency-root /persistent-cache/vo-runtime-cp311 --model-root /persistent-cache/malay-vo --report /path/project/melotts-ready.json
```

`--manifest-sha256 HASH` pada helper restore/verify mengesahkan manifest daripada panduan setup. Pemasang menyemak hash arkib penuh sebelum ekstrak; pip menggunakan `--no-index --require-hashes`. Semua wheel dan dependency transitif sudah dibina. Tiada compiler atau build source diperlukan di Gemini.

Prefix pemasangan mengandungi Python berasingan, venv, eSpeak dan library, wrapper serta `runtime-env.json`. `setup_melotts.py --dependency-root` membaca fail environment itu dan menyediakan PATH, LD_LIBRARY_PATH, PHONEMIZER_ESPEAK_LIBRARY serta kamus normalisasi bagi subprocess sahaja. Kekalkan prefix pada path asal selepas venv dibuat; gunakan prefix baharu jika mahu berpindah lokasi. Jangan memindahkan venv secara mentah atau menulis ganti folder custom pengguna.

## 3. Semakan dan pemulihan

`dependency_bundle.py` mengesahkan setiap bahagian serta fail arkib penuh. Ia bukan pemasang runtime. `install_vo_dependencies.py` menolak platform tidak serasi, prefix tanpa receipt yang mengandungi fail pengguna, hash salah, traversal atau link arkib yang keluar root. Ia menguji `pip check`, import enam pakej utama dan suara Melayu eSpeak. `ready:true` dependency belum membuktikan inferens TTS; jalankan setup_melotts untuk WAV Melayu sebenar.

Guna semula prefix/receipt yang sepadan. Jika pin atau fail perlu berbeza, pilih cache versi baharu; jangan paksa overwrite fail pengguna. Jika bahagian hilang, ambil fail tepat daripada manifest dan ulang restore. Jika pustaka host yang tidak dibundel masih kurang, laporkan `ldd`/error sebenar dan jangan menggantikan host libc atau menaikkan kebenaran.

Whisper, PyAudio untuk mikrofon, GPU/CUDA dan backend bahasa lain bukan syarat inferens MS dalam profil ini. Jangan melabel ciri tersebut dipasang hanya kerana dependency VO lulus. Kekalkan runtime/model apabila membersihkan frame render.

## 4. Provenance dan batas ujian

Torch/torchaudio CPU daripada indeks rasmi PyTorch; wheel lain daripada PyPI atau wheel yang dibina daripada source Mesolitica dipinkan. Source commit, perubahan metadata inferens, hash wheel, pakej .deb dan lesen disimpan dalam profil, lock, indeks serta arkib asal. Kamus Demoji asal ditambah kerana normalizer Malaya memintanya walaupun model sudah tersedia; ia dimuatkan setempat tanpa mengubah makna normalisasi.

Ujian setempat merangkumi pemasangan wheel tanpa indeks, `pip check`, eSpeak dan sintesis Melayu dengan guard rangkaian. Simpan laporan ujian sebenar. Ini bukan dakwaan pemasangan sudah diuji dalam akaun/VM Gemini pengguna; ulang preflight dan proof ringkas selepas pemasangan di sana.
