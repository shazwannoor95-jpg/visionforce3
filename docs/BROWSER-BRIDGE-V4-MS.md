# Browser ke projek — v0.0.0.4 DRAFT

v0.0.0.3 hanya membuka browser dan menyimpan sesi. Login bukan sambungan agent kepada projek. Versi ini menambah bridge pemindahan teks secara eksplisit:

1. Buka/cipta projek di Studio. Buka Browser Automation dan browser aplikasi. Login sendiri, kemudian buka Playground teks.
2. Tekan Semak sambungan. EDITOR_FOUND bermakna satu ruang prompt kelihatan ditemui; ia bukan pengesahan akaun atau kejayaan inferens. LOGIN_REQUIRED ialah halaman Google Accounts. PAGE_NOT_READY bermakna tiada editor dikesan, termasuk halaman yang masih loading. Status tidak lagi statik MANUAL_ACTION_REQUIRED sahaja.
3. Guna brief projek atau taip Brief AI Studio. Pindahkan brief menghantar teks itu ke halaman Google menggunakan input Chromium. Prompt sedia ada tidak ditimpa. Tiada fail/PDF dihantar dan tiada Run automatik.
4. Semak dan tekan Run sendiri di AI Studio. Selepas jawapan tersedia, pilih teks jawapan, kembali ke aplikasi dan tekan Ambil teks jawapan yang dipilih.
5. Semak/edit pratonton, kemudian Simpan jawapan ke projek. Jawapan dilabel import pengguna dan kekal dalam SQLite selepas restart. Kandungan provider dianggap teks, tidak dilaksanakan sebagai arahan atau kod.

Browser sistem yang dibuka melalui openExternal kekal berasingan. Akaun yang login dalam browser sistem tidak dikongsi dengan browser aplikasi. Status ditutup merujuk tetingkap yang dimiliki instance aplikasi ini, bukan semua Chrome pada PC. Gambar pengguna menunjukkan browser sistem pernah dibuka; gambar sahaja tidak membuktikan status tetingkap aplikasi yang lain.

Browser aplikasi kekal tanpa preload/Node dan tanpa eksport cookie/password. Probe hanya memeriksa ruang editor; tidak membaca identiti akaun. Respons hanya dibaca selepas pengguna memilih teks dan menekan butang. Had teks 20000 aksara. Laluan suara: tekan Buka Speech / TTS, pilih satu pembicara di AI Studio, pindahkan skrip, pilih suara dan tekan Run sendiri. Klik Download WAV/MP3 pada browser aplikasi. Muat turun daripada webContents browser aplikasi sahaja ditangkap ke direktori sementara khusus (had 50 MiB); format lain ditolak. Tekan Import audio ke projek untuk menyalin audio ke media projek. Audio pending belum diimport dibuang ketika app ditutup; import dahulu. Audio yang diimport kekal selepas restart. Browser sistem perlu Lampirkan fail secara manual. Penjanaan suara sebenar, pencampuran audio ke video dan agent penuh belum diuji/dilaksanakan sepenuhnya.

43 unit tests, build/typecheck dan Electron Linux smoke PASS. Fixture browser menguji probe, pemindahan teks, penolakan overwrite, import pilihan, navigasi Speech, muat turun WAV, import audio dan penyimpanan selepas restart, buka/reuse/tutup/reopen dan pengasingan Node. Fixture bukan bukti keserasian halaman Google terkini. Login akaun dan aliran langsung Google: NOT RUN; perlu ujian pengguna pada peranti mereka. Jika Google menukar DOM atau terdapat beberapa editor, adapter menolak dengan sebab dan tidak mengaku connected.

Checkpoint sebelum perubahan: checkpoint/browser-project-bridge-20261112 (v0.0.0.3). Versi diperuntukkan ledger remote; tiada merge main, force push atau Stable Release automatik. Log CI dan installer disediakan oleh workflow Windows pada branch feat/v41-browser-project-bridge.
