# AsciiAtrMaker app

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
