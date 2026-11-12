# Login browser — v0.0.0.3 (DRAFT)

v0.0.0.2 hanya mempunyai placeholder Browser Automation. v0.0.0.3 menambah butang Buka / Login Google AI Studio, Tutup browser, dan Buka dalam browser sistem.

Browser aplikasi menggunakan partition `persist:vf-provider-google` dalam userData VISIONFORGE3, berasingan daripada profil Chrome pengguna dan renderer aplikasi. Login dilakukan sendiri pada halaman provider. Browser tidak mempunyai preload atau Node integration; sandbox/context isolation aktif. Navigasi top-level terhad kepada HTTPS AI Studio dan Google Accounts; popup yang dibenarkan dibuka dalam tetingkap yang sama. Permission kamera/mikrofon ditolak untuk aliran login ini.

Status BROWSER DIBUKA mengesahkan tetingkap sahaja. Ia tidak mengesahkan akaun sudah login. Google boleh menolak embedded browser; butang browser sistem membuka URL rasmi tetap. Sesi browser sistem tidak boleh dikawal oleh adapter ini. Tiada cookie/token/password dieksport atau dibaca oleh kod aplikasi.

Sesi aplikasi disimpan secara tempatan oleh Chromium. Untuk logout, guna halaman akaun dalam browser. Tutup browser mengekalkan sesi; ia bukan logout. Backup projek tidak memasukkan profil login; jangan commit/share folder userData.

Login ini belum melaksanakan automasi TTS, penjanaan video provider, atau inferens melalui langganan ChatGPT/Claude. AI Providers kekal konfigurasi API berasingan.

Ujian tempatan: 41 unit tests PASS; typecheck/build PASS; Electron Linux smoke PASS. Smoke menggunakan halaman fixture tempatan melalui interception untuk menguji butang, buka/reuse/tutup/buka semula dan pengasingan Node/preload. Ia tidak menguji login Google sebenar. Suite sama dijalankan di Windows development, packaged, installed kedua-dua path oleh CI sedia ada. Login akaun sebenar: NOT RUN, memerlukan pengguna pada peranti mereka.

Checkpoint sebelum perubahan: checkpoint/browser-login-controls-20261112, pada v0.0.0.2 yang telah diuji. Nombor versi diperuntukkan melalui ledger remote. Tiada merge main atau Stable Release automatik.
