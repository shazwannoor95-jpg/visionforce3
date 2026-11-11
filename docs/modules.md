# Modul pilihan

Jangan pasang modul ini sehingga tugas memerlukannya. Setiap modul mesti diasingkan; jangan gabungkan persekitaran Python GPU dengan dokumen.

| Modul | Status | Pelan dependency apabila dipilih |
|---|---|---|
| Motion Canvas | REGISTERED, NOT INSTALLED, NOT TESTED | Projek Node berasingan melalui create-motion-canvas; @motion-canvas/core, @motion-canvas/2d, Vite. Pin versi dan lockfile selepas tugas dipilih. MIT. |
| MoviePy | REGISTERED, NOT INSTALLED, NOT TESTED | venv tersendiri; MoviePy 2.x, NumPy, Pillow, imageio, FFmpeg tersedia. API v1/v2 berbeza. MIT. |
| Manim Community | REGISTERED, NOT INSTALLED, NOT TESTED | venv tersendiri; Manim, Cairo/Pango/pkg-config. LaTeX hanya untuk formula yang memerlukannya. MIT. |
| Playwright | INSTALLED 1.56.1, TESTED | modules/browser; Chromium sistem. Browser Cloud terasing, bukan sesi peribadi pengguna. |

## GPU: OPTIONAL / NOT INSTALLED / NOT TESTED

Rujukan versi ialah SHA dalam repository-registry.json, bukan versi pakej yang dipasang.

| Projek | Keperluan rujukan upstream | Lesen / keserasian |
|---|---|---|
| ComfyUI | pyproject 0.45.0; Python >=3.10; README mengutamakan 3.13. PyTorch/driver bergantung GPU. VRAM bergantung model; dakwaan 4GB + 8GB RAM dengan offload bukan jaminan semua workflow. | GPL-3.0; lesen setiap model/custom node diperiksa berasingan. |
| FramePack | Python 3.10 berasingan; NVIDIA RTX 30/40/50 dengan fp16/bf16; minimum 6GB VRAM. Pakej Windows rujukan CUDA 12.6/PyTorch 2.6. Model auto-download >30GB: jangan jalankan demo sekarang. | Kod Apache-2.0; semak lesen checkpoint asas dan dependencies sebelum penggunaan komersial. |
| Wan 2.2 | PyTorch >=2.4, torchvision >=0.19, diffusers >=0.31, transformers 4.49–4.51.3; flash_attn memerlukan padanan CUDA/PyTorch. TI2V-5B contoh 24GB VRAM; A14B contoh 80GB. | README menyatakan Apache-2.0 untuk model dengan syarat penggunaan; semak LICENSE.txt dan model card varian dipilih. |

Tiada model AI dimuat turun, GPU disewa atau proses berbayar dimulakan. Kos semasa tindakan ini: tiada perkhidmatan GPU berbayar dimulakan (kos langganan Cloud sedia ada tidak diaudit). Kos masa depan belum dianggarkan tanpa provider/region/GPU/durasi; kira kadar sejam × masa + storan + egress, dan sahkan sebut harga sebelum memilih. Keserasian GPU belum diuji pada mesin ini.

Sumber: README, LICENSE dan requirements pada SHA yang direkodkan; https://github.com/Comfy-Org/ComfyUI ; https://github.com/lllyasviel/FramePack ; https://github.com/Wan-Video/Wan2.2 .
