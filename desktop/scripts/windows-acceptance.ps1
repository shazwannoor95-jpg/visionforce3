$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$version = Get-Content "$root/version.json" | ConvertFrom-Json
$release = (Get-Content "$root/desktop/release/latest-build.json" | ConvertFrom-Json).directory
$setup = Join-Path $release "VISIONFORGE-3-$($version.display)-Setup-x64.exe"
$portable = Join-Path $release "VISIONFORGE-3-$($version.display)-Portable-x64.exe"
$report = @{status='BUILDING';checks=@();signatures=@{}}
function Save-Report { $report | ConvertTo-Json -Depth 10 | Set-Content "$release/windows-tests.json" }
function Run-Smoke($exe, $name) {
 $env:VF_TEST_APP_EXE = $exe
 $env:VF_SMOKE_REPORT = "$root/artifacts/desktop/$name"
 Push-Location "$root/desktop"
 try { node tests/electron-smoke.cjs; if ($LASTEXITCODE -ne 0) { throw "Smoke $name gagal" } } finally { Pop-Location }
}
try {
 foreach ($f in @($setup,$portable)) {
  if (!(Test-Path $f)) { throw "Artifak tiada: $f" }
  $report.signatures[(Split-Path $f -Leaf)] = (Get-AuthenticodeSignature $f).Status.ToString()
 }
 $unpacked = "$release/win-unpacked/VISIONFORGE 3.exe"
 $fv = (Get-Item $unpacked).VersionInfo.FileVersion
 if ($fv -ne $version.fileVersion) { throw "FileVersion salah: $fv" }
 $report.fileVersion=$fv
 Run-Smoke $unpacked 'packaged'
 $report.checks += 'packaged app'; Save-Report
 $sentinelRoot=Join-Path $env:APPDATA 'VISIONFORGE3'
 New-Item -ItemType Directory -Force $sentinelRoot | Out-Null
 $sentinel=Join-Path $sentinelRoot ('ci-preserve-'+[guid]::NewGuid().ToString()+'.txt')
 [IO.File]::WriteAllText($sentinel,'VISIONFORGE3-user-data-42')
 foreach ($name in @('VFPlain','VF With Spaces')) {
  $destination = Join-Path $env:TEMP $name
  if (Test-Path $destination) { throw 'Destinasi ujian sedia ada; jangan overwrite' }
  # StdUtils.GetParameter dalam template electron-builder memerlukan nilai satu argumen.
  $arguments = '/S /D="{0}"' -f $destination
  Write-Host "VF_INSTALL_REQUEST $arguments"
  $process = Start-Process -FilePath $setup -ArgumentList $arguments -Wait -PassThru
  if ($process.ExitCode -ne 0) { throw 'Silent install gagal' }
  $exe = Join-Path $destination 'VISIONFORGE 3.exe'
  if (!(Test-Path $exe)) {
   $locations=Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall' | Get-ItemProperty | Where-Object {$_.DisplayName -like 'VISIONFORGE 3*'} | Select-Object DisplayName,InstallLocation,UninstallString
   Write-Host ('VF_INSTALL_DIAGNOSTIC '+(@{requested=$destination;exitCode=$process.ExitCode;registry=$locations} | ConvertTo-Json -Compress -Depth 5))
   throw 'Installed app tiada di laluan yang diminta'
  }
  Run-Smoke $exe ($name.Replace(' ','-'))
  $report.checks += "installed app: $name"; Save-Report
  $uninstaller = Get-ChildItem $destination -Filter '*Uninstall*.exe' | Select-Object -First 1
  if (!$uninstaller) { throw 'Uninstaller tiada' }
  $process = Start-Process -FilePath $uninstaller.FullName -ArgumentList '/S' -Wait -PassThru
  if ($process.ExitCode -ne 0) { throw 'Silent uninstall gagal' }
  Start-Sleep -Seconds 3
  if (Test-Path $exe) { throw 'Uninstall tidak membuang executable' }
  if (!(Test-Path $sentinel) -or [IO.File]::ReadAllText($sentinel) -ne 'VISIONFORGE3-user-data-42') { throw 'Uninstall mengubah data pengguna' }
  $report.checks += "uninstall and preserve data: $name"; Save-Report
 }
 Remove-Item -LiteralPath $sentinel
 $env:VF_PORTABLE_SELF_TEST = "$root/artifacts/desktop/portable-self-test.json"
 if (Test-Path $env:VF_PORTABLE_SELF_TEST) { throw 'Bukti portable lama dijumpai; jangan guna semula' }
 $p = Start-Process -FilePath $portable -PassThru
 $deadline = (Get-Date).AddMinutes(2)
 while (!(Test-Path $env:VF_PORTABLE_SELF_TEST) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 500 }
 if (!(Test-Path $env:VF_PORTABLE_SELF_TEST)) { throw 'Portable self-test tamat masa' }
 $result = Get-Content $env:VF_PORTABLE_SELF_TEST | ConvertFrom-Json
 if ($result.status -ne 'PASS' -or $result.platform -ne 'win32') { throw 'Portable self-test gagal' }
 $report.checks += 'portable process and IPC'; $report.status='PASS'; Save-Report
} catch { $report.status='FAIL';$report.error=$_.Exception.Message;Save-Report;throw }
