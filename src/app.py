from dotenv import load_dotenv
import threading
import subprocess
import PySimpleGUI as sg

def run_script(script_path):
    subprocess.run(["python", script_path], check=True)

def main():
    load_dotenv()

    sg.theme('DarkBlue')

    show_input = True
    input_is_file = True
    show_output = True
    output_is_file = False
    show_run_mode = True

    layout = [[sg.Text('Select input and output', font=("Sans Serif", 14), justification='center')]]

    if show_input:
        if input_is_file:
            layout.append([sg.Text('Input File', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FileBrowse(font=("Sans Serif", 12))])
        else:
            layout.append([sg.Text('Input Directory', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FolderBrowse(font=("Sans Serif", 12))])

    if show_output:
        if output_is_file:
            layout.append([sg.Text('Output File', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FileBrowse(font=("Sans Serif", 12))])
        else:
            layout.append([sg.Text('Output Directory', size=(8, 1), font=("Sans Serif", 12)), sg.Input(), sg.FolderBrowse(font=("Sans Serif", 12))])

    if show_run_mode:
        layout.extend([[sg.Text('Run Mode', size=(8, 1), font=("Sans Serif", 12)), sg.Combo(['Production', 'SB', 'Authorization'], size=(20, 1), font=("Sans Serif", 12))]])

    layout.append([sg.Submit(button_color=('white', 'green'), button_text='Run', font=("Sans Serif", 12)), sg.Cancel(button_color=('white', 'red'), button_text='Exit', font=("Sans Serif", 12))])

    window = sg.Window('Script Runner', layout)

    while True:
        event, values = window.read()

        if event == 'Run':
            input_path, output_path, mode = None, None, None
            if show_input:
                input_path = values[0]
            if show_output:
                output_path = values[1]
            if show_run_mode:
                mode = values[2]

            if (show_input and not input_path) or (show_output and not output_path) or (show_run_mode and not mode):
                sg.Popup("Please provide all required fields.", font=("Sans Serif", 12))
                continue

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
                sg.Popup("Please select a valid run mode.", font=("Sans Serif", 12))
                continue
            
            window.FindElement('Run').Update(disabled=True)
            threading.Thread(target=run_script, args=(script_path,), daemon=True).start()
            while threading.active_count() > 1:
                sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
            sg.PopupAnimated(None)
            window.FindElement('Run').Update(disabled=False)
            sg.Popup("Script finished running", font=("Sans Serif", 12))
            window.close()
            break

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

    window.close()

if __name__ == "__main__":
    main()
