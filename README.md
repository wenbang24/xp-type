# XP-type
A typing test app for Windows XP (technically cross platform but designed for XP)

## Installing
Download the latest release from the [releases page](https://github.com/wenbang24/xp-type/releases)

## Building
This guide is intended for Windows XP. Change versions accordingly for other operating systems.
1. Install Python 3.4
2. Install PyQt5.6 (installer available [here](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/))
    - At this point you can run with `python XPType.py` to test the app, continue if you want a standalone executable
3. Install PyInstaller 3.2
4. Download the source code from this repository
5. Open a command prompt in the source code directory
6. Run the command `pyinstaller XPType.spec`
    - The spec file is currently configured to create a standalone executable. If you want a different configuration, edit the spec file accordingly.
7. The executable will be created in the `dist` directory

## Credits
List of words acquired from [here](https://www.ef-australia.com.au/english-resources/english-vocabulary/top-1000-words/)
