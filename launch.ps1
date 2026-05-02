$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Start-Process powershell -ArgumentList "-NoProfile", "-Command", "cd '$scriptDir'; python pet_window.py; Read-Host 'Press Enter to close'"
