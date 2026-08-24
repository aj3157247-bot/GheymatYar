[app]

title = قیمت‌یار
package.name = gheymatyar
package.domain = org.gheymatyar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json

version = 1.0

requirements = python3,kivy==2.3.1,arabic-reshaper==3.0.0,python-bidi==0.6.6

orientation = portrait

fullscreen = 0

android.api = 35
android.minapi = 24
android.ndk = 27c
android.ndk_api = 24
android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_androidx = True

android.permissions = INTERNET

p4a.branch = master

log_level = 2
