from dotenv import load_dotenv
import threading
import subprocess
import PySimpleGUI as sg

def run_script(script_path):
    subprocess.run(["python", script_path], check=True)

def main():
    load_dotenv()

    sg.theme('DarkAmber')

    layout = [[sg.Text('Select input file and output directory', font=("Sans Serif", 14), justification='center')],
               [sg.Text('Input File', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FileBrowse(font=("Sans Serif", 12))],
               [sg.Text('Output', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FolderBrowse(font=("Sans Serif", 12))],
               [sg.Text('Run Mode', size=(8, 1), font=("Sans Serif", 12)), sg.Combo(['Production', 'SB', 'Authorization'], size=(20, 1), font=("Sans Serif", 12))],
               [sg.Submit(button_color=('white', 'green'), button_text='Run', font=("Sans Serif", 12)), sg.Cancel(button_color=('white', 'red'), button_text='Exit', font=("Sans Serif", 12))]]

    window = sg.Window('Script Runner', layout)

    while True:
        event, values = window.read()

        if event == 'Run':
            input_file, output_dir, mode = values[0], values[1], values[2]

            if not input_file or not output_dir or not mode:
                sg.Popup("Please provide all required fields: Input File, Output Folder, and Run Mode.", font=("Sans Serif", 12))
                continue

            with open("../.env", 'a') as env:
                env.write(f"input_file='{input_file}'\n")
                env.write(f"output_dir='{output_dir}'\n")

            if mode == "Production":
                script_path = "src/prod/script.py"
            elif mode == "SB":
                script_path = "src/sb/script.py"
            elif mode == "Authorization":
                script_path = "src/auth.py"
            else:
                sg.Popup("Please select a valid run mode.", font=("Sans Serif", 12))
                continue
            
            window.FindElement('Run').Update(disabled=True)
            threading.Thread(target=run_script, args=(script_path,), daemon=True).start()
            while threading.active_count() > 1:
                sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
            sg.PopupAnimated(None)
            window.FindElement('Run').Update(disabled=False)
            sg.Popup("Script finished running.", font=("Sans Serif", 12))
            window.close()
            break

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

    window.close()

if __name__ == "__main__":
    main()

