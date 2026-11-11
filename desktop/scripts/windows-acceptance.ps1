$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$pkg = Get-Content "$root/desktop/package.json" | ConvertFrom-Json
$version = Get-Content "$root/version.json" | ConvertFrom-Json
$release = (Get-Content "$root/desktop/release/latest-build.json" | ConvertFrom-Json).directory
$setup = Join-Path $release "VISIONFORGE-3-$($version.display)-Setup-x64.exe"
$portable = Join-Path $release "VISIONFORGE-3-$($version.display)-Portable-x64.exe"
foreach ($f in @($setup,$portable)) { if (!(Test-Path $f)) { throw "Artifak tiada: $f" } }
function Run-Smoke($exe, $name) {
  $env:VF_TEST_APP_EXE = $exe
  $env:VF_SMOKE_REPORT = "$root/artifacts/desktop/$name"
  Push-Location "$root/desktop"
  try { node tests/electron-smoke.cjs; if ($LASTEXITCODE -ne 0) { throw "Smoke $name gagal" } } finally { Pop-Location }
}
$unpacked = "$release/win-unpacked/VISIONFORGE 3.exe"
$fv = (Get-Item $unpacked).VersionInfo.FileVersion
if ($fv -ne $version.fileVersion) { throw "FileVersion salah: $fv" }
Run-Smoke $unpacked 'packaged'
foreach ($name in @('VFPlain','VF With Spaces')) {
 $destination = Join-Path $env:TEMP $name
 if (Test-Path $destination) { throw 'Destinasi ujian sedia ada; jangan overwrite' }
 $process = Start-Process -FilePath $setup -ArgumentList "/S /D=$destination" -Wait -PassThru
 if ($process.ExitCode -ne 0) { throw 'Silent install gagal' }
 $exe = Join-Path $destination 'VISIONFORGE 3.exe'
 if (!(Test-Path $exe)) { throw 'Installed app tiada' }
 Run-Smoke $exe $name.Replace(' ','-')
 $uninstaller = Get-ChildItem $destination -Filter '*Uninstall*.exe' | Select-Object -First 1
 if (!$uninstaller) { throw 'Uninstaller tiada' }
 $process = Start-Process -FilePath $uninstaller.FullName -ArgumentList '/S' -Wait -PassThru
 if ($process.ExitCode -ne 0) { throw 'Silent uninstall gagal' }
 Start-Sleep -Seconds 3
 if (Test-Path $exe) { throw 'Uninstall tidak membuang executable' }
}
# Portable launcher memerlukan child-process handoff; guna self-test persekitaran di bawah.
$env:VF_PORTABLE_SELF_TEST = "$root/artifacts/desktop/portable-self-test.json"
$p = Start-Process -FilePath $portable -PassThru
$deadline = (Get-Date).AddMinutes(2)
while (!(Test-Path $env:VF_PORTABLE_SELF_TEST) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 500 }
if (!(Test-Path $env:VF_PORTABLE_SELF_TEST)) { throw 'Portable self-test tamat masa' }
$result = Get-Content $env:VF_PORTABLE_SELF_TEST | ConvertFrom-Json
if ($result.status -ne 'PASS') { throw 'Portable self-test gagal' }
@{ status='PASS';fileVersion=$fv;checks=@('packaged app','NSIS spaces','NSIS plain','silent uninstall','portable') } | ConvertTo-Json | Set-Content "$release/windows-tests.json"
