[app]

# Nome do app exibido no celular
title = Inventario TI

# Nome do pacote e dominio  ->  org.empresa.inventarioti
package.name = inventarioti
package.domain = org.empresa

# Onde estao os fontes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,csv

version = 0.1

# Bibliotecas Python necessarias
requirements = python3,kivy,pyjnius

# Tela em retrato
orientation = portrait

# Icone (opcional). Deixe comentado se nao tiver o arquivo.
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 0

[app:android]

# Permissoes (mesmas do APK original)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_PHONE_STATE

# Versoes de SDK/Build
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

# Aceitar automaticamente as licencas do SDK
android.accept_sdk_license = True
