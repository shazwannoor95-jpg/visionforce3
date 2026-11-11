# VISIONFORGE 3 V3.5 — Fasa 0 dan 1

## Hasil dan bukti

Asas worker CPU telah dibina dan diuji. Ini bukan dakwaan platform chat AI penuh telah siap. Baseline repo: `907d161`, branch asal `work`; pembangunan dalam `feat/v35-core-worker`, tanpa merge atau push ke main. Repo lama visionforce2 diperiksa melalui clone metadata READ-ONLY di /tmp; HEAD `6303e45ad13cda329e67816317e4b52dc798d908` hanya mengandungi README (`# visionforce2`). Tiada perubahan atau push ke repo lama.

- `RepositoryManager`: 10 sumber rasmi didaftarkan; cubaan Git HTTPS read-only dan SHA remote direkodkan dalam v35-repositories.json. SHA pemerhatian bukan arahan upgrade dependency.
- `SkillRegistry`: 18 SKILL.md diperiksa nama/deskripsi/hash; v35-skills.json. Status VERIFIED ialah fail arahan, bukan keseluruhan fungsi READY.
- `DependencyProvisioningEngine`: memeriksa Node, Chromium, FFmpeg, FFprobe, Remotion 4.0.542 dan lockfile. Boleh melakukan npm ci tanpa lifecycle scripts hanya apabila pemasangan core diluluskan melalui allow_install; tiada remote script atau pemasangan GPU automatik. Worker semasa guna dependency tersedia dan BLOCKED jika tiada. Pipeline berjaya merekod TESTED selepas verifikasi output, bukan sekadar folder wujud.
- Parser PDF berteks: had 20 MiB/50 halaman/100k aksara. Dokumen berkunci/scanned ditolak; OCR, DOCX/PPTX upload ialah kerja seterusnya. Sumber tidak dijalankan sebagai arahan.
- Queue SQLite kekal di storan job; atomic claim mengelakkan dua worker mengambil job sama. Status PENDING/RUNNING/SUCCEEDED/FAILED; retry manual untuk FAILED/RUNNING selepas memastikan worker lama berhenti. Tiada janji exactly-once selepas crash atau recovery automatik.
- Renderer React/Remotion: petikan tepat setiap scene, provenance halaman, spring entry, bentuk berputar dan progress bar. Maksimum 8 petikan/180 aksara setiap satu, 3 saat setiap scene. Teks selebihnya disenaraikan sebagai tidak digunakan dalam coverage.json. Source Lock tidak bermaksud semua halaman pasti diliputi.
- Hasil: MP4 H.264/AAC, SRT, source.json, manifest.json, coverage.json dan render.log. Bed audio sintetik tempatan; voice-over belum disambungkan ke pipeline ini. Model suara terdahulu kekal tersedia berasingan.

## Ujian sebenar

`python3 -m unittest discover -s tests -v`: ujian parser, dokumen tidak sah/scanned, Source Lock, queue retry/failure, atomic claim, registry dan HTTP access guards.

`npm --prefix video run typecheck`: semakan TypeScript.

`python3 -m tests.smoke_pipeline`: HTTP upload PDF sebenar -> queue SQLite -> Remotion -> FFmpeg encode/decode -> HTTP download -> Source Coverage Report. Fixture dua petikan dengan angka 42; output 1920×1080, 30fps, 180 frame/6 saat, H.264/AAC. Dua checksum frame berbeza membuktikan frame berubah. Bukti di artifacts/v35-smoke/. Tiada MOCK PASS dikira sebagai ujian render.

## Matriks acceptance

| Ujian | Status | Skop |
|---|---|---|
| A Skills | PASS | Skill Remotion tersedia/dibaca, animasi sebenar dirender |
| B PDF -> MP4 | PASS (API/worker core) | Upload HTTP dan download sebenar; chat/LLM belum disediakan |
| C Source Lock | PASS (fixture) | Petikan tepat, halaman, SHA PDF, angka dan coverage; bukan semua dokumen |
| D Google AI Studio TTS | BLOCKED | Sesi login/browser/provider belum disambungkan; TTS tempatan bukan pengganti ujian D |
| E Browser video | BLOCKED | Provider/akses/kuota belum dipilih dan disahkan |
| F Hybrid | NOT RUN | Tiada klip provider browser |
| G Chat experience | NOT RUN | UI/chat/provider orchestration Fasa 2 |
| H Editor | NOT RUN | Pilihan Fasa 5 |

Planner semasa deterministik, memetik teks PDF; prompt disimpan sebagai brief tetapi tidak ditafsir oleh LLM. Login ChatGPT/Claude/API/billing tidak dipautkan. Tiada key diperlukan untuk core offline ini. Codex Cloud bukan server produksi kekal. Tiada GPU/model generatif besar atau servis berbayar diaktifkan.

## Lesen dan keserasian

FFmpeg sistem 7.1.5 Debian dibina `--enable-gpl`, menyokong libx264/AAC. Pengedaran binary memerlukan pematuhan GPL dan lesen library terlibat; jangan label binary ini LGPL sahaja. Remotion mempunyai lesen tersendiri: semak kelayakan komersial organisasi sebelum deployment. Lesen standalone repo skills tidak ditemui pada snapshot; status review diperlukan. Motion Array/custom assets tidak dianggap mempunyai hak redistribusi tanpa semakan fail LICENSE dan asal aset. Tiada aset pihak ketiga tersebut digunakan dalam fixture. Registry menyimpan review pending, bukan kelulusan undang-undang. Versi optional/GPU kekal seperti docs/modules.md; tidak dipasang lagi hanya kerana registry wujud.

## Had deployment

API core.server ialah alat pembangunan loopback, bukan servis multi-tenant. Belum ada login, TLS, rate limiting, antivirus, quota isolation, sandbox parser proses, private object storage, cancellation atau production auth. Jangan expose port kepada Internet. Worker tidak menerima kod daripada PDF/prompt; ia merender composition statik dengan props data. Jangan benarkan pengguna memuat naik kod React untuk worker ini.

Persistence: source/lockfile dalam Git; .data, output per-job dan node_modules diabaikan. Snapshot/runtime Cloud task baharu belum disahkan. PR/akses API GitHub dilaporkan berasingan daripada kebolehan git push; jangan merge automatik.
