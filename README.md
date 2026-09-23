# Flatpak Manager Pro

A sleek, lightweight, and user-friendly bulk uninstaller for Flatpak applications, specifically optimized for Bazzite, Steam Deck (SteamOS), and other immutable or traditional Linux desktop environments. 

Built using Python 3 and PyQt6, **Flatpak Manager Pro** automatically detects your system language (supporting Dutch and English) and allows you to thoroughly clean up multiple applications along with their leftover user data and unused runtimes in just a few clicks.

## 🌟 Features

* **Bulk Uninstallation:** Select multiple applications using checkboxes and remove them all at once.
* **Thorough Cleanup:** Automatically deletes user configuration data (`--delete-data`) and prunes unused system runtimes (`--unused`) to free up valuable SSD space.
* **Environment Detection:** Clearly distinguishes between **🖥️ SYSTEM** (full PC) and **👤 USER** (isolated user profile) installations.
* **Automatic Localization:** Automatically switches interface language between English and Dutch based on your system's locale settings.
* **Flathub Ready:** Sandboxed configuration utilizing secure host-spawning mechanisms to communicate safely with your native package manager.

## 📸 Screenshots

*(To add a screenshot, upload an image named `screenshot.png` to your repository and uncomment the line below)*
<!-- ![Flatpak Manager Pro Interface](screenshot.png) -->

## 🔧 Installation & Build Instructions

Since Flatpak Manager Pro is built as a native Flatpak application, you can easily build and install it locally using `flatpak-builder`.

### Prerequisites

Ensure you have `flatpak` and `flatpak-builder` installed on your Linux distribution. On Bazzite or SteamOS, these are included out of the box.

### Building from Source

1. Clone this repository to your desktop or project directory:
   ```bash
   cd ~/Desktop
   git clone https://github.com
   cd Flatpak-Uninstaller
   ```

2. Clear out any previous build caches to ensure a clean slate:
   ```bash
   rm -rf build-dir .flatpak-builder local-repo
   ```

3. Build and install the application locally into your user profile:
   ```bash
   flatpak run org.flatpak.Builder --user --install --force-clean build-dir org.bazzite.FlatpakManager.json
   ```

4. *(Optional)* Refresh your desktop shell (KDE Plasma) to force the new round icon to display immediately in your application menu:
   ```bash
   kquitapp5 plasmashell && kstart5 plasmashell
   ```

## 🛠️ Sandbox Permissions Explained

This application runs securely inside a Flatpak sandbox but safely bypasses it for package management via the following defined parameters inside the manifest:
* `--filesystem=host`: Required to accurately scan system configurations.
* `flatpak-spawn --host`: Used internally to safely execute native CLI tasks (`flatpak list` and `flatpak uninstall`) on the host system without compromising absolute desktop security.

## 📄 License

This project is licensed under the GPL-3.0 License - see the source files for full copyright details.

## 👤 Author

Developed with ❤️ by [LionheartTim](https://github.com). Feel free to submit an issue or pull request if you want to contribute to future feature releases!
