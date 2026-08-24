[app]

title = GheymatYar
package.name = gheymatyar
package.domain = org.gheymatyar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json,ico,webp

version = 1.0

# --------------------------------------------------
# Python / Kivy
# --------------------------------------------------

requirements = python3,kivy,pyjnius

# --------------------------------------------------
# Display
# --------------------------------------------------

orientation = portrait

fullscreen = 0

# --------------------------------------------------
# Android
# --------------------------------------------------

android.api = 35
android.minapi = 24

android.ndk = 27c
android.ndk_api = 24

android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_androidx = True

# --------------------------------------------------
# Permissions
# --------------------------------------------------

android.permissions = INTERNET,ACCESS_NETWORK_STATE

# --------------------------------------------------
# Python-for-Android
# --------------------------------------------------

p4a.branch = master

# --------------------------------------------------
# Build
# --------------------------------------------------

log_level = 2

# --------------------------------------------------
# Presplash / Icon
# --------------------------------------------------

# اگر آیکون پروژه داری، این خط را فعال کن:
# icon.filename = %(source.dir)s/assets/icon.png

# اگر presplash داری، این خط را فعال کن:
# presplash.filename = %(source.dir)s/assets/presplash.png
