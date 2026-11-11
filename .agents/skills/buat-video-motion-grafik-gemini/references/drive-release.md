# Keluaran Gemini 10 November 2026 — folder utama

- Folder keluaran: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF
- Toolkit: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF
- Model MeloTTS-MS + Malay BERT dan source: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF
- Folder induk pengguna: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF

Ambil `Gemini_Setup_2026-11-10.md` daripada folder keluaran untuk pautan terus serta SHA-256 dua manifest:

1. `Gemini_Motion_Manifest_2026-11-10.json` bagi 11 pek toolkit.
2. `Gemini_VO_Models_Manifest_2026-11-10.json` bagi 89 bahagian yang membentuk sembilan fail model/config/tokenizer/source.

Ambil helper `gemini_cache.py` dan `model_bundle.py` yang disertakan secara berasingan jika core belum tersedia. Muat turun hanya keperluan projek dan gunakan nama fail tepat dalam manifest. Semua fail upload keluaran ini kurang daripada 10,000,000 bait. Semua bahagian model maksimum 8,000,000 bait; pek toolkit terbesar sekitar 8.01 MB. Berat model penuh dibentuk semula secara setempat selepas semua bahagian sah tersedia.

Hash setiap bahagian, fail penuh dan pek ditentukan daripada bait sebenar; jangan menggantikan dengan hash nama fail atau metadata folder. File-size/pack verification bukan bukti dependency OS/Python atau inferens TTS sudah ready. Ikut preflight khusus dalam skill.

Semua pek toolkit, bahagian model, manifest, helper dan SKILL.md terkini berada terus dalam folder utama yang sama. Kekalkan susunan satu aras ini; jangan mencipta folder Drive baharu. Nama fail dan ID sedia ada dikekalkan apabila memindahkan fail.

## Dependency VO untuk pemasangan bersama skill

`Gemini_VO_Dependencies_Manifest_2026-11-10.json` serta 54 bahagian arkib berada dalam folder utama yang sama. Ini membawa Python 3.11, eSpeak-ng/libespeak-ng1 beserta dependency/data, 104 wheel CPU dan kamus normalisasi. Baca `offline-vo-dependencies.md`; pasang bersama core, kemudian jalankan proof TTS. Jangan cipta folder Drive baharu.
