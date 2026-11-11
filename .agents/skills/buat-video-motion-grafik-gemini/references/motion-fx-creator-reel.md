# Gaya Motion FX Creator Reel

Gunakan nama **Motion FX Creator Reel** atau alias **Motion-Enhanced Talking Head**. Jadikan penyampai sebenar sebagai anchor, dengan rupa sinematik dan efek compositing yang bertukar mengikut dialog. Anggapnya varian pengarahan Cinematic Creator Reel yang boleh dipilih dengan namanya sendiri; kekalkan gaya lain dan ikut bahan serta arahan terbaru pengguna.

## Rujukan dan skop

Gunakan pemeriksaan visual dalam perbualan daripada [reel justyn.ai yang diberikan pengguna](https://www.instagram.com/reel/Dfcr8TJMKCV/?rpxt=MXFjb3BzYjM1dzhuZg%3D%3D). **Abaikan senarai di kanan video**, termasuk nama, bilangan dan sorotan efeknya. Jangan menyalin panel senarai atau UI Instagram ke video hasil. Jadikan tindakan yang kelihatan dalam video utama sebagai bukti.

| Sampel playback anggaran | Pemerhatian video utama |
|---|---|
| 0–2 saat | Cursor/kotak pemilihan simulasi dan salinan penyampai pada lapisan belakang |
| Sekitar 4 saat | Papan kekunci terapung di hadapan torso |
| Sekitar 6 saat | Siluet penyampai dibentuk daripada aksara/baris kod |
| Sekitar 8 saat | Footage kelihatan melalui huruf besar “dive” pada pentas krim |
| Sekitar 10–12 saat | Kad komen bertingkat dan caption bold dalam kotak putih |
| Sekitar 18 saat | Latar kabur sementara penyampai kekal jelas |
| Sekitar 20–22 saat | Widget voice note dan perubahan framing penyampai |
| Sekitar 24 saat | Lapisan surat khabar terkoyak untuk mendedahkan penyampai |

Anggap masa itu sebagai sampel playback, bukan onset/keyframe tepat. Pemain melaporkan keseluruhan reel sekitar **26.005 saat, 1080×1920**; jangan menetapkan spesifikasi projek baharu daripada angka itu. Audio belum disahkan melalui pendengaran. Nama gaya ini ialah label pengarahan deskriptif yang diterima pengguna, bukan preset rasmi HyperFrames. Sebutan Claude/ChatGPT dalam promosi tidak membuktikan backend, model matting, tracking atau kod asal. Panduan tersimpan tidak membuktikan render baharu telah diuji atau padanan 100%.

## Identiti dan koreografi

- Kekalkan penyampai sebagai fokus cerita dengan latar gelap, kontras sinematik dan warna kulit terkawal. Gunakan aksen krim/hijau gelap jika sesuai; adaptasi palet kepada projek.
- Padankan satu efek utama kepada satu beat bermakna. Gunakan objek UI untuk menerangkan tindakan, cloning untuk pengulangan/pilihan, dan perubahan tipografi atau bahan sebagai peralihan.
- Pelbagaikan medium shot, close-up, kedudukan grafik dan pentas grafik penuh. Bezakan pergerakan foreground, subjek dan background; elakkan satu poster rata yang hanya dizoom.
- Jangan memaksa kesemua mekanisme dalam setiap klip. Keutamaan ialah makna dialog, kesinambungan gestur dan bacaan teks pada telefon.
- Lindungi muka, mata dan teks sumber sepanjang entrance, hold dan exit. Kekalkan dialog/audio yang telah diluluskan.

## Mekanisme efek

| Mekanisme | Panduan pelaksanaan |
|---|---|
| Subject cloning | Asingkan penyampai dengan matte temporal sebenar atau alpha sah. Letakkan beberapa salinan pada depth/skala berbeza di belakang subjek utama. Selaraskan jam sumber; gunakan kelewatan masa hanya jika disengajakan dalam brief. |
| Simulated editor UI | Animasikan cursor, bingkai pemilihan dan pemegang resize pada anchor visual yang dipilih. Jika perlu mengikuti subjek, gunakan data posisi/keyframe yang disemak. Ini simulasi grafik, bukan bukti kawalan editor atau auto-tracking sebenar. |
| Floating UI | Bina papan kekunci, kad komen dan widget voice note berlapis dengan bayang serta entrance/exit berbeza. Gunakan teks projek atau demo neutral; jangan mereka testimoni, akaun atau bukti engagement. |
| Kinetic captions | Gunakan sans-serif bold gelap pada kotak putih/krim dengan padding mencukupi, kemudian bina frasa secara berperingkat mengikut cue audio. Jika pengguna meminta caption tanpa textbox, ikut arahan itu. |
| Video inside typography | Gunakan glyph sebenar sebagai alpha mask kepada footage bergerak. Ukur saiz/kerning dan jaga counter huruf; animasikan skala huruf atau kamera sebagai handoff ke footage penuh. |
| Code-body | Isikan siluet matte penyampai dengan tekstur aksara/kod yang bergerak secara deterministik. Kekalkan bentuk kepala/badan dapat dikenal pasti dan jangan paparkan rahsia atau kod sensitif. |
| Focus/depth | Blur latar secara beransur sambil subjek bermatte kekal tajam; periksa halo pada rambut, topi dan bahu. Bezakan efek compositing ini daripada dakwaan rakaman fokus optik sebenar. |
| Reframing | Gunakan push-in, pull-back atau pertukaran crop pada beat penegasan. Ukur safe area selepas transform dan kekalkan lip-sync serta gestur. |
| Paper-tear transition | Gunakan tekstur kertas/surat khabar dengan tepi alpha koyak, panel bergerak berasingan, bayang dan occlusion untuk mendedahkan footage. Bina bahan neutral mengikut topik; jangan warisi berita atau promosi sumber. |

Susun lapisan mengikut shot: footage/latar → salinan subjek/grafik belakang → subjek utama beralpha → UI/prop foreground → caption. Kekalkan footage asal dan semua lapisan yang perlu selaras pada masa sumber yang sama. Reset state matting pada cut dan semak tepi temporal, mikrofon, tangan serta props.

Untuk kod/surat khabar atau huruf yang meliputi seluruh frame, rancang pertukaran fokus dan masa pulang kepada penyampai. Kekalkan satu fokus bacaan; elemen sementara perlu selesai atau keluar sebelum fokus baharu mengambil alih.

## Audio, pelaksanaan dan QA

- Ambil cue caption daripada audio sebenar melalui aliran transkripsi sedia ada. Jangan menganggap label demo membuktikan ketepatan perkataan atau potongan senyap.
- Pilih muzik, click, typing, whoosh, impak dan ASMR kertas sebagai keputusan produksi baharu mengikut brief. Selaraskan onset dengan aksi visual dan duck muzik ketika pertuturan; jangan mendakwa bunyi itu telah didengar dalam rujukan.
- Gunakan Python/FFmpeg bagi footage/compositing dan HTML/SVG/Canvas + GSAP melalui HyperFrames bagi grafik apabila sesuai atau diminta. Nama gaya tidak menukar backend projek atau menambah ID kepada Atlas 922.
- Catat sumber footage, matte, z-order, mask tipografi/kod, cue, anchor UI, fon dan backend sebenar dalam manifest. Gunakan masa frame deterministik dan seed tetap bagi animasi prosedural.
- Render proof pendek bagi mekanisme tersukar yang dipilih: contohnya cloning + widget, glyph mask atau kertas koyak. Periksa playback biasa dan frame bersebelahan, bukan contact sheet sahaja.
- Pastikan matte stabil, tiada ghosting, huruf terbaca, kad tidak menutup muka/teks sumber, tiada panel senarai kanan, peralihan lengkap dan audio bersinkroni. Jalankan QA teknikal MP4/audio sebelum penghantaran master.

## Contoh arahan

`Guna @Buat Video Motion Grafik, Gaya Motion FX Creator Reel. Sunting footage saya menjadi MP4 menegak dengan penyampai sebagai fokus, cloning berlapis, widget UI terapung, kinetic captions, video di dalam huruf dan peralihan kertas koyak. Pilih efek mengikut dialog, kekalkan suara asal, serta jaga muka dan safe zone. Jangan masukkan senarai efek di kanan.`

`Use @Buat Video Motion Grafik in the Motion FX Creator Reel style. Edit my talking-head footage with cinematic grading, layered subject clones, floating UI widgets, kinetic captions, video-filled typography and a paper-tear transition. Match each effect to the dialogue, preserve the original voice, protect faces and source text, and omit the right-hand effects list.`
