from dotenv import load_dotenv
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QComboBox, QLineEdit, QMessageBox, QLabel, QDialog, QFrame
from PyQt5.QtGui import QMovie, QIcon, QPalette, QColor, QFont
from src.prod.script import process_aging_report

def main():
    load_dotenv()

    # app init
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Aging Ticket Report Modifier')
    window.setFixedWidth(700)
    layout = QVBoxLayout()
    window.setWindowIcon(QIcon('../assets/logo.png'))

    # styling
    app.setStyle('fusion')
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor("#09396C"))
    palette.setColor(QPalette.Button, QColor("#879EC3"))
    palette.setColor(QPalette.WindowText, QColor("#ffffff"))
    app.setFont(QFont("slab serif", 10, QFont.Bold))
    app.setPalette(palette)

    # i/o config
    show_input = True
    input_is_file = True
    show_output = True
    output_is_file = False
    show_run_mode = False

    button_font = QFont("slab serif", 9)

    if show_input:
        if input_is_file:
            input_label = QLabel('Input File')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.setFont(button_font)
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)
        else:
            input_label = QLabel('Input Directory')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.setFont(button_font)
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getExistingDirectory()))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)

    if show_output:
        if output_is_file:
            output_label = QLabel('Output File')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
            output_button.setFont(button_font)
            output_button.clicked.connect(lambda: output_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(output_label)
            layout.addWidget(output_field)
            layout.addWidget(output_button)
        else:
            output_label = QLabel('Output Directory')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
            output_button.setFont(button_font)
            output_button.clicked.connect(lambda: output_field.setText(QFileDialog.getExistingDirectory()))
            layout.addWidget(output_label)
            layout.addWidget(output_field)
            layout.addWidget(output_button)

    if show_run_mode:
        mode_label = QLabel('Run Mode')
        mode_combo = QComboBox()
        mode_combo.addItems(['Production', 'SB', 'Authorization'])
        layout.addWidget(mode_label)
        layout.addWidget(mode_combo)

    layout.addSpacing(10)
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(line)
    layout.addSpacing(10)
    run_button = QPushButton('Run')
    run_button.setFont(button_font)
    run_button.setStyleSheet("background-color: #21314d; color: #ffffff")
    exit_button = QPushButton('Exit')
    exit_button.setFont(button_font)
    exit_button.setStyleSheet("background-color: #cc4628; color: #ffffff")
    layout.addWidget(run_button)
    layout.addWidget(exit_button)

    loading_gif = QMovie("../assets/pacman-loading.gif")
    loading_dialog = QDialog(window)
    loading_label = QLabel(loading_dialog)
    loading_label.setMovie(loading_gif)
    loading_dialog.setLayout(QVBoxLayout())
    loading_dialog.layout().addWidget(loading_label)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    def run_script():
        input_path, output_path, mode = None, None, None
        if show_input:
            input_path = input_field.text()
        if show_output:
            output_path = output_field.text()
        if show_run_mode:
            mode = mode_combo.currentText()

        if (show_input and not input_path) or (show_output and not output_path) or (show_run_mode and not mode):
            QMessageBox.warning(window, "Warning", "Please provide all required fields.")
            return

        if mode == "Production" or not show_run_mode:
            run_button.setEnabled(False)
            loading_dialog.show()
            loading_gif.start()
            process_aging_report(input_path, output_path)
            loading_gif.stop()
            loading_dialog.close()
            run_button.setEnabled(True)
            QMessageBox.information(window, "Information", "Script finished running")

    run_button.clicked.connect(run_script)
    exit_button.clicked.connect(lambda: window.close())

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
