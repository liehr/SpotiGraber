import threading

from termcolor import cprint, colored

import SpotiWave
import SpotiColor


def run_spotiwave():
    try:
        SpotiWave.start_wave()
    except Exception as e:
        print(f"An error occurred in SpotiWave: {e}")


def run_spoticolor():
    try:
        SpotiColor.start_color()
    except Exception as e:
        print(f"An error occurred in SpotiColor: {e}")


def start_program():
    try:
        wave_thread = threading.Thread(target=run_spotiwave)
        color_thread = threading.Thread(target=run_spoticolor)

        wave_thread.start()
        color_thread.start()

        wave_thread.join()
        color_thread.join()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


def color_wave():
    ascii_art = """
  ,----..             ,--,                                .---.                             
 /   /   \          ,--.'|                               /. ./|                             
|   :     :  ,---.  |  | :     ,---.    __  ,-.      .--'.  ' ;                             
.   |  ;. / '   ,'\ :  : '    '   ,'\ ,' ,'/ /|     /__./ \ : |               .---.         
.   ; /--` /   /   ||  ' |   /   /   |'  | |' | .--'.  '   \' .  ,--.--.    /.  ./|  ,---.  
;   | ;   .   ; ,. :'  | |  .   ; ,. :|  |   ,'/___/ \ |    ' ' /       \ .-' . ' | /     \ 
|   : |   '   | |: :|  | :  '   | |: :'  :  /  ;   \  \;      :.--.  .-. /___/ \: |/    /  |
.   | '___'   | .; :'  : |__'   | .; :|  | '    \   ;  `      | \__\/: . .   \  ' .    ' / |
'   ; : .'|   :    ||  | '.'|   :    |;  : |     .   \    .\  ; ," .--.; |\   \   '   ;   /|
'   | '/  :\   \  / ;  :    ;\   \  / |  , ;      \   \   ' \ |/  /  ,.  | \   \  '   |  / |
|   :    /  `----'  |  ,   /  `----'   ---'        :   '  |--";  :   .'   \ \   \ |   :    |
 \   \ .'            ---`-'                         \   \ ;   |  ,     .-./  '---" \   \  / 
  `---`                                              '---"     `--`---'             `----'  
"""
    cprint(ascii_art, "red", attrs=["bold"])


if __name__ == "__main__":
    color_wave()
    start_program()
