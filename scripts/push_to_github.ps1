# Helper script: guide to install Git on Windows and push project to GitHub
# Usage: run in PowerShell as a normal user (not admin) after editing the repo URL below.

$repoUrl = 'https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПО.git' # <- replace this

Write-Host "1) Проверка наличия git"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git не найден. Предлагаю установить через winget (если доступен) или откройте https://git-scm.com/download/win"
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Установка git через winget..."
        winget install --id Git.Git -e --source winget
    } else {
        Write-Host "Пожалуйста скачайте и установите Git вручную: https://git-scm.com/download/win"
        return
    }
}

Write-Host "2) Настройка .gitignore"
if (-not (Test-Path .gitignore)) {
    @'
venv/
*.pyc
__pycache__/
db.sqlite3
.env
node_modules/
*.log
.vscode/
'@ > .gitignore
    Write-Host ".gitignore создан"
}

Write-Host "3) Инициализация и push"
cd (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)
# go to project root
$projectPath = "$(Get-Location)"
Write-Host "Текущая папка: $projectPath"

# init git if necessary
if (-not (Test-Path .git)) {
    git init
}

git add .
git commit -m "Initial commit: deploy-ready"

# set remote (user must replace $repoUrl)
if ($repoUrl -eq 'https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПО.git') {
    Write-Host "Пожалуйста замените переменную `\$repoUrl` в этом скрипте на URL вашего репозитория и запустите снова."
    return
}

git remote add origin $repoUrl
git branch -M main
git push -u origin main

Write-Host "Готово. Если push запросил авторизацию, используйте Git Credential Manager или Personal Access Token (PAT)."
