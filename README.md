# Bazzite Flatpak Manager Pro 🚀

Een krachtige, gestroomlijnde en gebruiksvriendelijke bulk-deïnstalleerder voor Flatpak-applicaties. Specifiek geoptimaliseerd voor Bazzite, Steam Deck (SteamOS) en andere immutable of traditionele Linux-desktopomgevingen. [3]

Gebouwd met Python 3 en PyQt6. **Flatpak Manager Pro** detecteert automatisch je systeemtaal (ondersteunt Nederlands en Engels) en stelt je in staat om met een paar klikken grondig meerdere applicaties te verwijderen, inclusief alle bijbehorende verborgen gebruikersdata en ongebruikte runtimes. [3]

## 🌟 Functionaliteiten

*   **Bulk-deïnstalleerder:** Selecteer meerdere applicaties tegelijk via handige selectievakjes om ze in één keer te wissen. [3]
*   **Grondige Opschoning:** Verwijdert automatisch alle configuratie- en cachebestanden (`--delete-data`) en schoont ongebruikte systeembasissen op (`--unused`) om kostbare SSD-ruimte vrij te maken. [3]
*   **Geavanceerde Metadata (Discover-stijl):** Klap een applicatie live uit om direct de schijfgrootte van de gebruikersdata, branch-informatie, architectuur, herkomst en de exacte commit-hashes te bekijken.
*   **Omgevingsdetectie:** Maakt een helder visueel onderscheid tussen **🖥️ SYSTEM** (volledige pc) en **👤 USER** (geïsoleerd gebruikersprofiel) installaties. [3]
*   **Automatische Systeemtaal:** De interface schakelt automatisch tussen Engels en Nederlands op basis van de actieve landinstellingen van je computer. [3]

## 📸 Screenshots

*(Om een screenshot toe te voegen, upload een afbeelding genaamd `screenshot.png` naar je repository en haal de commentaartekens hieronder weg)* [3]
<!-- ![Flatpak Manager Pro Interface](screenshot.png) -->

## 🔧 Installatie & Bouwinstructies

Omdat Bazzite Flatpak Manager Pro is gebouwd als een native Flatpak-applicatie, kun je deze eenvoudig lokaal compileren en installeren met `flatpak-builder`. [3]

### Benodigdheden

Zorg ervoor dat `flatpak` en `flatpak-builder` aanwezig zijn op je Linux-distributie. Op Bazzite en SteamOS is dit standaard al out-of-the-box geïnstalleerd. [3]

### Optie 1: Compileren vanaf de Broncode (Ontwikkelaars)

1.  Kloon deze repository naar je bureaublad of projectmap: [3]
    ```bash
    cd ~/Desktop
    git clone https://github.com
    cd flatpak-manager-pro
    ```
2.  Wis eventuele oude bouwcaches voor een gegarandeerd schone start: [3]
    ```bash
    rm -rf build-dir .flatpak-builder local-repo
    ```
3.  Bouw en installeer de applicatie lokaal binnen je gebruikersprofiel: [3]
    ```bash
    flatpak run org.flatpak.Builder --user --install --force-clean build-dir org.bazzite.FlatpakManager.json
    ```
4.  Registreer de snelkoppeling en ververs je startmenu (KDE Plasma 6) om het ronde logo direct live te activeren: [3]
    ```bash
    mkdir -p ~/.local/share/applications
    cp /var/lib/flatpak/app/org.bazzite.FlatpakManager/current/active/export/share/applications/org.bazzite.FlatpakManager.desktop ~/.local/share/applications/ 2>/dev/null || cp ~/.local/share/flatpak/app/org.bazzite.FlatpakManager/current/active/export/share/applications/org.bazzite.FlatpakManager.desktop ~/.local/share/applications/ 2>/dev/null
    
    rm -rf ~/.cache/icoon-cache ~/.cache/icon-cache.kcache
    kbuildsycoca6 --noincremental
    kquitapp6 plasmashell && kstart6 plasmashell
    ```

### Optie 2: Installeren via het Universele `.flatpak` Bestand (Gebruikers)

Als je de app als kant-and-klaar pakket hebt gedownload van de GitHub Releases-pagina, kun je de standalone installer direct uitvoeren en installeren in Discover:

```bash
flatpak install --user BazziteFlatpakManagerPro.flatpak
```

## 🛠️ Sandbox-rechten Toegelicht

Deze applicatie draait veilig binnen een Flatpak-sandbox, maar communiceert op een verantwoorde manier met het basissysteem voor pakketbeheer via de volgende parameters in het manifest: [3]
*   `--filesystem=host`: Vereist om de gebruikersmappen accuraat te scannen op schijfgrootte. [3]
*   `flatpak-spawn --host`: Wordt intern gebruikt om de native CLI-taken (`flatpak list` en `flatpak uninstall`) veilig op de host uit te voeren zonder de algehele desktopbeveiliging in gevaar te brengen. [3]

## 📄 Licentie

Dit project is gelicentieerd onder de GPL-3.0 Licentie - zie de broncodebestanden voor volledige auteursrechtelijke details. [3]

## 👤 Auteur

Ontwikkeld met ❤️ door [LionheartTim](https://github.com). Voel je vrij om een issue of pull-request in te dienen als je wilt bijdragen aan toekomstige functionaliteiten! [3]
