# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath('src'))

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/Data/fill_the_blanks', 'assets/Data/fill_the_blanks'),
        ('assets/Data/image_matching', 'assets/Data/image_matching'),
        ('src/svt_app/templates', 'svt_app/templates'),
        ('src/svt_app/static', 'svt_app/static'),
    ],
    hiddenimports=[
        'waitress',
        'flask',
        'jinja2',
        'werkzeug',
        'svt_app.controllers.game_controller',
        'svt_app.services.question_service',
        'svt_app.models.question'
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
    name='Révijouer',
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