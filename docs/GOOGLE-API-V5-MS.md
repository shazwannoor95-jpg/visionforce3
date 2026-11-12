# Google AI Studio / Gemini API — v0.0.0.5 DRAFT

Gambar pengguna menunjukkan `Failed to list API keys: permission denied` serta isu pada Default Gemini Project. Ini bukti penolakan akses halaman Google, bukan bukti key tersimpan atau API inference berjaya. Punca khusus (sesi embedded, akaun, hak akses projek, sekatan atau kelayakan) belum disahkan. Aplikasi tidak mengubah IAM atau billing pengguna.

AI Providers kini mempunyai Google AI Studio / Gemini. Key dimasukkan hanya dalam aplikasi dan disimpan melalui Electron safeStorage; basic_text/tanpa penyulitan ditolak. Key tidak dipulangkan ke renderer atau dimasukkan ke URL/log. Data provider OpenAI/Anthropic dikekalkan.

Uji akses baca API memanggil GET `https://generativelanguage.googleapis.com/v1beta/models` dengan header `x-goog-api-key`, tiada redirect, timeout 15 saat. Respons memaparkan model yang menyokong generateContent. HTTP 400/401/403/404/429/5xx memberi panduan tetap tanpa memaparkan respons mentah yang mungkin mengandungi rahsia. API_READ_VERIFIED hanya akses baca; bukan bukti inferens/TTS atau billing.

Buka/cipta projek, pilih Google, simpan key, uji baca dan semak senarai model. Bahagian Gemini API menyediakan teks projek, model teks, model suara dan suara. Model cadangan boleh berubah; pilih model yang tersedia untuk key/projek anda. Jana jawapan/Jana suara meminta pengesahan native sebelum teks dihantar melalui generateContent, timeout 120 saat tanpa retry. Respons teks disimpan dalam perbualan; respons panjang disimpan sebagai gemini-answer.txt. Suara PCM mono 24 kHz 16-bit dibungkus WAV dan dilampirkan ke media projek. Penjanaan boleh menggunakan kuota/caj Google; tiada panggilan penjanaan sebenar dibuat oleh CI.

Key, login AI Studio dan langganan Google AI Pro adalah keadaan yang berasingan. Tiada fail PDF dihantar oleh aliran ini. AI provider Google belum menggantikan router brief tempatan secara automatik; gunakan butang penjanaan Gemini. Audio tidak dicampurkan ke video secara automatik.

Untuk ralat halaman key: tekan Buka halaman API key Google untuk membuka browser sistem. Jika ralat sama berlaku, sahkan akaun yang betul, projek yang anda mempunyai akses, dan minta pentadbir projek menyemak kebenaran/kelayakan serta Generative Language API. Semak sekatan key dan kuota untuk kegagalan API. Jangan tampal key dalam chat atau commit repo. Jika ralat hanya berlaku dalam embedded browser, gunakan laluan API dengan key yang dicipta pada browser sistem. Diagnosis embedded browser sebenar masih belum diuji pada akaun pengguna.

Probe browser kini membezakan halaman pengurusan API key daripada editor Playground dan mengesan mesej permission denied dalam gambar. Ia tidak mendakwa login berjaya. Pengesanan DOM bersifat terhad dan boleh berubah jika Google menukar halaman.

Ujian: 55 unit tests PASS, typecheck/build PASS, Linux Electron smoke PASS. Unit tests menggunakan fetch mock untuk header/endpoint, model, teks, TTS/WAV, respons kosong/disekat, model berbahaya dan ralat HTTP tanpa pendedahan key. Smoke memeriksa pilihan Google dan halaman ralat; pada Windows ia turut menyimpan key fixture dengan penyulitan OS dan membatalkan penjanaan sebelum rangkaian. Tiada key sebenar, akaun pengguna atau panggilan berbayar digunakan. Google API langsung dan penjanaan akaun pengguna: NOT RUN.

Rujukan protokol: https://ai.google.dev/api/generate-content dan https://ai.google.dev/gemini-api/docs/speech-generation ; contoh audio rasmi https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb (mono 24kHz PCM/WAV).

Checkpoint v0.0.0.4: checkpoint/google-api-20261112. Versi 5 diperuntukkan melalui ledger remote. Branch feat/v41-google-api; tiada merge main atau Stable Release automatik. Keputusan native Windows tersedia dalam Actions dan branch ci/windows-evidence-v0.0.0.5 selepas workflow selesai.
