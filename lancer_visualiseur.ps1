Write-Host "Demarrage du visualiseur JETBOAT..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Ouvrez http://localhost:8000 dans votre navigateur" -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Yellow
Write-Host ""
python -m http.server 8000
