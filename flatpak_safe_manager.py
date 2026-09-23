#!/usr/bin/env python3
import sys
import subprocess
import os
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QMessageBox, QHeaderView, QProgressBar, QLabel)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QLocale
from PyQt6.QtGui import QIcon

PROJECT_DIR = "/home/Tim/Desktop/Flatpak uninstaller"

def run_cmd(cmd_list):
    """
    Voert commando's uit buiten de sandbox op het echte basissysteem (de host).
    Zorgt ervoor dat de Flatpak 'flatpak list' en 'flatpak uninstall' kan aanroepen.
    """
    try:
        spawn_cmd = ["flatpak-spawn", "--host"] + cmd_list
        result = subprocess.run(spawn_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

# Vertaal-database voor de automatische taaldetectie
VERTALINGEN = {
    "nl": {
        "titel": "Bazzite Flatpak Manager Pro",
        "info": "<b>Selecteer één of meerdere apps</b> via de selectievakjes en klik onderin op Verwijderen.",
        "kolom_kies": "Kies",
        "kolom_naam": "Applicatienaam",
        "kolom_id": "Applicatie ID",
        "kolom_type": "Type (Locatie)",
        "btn_sluiten": "Sluiten",
        "btn_verwijderen": "Geselecteerde verwijderen",
        "fout_geen_selectie": "Je hebt geen applicaties geselecteerd!",
        "prompt_system": "<b>Let op:</b> Je hebt <b>{}</b> app(s) geselecteerd, waaronder SYSTEM-apps.<br><br>Weet je zeker dat je deze en alle bijbehorende gebruikersdata permanent wilt wissen?",
        "prompt_user": "Weet je zeker dat je de <b>{}</b> geselecteerde USER app(s) and alle bijbehorende gebruikersdata grondig wilt wissen?",
        "bevestig_titel": "Verwijdering Bevestigen",
        "succes_titel": "Succes",
        "succes_tekst": "De geselecteerde applicaties zijn succesvol verwijderd!",
        "status_verwijderen": "({}/{}) Verwijderen van {}...",
        "status_scannen": "Systeem scannen op ongebruikte restbestanden (runtimes)...",
        "status_voltooid": "Voltooid!",
        "type_system": "🖥️ SYSTEM (Hele PC)",
        "type_user": "👤 USER (Alleen jij)"
    },
    "en": {
        "titel": "Bazzite Flatpak Manager Pro",
        "info": "<b>Select one or more apps</b> via the checkboxes and click Uninstall below.",
        "kolom_kies": "Select",
        "kolom_naam": "Application Name",
        "kolom_id": "Application ID",
        "kolom_type": "Type (Location)",
        "btn_sluiten": "Close",
        "btn_verwijderen": "Uninstall Selected",
        "fout_geen_selectie": "You have not selected any applications!",
        "prompt_system": "<b>Warning:</b> You selected <b>{}</b> app(s), including SYSTEM apps.<br><br>Are you sure you want to permanently delete these and all associated user data?",
        "prompt_user": "Are you sure you want to thoroughly delete the <b>{}</b> selected USER app(s) and all associated user data?",
        "bevestig_titel": "Confirm Destruction",
        "succes_titel": "Success",
        "succes_tekst": "The selected applications have been successfully removed!",
        "status_verwijderen": "({}/{}) Uninstalling {}...",
        "status_scannen": "Scanning system for unused leftover files (runtimes)...",
        "status_voltooid": "Completed!",
        "type_system": "🖥️ SYSTEM (Full PC)",
        "type_user": "👤 USER (Just you)"
    }
}

class UninstallThread(QThread):
    """Achtergrond-thread zodat de GUI vloeiend blijft lopen tijdens het de-installeren."""
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal()

    def __init__(self, gekozen_apps, taal_dict):
        super().__init__()
        self.gekozen_apps = gekozen_apps
        self.t = taal_dict

    def run(self):
        totaal = len(self.gekozen_apps)
        for i, (app_id, is_system) in enumerate(self.gekozen_apps):
            procent = int((i / totaal) * 100)
            txt = self.t["status_verwijderen"].format(i+1, totaal, app_id)
            self.progress_signal.emit(procent, txt)

            scope_flag = "--system" if is_system else "--user"
            run_cmd(["flatpak", "uninstall", scope_flag, "-y", "--delete-data", app_id])
            time.sleep(0.2)

        self.progress_signal.emit(95, self.t["status_scannen"])
        run_cmd(["flatpak", "uninstall", "-y", "--unused"])
        time.sleep(0.3)

        self.progress_signal.emit(100, self.t["status_voltooid"])
        self.finished_signal.emit()
class FlatpakManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        systeem_taal = QLocale.system().name()[:2]
        self.t = VERTALINGEN.get(systeem_taal, VERTALINGEN["en"])

        self.setWindowTitle(self.t["titel"])
        self.resize(850, 550)

        # Laad je nieuwe logo in via het geregistreerde Flatpak-thema
        self.setWindowIcon(QIcon.fromTheme("org.bazzite.FlatpakManager"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.info_label = QLabel(self.t["info"])
        self.layout.addWidget(self.info_label)

        # Tabel opbouwen
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            self.t["kolom_kies"], self.t["kolom_naam"], self.t["kolom_id"], self.t["kolom_type"]
        ])

        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.layout.addWidget(self.table)

        self.progress_label = QLabel("")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)

        # Knoppenbalk onderin
        self.btn_layout = QHBoxLayout()

        self.btn_close = QPushButton(self.t["btn_sluiten"])
        self.btn_close.clicked.connect(self.close)
        self.btn_layout.addWidget(self.btn_close)

        self.btn_layout.addStretch()

        self.credits_label = QLabel(
            "v1.0.0 | Made by <a href='https://github.com/LionheartTim' style='color: #3498db; text-decoration: none;'>LionheartTim</a>"
        )
        self.credits_label.setOpenExternalLinks(True)
        self.credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_layout.addWidget(self.credits_label)

        self.btn_layout.addStretch()

        self.btn_uninstall = QPushButton(self.t["btn_verwijderen"])
        self.btn_uninstall.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold;")
        self.btn_uninstall.clicked.connect(self.start_uninstall)
        self.btn_layout.addWidget(self.btn_uninstall)

        self.layout.addLayout(self.btn_layout)

        self.laad_flatpaks()

    def laad_flatpaks(self):
        """Scant het systeem live via de host en gebruikt jouw exacte werkende splitsing."""
        self.table.setRowCount(0)
        raw_output = run_cmd(["flatpak", "list", "--app", "--columns=name,application,installation"])

        if not raw_output:
            return

        lines = raw_output.strip().split("\n")
        row = 0
        for line in lines:
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                self.table.insertRow(row)

                chk_item = QTableWidgetItem()
                chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                chk_item.setCheckState(Qt.CheckState.Unchecked)
                chk_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 0, chk_item)

                # HERSTELD: Dit zijn exact de elementen uit jouw 100% werkende code!
                naam_item = QTableWidgetItem(parts[0].strip())
                naam_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                naam_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 1, naam_item)

                id_item = QTableWidgetItem(parts[1].strip())
                id_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 2, id_item)

                type_label = self.t["type_system"] if parts[2].strip().lower() == "system" else self.t["type_user"]
                type_item = QTableWidgetItem(type_label)
                type_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                type_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 3, type_item)

                row += 1

    def start_uninstall(self):
        """Verzamelt de geselecteerde apps."""
        gekozen_apps = []
        bevat_system = False

        for row in range(self.table.rowCount()):
            chk_item = self.table.item(row, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                app_id = self.table.item(row, 2).text()
                is_system = "SYSTEM" in self.table.item(row, 3).text()
                gekozen_apps.append((app_id, is_system))
                if is_system:
                    bevat_system = True

        if not gekozen_apps:
            QMessageBox.information(self, "Info", self.t["fout_geen_selectie"])
            return

        aantal = len(gekozen_apps)
        prompt = (self.t["prompt_system"].format(aantal) if bevat_system else self.t["prompt_user"].format(aantal))

        bevestig = QMessageBox.question(self, "{}".format(self.t["bevestig_titel"]), prompt,
                                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if bevestig == QMessageBox.StandardButton.Ok:
            self.btn_uninstall.setEnabled(False)
            self.table.setEnabled(False)
            self.progress_bar.setVisible(True)

            self.thread = UninstallThread(gekozen_apps, self.t)
            self.thread.progress_signal.connect(self.update_progress)
            self.thread.finished_signal.connect(self.uninstall_klaar)
            self.thread.start()

    def update_progress(self, procent, status_tekst):
        self.progress_bar.setValue(procent)
        self.progress_label.setText(status_tekst)

    def uninstall_klaar(self):
        QMessageBox.information(self, "{}".format(self.t["succes_titel"]), self.t["succes_tekst"])
        self.progress_bar.setVisible(False)
        self.progress_label.setText("")
        self.btn_uninstall.setEnabled(True)
        self.table.setEnabled(True)
        self.laad_flatpaks()

if __name__ == "__main__":
    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)
    os.chdir(PROJECT_DIR)

    import ctypes
    myappid = "org.bazzite.flatpakmanagerpro.1.0"
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass

    app = QApplication(sys.argv)
    window = FlatpakManagerApp()
    window.show()
    sys.exit(app.exec())
