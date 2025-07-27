# -*- mode: python -*-

block_cipher = None


a = Analysis(['widget.py', 'MainWindow.py', 'SettingsDialog.py'],
             pathex=['C:\\Documents and Settings\\All Users\\Documents\\XPType'],
             binaries=[],
             datas=[('words.txt', '.')],
             hiddenimports=['sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='XPType',
          debug=False,
          strip=False,
          upx=True,
          console=False )
