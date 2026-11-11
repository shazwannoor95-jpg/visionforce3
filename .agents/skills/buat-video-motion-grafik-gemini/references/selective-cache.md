# Cache dan muat turun terpilih — keluaran 10 November 2026

## Fail keluaran

Folder induk: https://drive.google.com/drive/folders/1A9wvTKxG5apOsO61Tg-KIEVkTWG_uTEF . Buka panduan setup keluaran terkini terus dalam folder utama itu untuk pautan serta hash manifest tepat. Gunakan `Gemini_Motion_Manifest_2026-11-10.json` bagi toolkit dan `Gemini_VO_Models_Manifest_2026-11-10.json` bagi model. Semua fail upload keluaran baharu kurang daripada 10,000,000 bait; pek toolkit sasaran 7 MiB dan bahagian model maksimum 8,000,000 bait.

Jangan mencampur manifest 22 Oktober/1 November dengan pek baharu. Install ke root versi baharu jika fail lama atau suntingan pengguna bertembung. Pemasang mengekalkan fail custom, menolak ZIP traversal/symlink/hash salah dan mengesahkan semua fail terpilih sebelum menulis.

## Toolkit

```bash
python3 scripts/gemini_cache.py plan --manifest /path/Gemini_Motion_Manifest_2026-11-10.json --need core --root /vm/cache/motion-2026-11-10 --cache-root /path/existing/toolkit --packs-dir /path/cached-zips
python3 scripts/gemini_cache.py install --manifest /path/Gemini_Motion_Manifest_2026-11-10.json --need core --root /vm/cache/motion-2026-11-10 --cache-root /path/existing/toolkit --packs-dir /path/cached-zips
python3 scripts/gemini_cache.py verify --manifest /path/Gemini_Motion_Manifest_2026-11-10.json --need core --root /vm/cache/motion-2026-11-10
```

Helper tidak menggunakan rangkaian. `plan` memberikan `ready` bagi fail diekstrak yang sah, `install-local` bagi ZIP sah dalam cache dan `download-required` hanya bagi pek hilang/rosak. Muat turun yang perlu melalui saluran Drive sah, simpan nama tepat `packs[].name`, kemudian ulang install/verify. Folder kosong bukan cache sah.

| Keperluan | Pilih kategori |
|---|---|
| HTML/GSAP dan panduan gaya | core; Node/Chrome/dependency OS dipasang berasingan melalui preflight |
| Preset API Atlas terpinkan | core + atlas_locked; root kod terkunci ialah `atlas_locked/` |
| Kod/katalog preset sumber asal | presets, pilihan; bukan pengganti kontrak atlas_locked |
| Bank 20 watak V3 | characters |
| SVG / komponen Motion Array | svg / motion_array |
| Fon kreatif | fonts |
| Montaj/LUT/SFX VL | hanya vlog_payload yang diperlukan selepas semakan indeks |
| Preview katalog | previews, pilihan |

Semak `packs[].key/category/files` sebenar; kategori besar boleh mempunyai lebih satu ZIP. `atlas_preset.py` ialah shim kepada kod asal dalam pek atlas_locked, bukan renderer baharu. Boleh tetapkan `GEMINI_ATLAS_ROOT` kepada root runtime terkunci lain yang telah disahkan. Jangan membina semula kontrak untuk memintas kegagalan.

## Model VO

Gunakan `scripts/model_bundle.py` dan panduan `melotts-malay-voiceover.md`, bukan `gemini_cache.py`, untuk bahagian model. Model-files-ready berbeza daripada inferens-ready; perlukan `setup_melotts.py` dengan report `ready:true`. Semua berat model/tokenizer dipulihkan dari Drive, manakala wheel Python dan library OS memerlukan cache lengkap atau pemasangan online.

## Dependency VO offline

Pemasangan penuh skill yang merangkumi VO turut memerlukan manifest `Gemini_VO_Dependencies_Manifest_2026-11-10.json`. Baca `offline-vo-dependencies.md`; pulihkan hanya komponen `python_cp311`, `espeak_linux` dan `wheelhouse_cp311_cpu` yang belum sah, pasang secara offline dan semak inferens. Manifest model dan manifest dependency adalah berasingan; jangan gandakan model atau mengulang pip/apt pada setiap video.

## Runtime dan offline

Gunakan runtime-lock semakan 3 November, HyperFrames 0.9.4 + GSAP 3.15.0. Jalankan preflight khusus, Chrome launch sebenar, proof pendek dan QA. Jangan menyamakan asset checksum dengan browser/TTS/Whisper/RVM ready. Kekalkan cache model, venv, runtime dan receipt apabila membuang frame render. Jika offline dan keperluan hilang, laporkan fail tepat; jangan mencuba muat turun berulang atau menyimpan halaman login sebagai ZIP.

Manifest tidak membenam hash dirinya. Hash manifest disimpan dalam panduan setup berasingan selepas upload. Semakan packaging/checksum setempat bukan ujian dalam akaun Gemini pengguna.
