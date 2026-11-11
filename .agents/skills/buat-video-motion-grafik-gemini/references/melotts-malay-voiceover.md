# Voice-over BM: Mesolitica MeloTTS-MS + Malay BERT

## Kandungan

1. Pilihan suara dan sumber
2. Model daripada Drive
3. Pemasangan dan inferens
4. Sintesis, ekspresi dan mix
5. Cache, checkpoint dan QA

## 1. Pilihan suara dan sumber

Untuk VO BM baharu dalam Gemini, gunakan fork **Mesolitica MeloTTS-MS** dengan **Malay BERT**. Kekalkan audio projek yang telah dipersetujui; pilihan penyedia eksplisit pengguna mengatasi lalai ini. Jangan memasang MeloTTS asal lalu menganggap `MS` tersedia. BERT ialah pengekod ciri teks untuk TTS, bukan suara atau pengganti checkpoint akustik.

| Komponen | Sumber dan revision |
|---|---|
| Fork | https://github.com/mesolitica/MeloTTS-MS ; commit `eb9ef5fb6dd283da3ba0e811cdb26aca147f58b6` |
| Checkpoint inferens | https://huggingface.co/mesolitica/MeloTTS-MS ; revision `1bb57b4c1c8574585b21a35892b131da27094b56` ; `model.pth` + `config.json` |
| Malay BERT | https://huggingface.co/mesolitica/bert-base-standard-bahasa-cased ; revision `7e5ef50008a66002b205828de3828e68ffee2887` ; `pytorch_model.bin`, config, vocab dan tokenizer |
| Normalizer/fonem | https://github.com/mesolitica/malaya-speech , pakej `malaya`, `phonemizer` dan OS eSpeak/eSpeak-ng |

Sumber model rasmi mempunyai typo `from from melo.api`; gunakan `from melo.api import TTS`. Fork semasa membaca path BERT melalui `MODEL_ID`. Model-card menyenaraikan tiga speaker; baca `config.json` sebenar. ID 0 (`husein-chatbot`) ialah pilihan narator asas contoh ini. Jangan memilih speaker berdasarkan nama tokoh untuk video berita/politik kecuali diminta secara jelas.

## 2. Model daripada Drive

Folder keluaran: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF . Dapatkan `Gemini_VO_Models_Manifest_2026-11-10.json` dan hash daripada panduan setup keluaran sama. Manifest memuatkan pautan Drive dan SHA-256 setiap bahagian serta setiap fail penuh.

Semua fail upload baharu di bawah **10,000,000 bait**; bahagian model maksimum **8,000,000 bait**. Fail `.partNNNN` ialah potongan bait, bukan ZIP yang boleh diekstrak sendiri. Jangan mengimportnya terus ke PyTorch. Muat turun bahagian bagi `melotts_ms`, `malay_bert` dan `melotts_source` menggunakan akses Drive yang tersedia, kemudian:

```bash
python3 scripts/model_bundle.py restore --manifest /path/Gemini_VO_Models_Manifest_2026-11-10.json --parts-dir /path/downloaded-parts --root /persistent-cache/malay-vo --need melotts_ms malay_bert melotts_source
python3 scripts/model_bundle.py verify --manifest /path/Gemini_VO_Models_Manifest_2026-11-10.json --root /persistent-cache/malay-vo --need melotts_ms malay_bert melotts_source
```

`--manifest-sha256 HASH` mengesahkan manifest daripada panduan setup. Helper menggunakan streaming, mengekalkan fail penuh yang sah, menolak bahagian hilang/rosak, path tidak selamat serta fail pengguna yang berbeza. Fail model asal dicantum semula tanpa kuantisasi, perubahan berat atau serialisasi semula. Checkpoint optimizer/discriminator latihan tidak diperlukan untuk inferens dan tidak dimuat turun.

## 3. Pemasangan dan inferens

Baca [dependency VO offline](offline-vo-dependencies.md) dan gunakan `Gemini_VO_Dependencies_Manifest_2026-11-10.json` dalam folder utama yang sama. Bundle membawa runtime Python 3.11, 104 wheel lengkap, eSpeak/data/library dan kamus normalisasi. Semak cache, cantum/sahkan bahagian, kemudian pasang ke prefix pengguna dengan `scripts/install_vo_dependencies.py`. Jangan memasang wheel di Python/ABI lain atau menimpa environment video sedia ada.

```bash
python3 scripts/dependency_bundle.py restore --manifest /path/Gemini_VO_Dependencies_Manifest_2026-11-10.json --parts-dir /path/dependency-parts --root /persistent-cache/vo-deps
python3 scripts/install_vo_dependencies.py --manifest /path/Gemini_VO_Dependencies_Manifest_2026-11-10.json --bundle-root /persistent-cache/vo-deps --prefix /persistent-cache/vo-runtime-cp311 --report /path/project/vo-dependencies-ready.json
python3 scripts/setup_melotts.py --offline --dependency-root /persistent-cache/vo-runtime-cp311 --model-root /persistent-cache/malay-vo --report /path/project/melotts-ready.json
```

Helper membaca runtime-env.json bagi eSpeak, library, venv dan kamus setempat. Profil CPU menggunakan torch/torchaudio 2.5.1+cpu dan Transformers 4.38.2 supaya serasi import Malaya. Wheel MeloTTS-MS berlabel `0.1.2+geminims2` mengehadkan metadata dependency kepada inferens MS; berat model serta kod fonem asal dikekalkan. Adapter import malas mengelakkan tokenizer bahasa lain; cache kamus Demoji mengelakkan permintaan GitHub ketika normalisasi. Jangan memasang source ZIP asal di atas profil ini.

Ujian mesti menghasilkan WAV Melayu sebenar secara offline dan menyimpan report, proof serta versi dependency. `ready:true` memerlukan sampel audio sah, bukan import sahaja. Jika gagal, kekalkan ready:false dan baiki punca; jangan menukar model/bahasa secara senyap. Fail audio diluluskan dan pilihan penyedia eksplisit pengguna tetap diutamakan.

## 4. Sintesis, ekspresi dan mix

Gunakan ayat BM Malaysia santai dan sapaan “korang” bagi explainer santai apabila sesuai. Kekalkan skrip diluluskan. Pecahkan narasi kepada frasa bererti, bukan satu perkataan setiap fail; beri emosi melalui pilihan kata, tanda baca, tekanan dan tempo. Gunakan API fork yang disahkan:

```python
import os
os.environ['MODEL_ID'] = '/persistent-cache/malay-vo/malay-bert'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from melo.api import TTS
model = TTS(language='MS', device='cpu', config_path='/persistent-cache/malay-vo/melotts-ms/config.json', ckpt_path='/persistent-cache/malay-vo/melotts-ms/model.pth')
model.tts_to_file('Korang pernah rasa macam ini?', 0, output_path='/path/project/phrase-001.wav', split=True, sdp_ratio=0, noise_scale=0.667, speed=1.0)
```

`speed=1.0` ialah titik mula, bukan janji durasi. Uji variasi kecil mengikut suara; jangan memecut secara ekstrem untuk memuatkan skrip. Model ini tidak mempunyai kawalan emosi/SSML ekspresif penuh yang dijamin. Untuk hidupkan penyampaian, gunakan variasi tempo/pitch/gain kecil setiap frasa yang sesuai, jeda sekitar 60–180 ms pada sambungan dan 180–350 ms pada pertukaran idea, kemudian dengar semula. Hormati brief laju/tanpa pause dan tempoh sebenar pengguna.

Mulakan EQ dengan high-pass sekitar 70–90 Hz, potongan rendah-tengah lembut jika keruh dan presence kecil jika diperlukan. Gunakan compressor ringan, de-esser hanya jika perlu, ducking muzik dan limiter. Pitch pascaproses sekitar ±0.2–0.6 semitone secara terpilih; gunakan pengekalan formant apabila penapis tersedia. Jangan modulasi setiap suku kata atau ubah pitch global berlebihan. `rubberband` memerlukan FFmpeg yang dibina dengan filter itu; semak filter sebenar. Jangan kelirukan menukar sample rate dengan pitch yang mengekalkan tempo.

Contoh asas EQ/mix, laras mengikut rakaman dan bukan wajib satu chain untuk semua suara:

```bash
ffmpeg -i phrase-001.wav -af "highpass=f=80,equalizer=f=250:t=q:w=1:g=-1.5,acompressor=threshold=0.125:ratio=2:attack=12:release=100,loudnorm=I=-16:TP=-1.5:LRA=9" -ar 48000 phrase-001-clean.wav
```

Simpan WAV mentah dan processed berasingan. Ukur durasi fail processed sebelum mencantum; buat crossfade sangat pendek hanya pada sempadan senyap supaya fonem tidak dipotong. Campur music/SFX/paper ASMR mengikut cue visual tanpa menenggelamkan VO. Sasaran mix video biasa sekitar -16 LUFS dan true peak ≤ -1 dBTP; ukur master sebenar, gunakan dua pass loudness bila diperlukan dan ikut arahan projek.

## 5. Cache, checkpoint dan QA

Audio final ialah jam utama: rekod offset/durasi setiap frasa selepas DSP serta cantuman, jalankan alignment/transkripsi apabila alat tersedia dan semak active-word highlights pada awal/tengah/akhir. Jangan menyamakan anggaran bilangan perkataan dengan sync sebenar. Split/spacing boleh diubah untuk sasaran 1:50–2:00 apabila brief meminta, sambil mengekalkan sebutan jelas dan gerakan berantai.

Simpan revision model, SHA-256, speaker ID, seed, teks setiap frasa, parameter TTS/DSP, environment lock dan path checkpoint. Semak nama Melayu/Arab, nombor, ayat agama serta singkatan. Jangan padam model/venv bersama frame render. Ujian packaging/checksum tidak membuktikan kualiti VO atau pemasangan dalam akaun Gemini; bezakan hasil yang benar-benar diuji.
