# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath('src'))

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/svt_app/templates', 'svt_app/templates'),
        ('src/svt_app/static', 'svt_app/static'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'waitress',
        'flask',
        'jinja2',
        'werkzeug',
        'svt_app.controllers.game_controller',
        'svt_app.services.question_service'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SVT Reproduction Animaux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 