$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Push-Location "$root/video"
try {
 npm ci --ignore-scripts
 if ($LASTEXITCODE -ne 0) { throw 'Remotion dependencies gagal' }
 node node_modules/@remotion/cli/remotion-cli.js render src/index.tsx VisionForge3 "$root/artifacts/desktop/windows-remotion.mp4" --concurrency=2
 if ($LASTEXITCODE -ne 0) { throw 'Render Windows gagal' }
} finally { Pop-Location }
# FFprobe daripada pakej compositor rasmi yang dipin oleh lockfile Remotion.
$ffprobe = Get-ChildItem "$root/video/node_modules/@remotion" -Recurse -Filter ffprobe.exe | Select-Object -First 1
$ffmpeg = Get-ChildItem "$root/video/node_modules/@remotion" -Recurse -Filter ffmpeg.exe | Select-Object -First 1
if (!$ffprobe -or !$ffmpeg) { throw 'Binary verifikasi Remotion tidak tersedia' }
$json = & $ffprobe.FullName -v error -count_frames -show_streams -show_format -of json "$root/artifacts/desktop/windows-remotion.mp4"
if ($LASTEXITCODE -ne 0) { throw 'FFprobe gagal' }
$probe = $json | ConvertFrom-Json
$video = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
if ($video.width -ne 1920 -or $video.height -ne 1080 -or $video.avg_frame_rate -ne '30/1' -or $video.nb_read_frames -ne '120') { throw 'Dimensi/FPS/frame gagal' }
& $ffmpeg.FullName -v error -i "$root/artifacts/desktop/windows-remotion.mp4" -f null -
if ($LASTEXITCODE -ne 0) { throw 'Decode Windows gagal' }
$json | Set-Content "$root/artifacts/desktop/windows-video-probe.json"
