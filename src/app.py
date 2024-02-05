from dotenv import load_dotenv
import threading
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QComboBox, QLineEdit, QMessageBox, QProgressBar
from PyQt6.QtCore import Qt

def run_script(script_path, progress_callback):
    process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            progress_callback(output.strip())
    rc = process.poll()

def main():
    load_dotenv()

    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle('Script Runner')
    layout = QVBoxLayout()

    show_input = True
    input_is_file = True
    show_output = True
    output_is_file = False
    show_run_mode = True

    if show_input:
        if input_is_file:
            input_label = QLabel('Input File')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)
        else:
            input_label = QLabel('Input Directory')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getExistingDirectory()))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)

    if show_output:
        if output_is_file:
            output_label = QLabel('Output File')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
            output_button.clicked.connect(lambda: output_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(output_label)
            layout.addWidget(output_field)
            layout.addWidget(output_button)
        else:
            output_label = QLabel('Output Directory')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
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

    run_button = QPushButton('Run')
    exit_button = QPushButton('Exit')
    layout.addWidget(run_button)
    layout.addWidget(exit_button)

    progress_bar = QProgressBar()
    layout.addWidget(progress_bar)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    def update_progress_bar(value):
        progress_bar.setValue(int(value))

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

        with open("../.env", 'a') as env:
            if show_input:
                if input_is_file:
                    env.write(f"INPUT_FILE={input_path}\n")
                else:
                    env.write(f"INPUT_DIR={input_path}\n")
            if show_output:
                if output_is_file:
                    env.write(f"OUTPUT_FILE={output_path}\n")
                else:
                    env.write(f"OUTPUT_DIR={output_path}\n")
            if show_run_mode:
                env.write(f"RUN_MODE={mode}\n")

        if mode == "Production":
            script_path = "src/prod/script.py"
        elif mode == "SB":
            script_path = "src/sb/script.py"
        elif mode == "Authorization":
            script_path = "src/auth.py"
        else:
            QMessageBox.warning(window, "Warning", "Please select a valid run mode.")
            return

        run_button.setEnabled(False)
        threading.Thread(target=run_script, args=(script_path, update_progress_bar), daemon=True).start()
        while threading.active_count() > 1:
            QApplication.processEvents()
        run_button.setEnabled(True)
        QMessageBox.information(window, "Information", "Script finished running")
        window.close()

    run_button.clicked.connect(run_script)
    exit_button.clicked.connect(lambda: window.close())

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
