# AsciiAtrMaker app

<div align="center">
  <img width="4400" height="2474" alt="logo_ascii" src="https://github.com/user-attachments/assets/617eb892-0f2f-4eb4-b551-9eb16075b7b4" />
</div>

![Python](https://img.shields.io/badge/Python-3.10+-548af7?style=for-the-badge)
![Flet](https://img.shields.io/badge/Flet-0.80.0+-ee3167?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-12.0.0+-b43879?style=for-the-badge)

![Android](https://img.shields.io/badge/Android-2ea965?style=for-the-badge&logo=android&logoColor=white)
![IOS](https://img.shields.io/badge/IOS-000000?style=for-the-badge&logo=ios&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white&style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black&style=for-the-badge)
![Windows](https://custom-icon-badges.demolab.com/badge/Windows-0078d4?style=for-the-badge&logo=windows-11&logoColor=white)

## Installing

```
pip install -r requirements.txt
```

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://docs.flet.dev/).

## Build the app (start as administrator only)

### Platform matrix

The following matrix shows which OS you should run `flet build` command on in order to build a package for specific platform:

<table>
  <tr>
    <th rowspan="2">Run on</th>
    <th colspan="6" style="text-align: center;">Target Platform</th>
  </tr>
  <tr>
    <th>Android</th>
    <th>iOS</th>
    <th>macOS</th>
    <th>Linux</th>
    <th>Windows</th>
    <th>Web</th>
  </tr>
  <tr>
    <td>macOS</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;">✅</td>
  </tr>
  <tr>
    <td>Windows</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;">✅ (WSL)</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;">✅</td>
  </tr>
  <tr>
    <td>Linux</td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;">✅</td>
    <td style="text-align: center;"></td>
    <td style="text-align: center;">✅</td>
  </tr>
</table>

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://docs.flet.dev/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://docs.flet.dev/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://docs.flet.dev/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://docs.flet.dev/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://docs.flet.dev/publish/windows/).
