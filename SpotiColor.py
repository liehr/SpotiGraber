import binascii
import os
import time

import imageio
import numpy as np
import scipy
from scipy.cluster import hierarchy
from PIL import Image
from termcolor import cprint
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ImageChangeHandler(FileSystemEventHandler):
    processing = False  # Flag to check if processing is in progress

    def on_modified(self, event):
        target_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'spotify_album_cover.png')
        if event.src_path == target_path and not self.processing:
            self.processing = True  # Set flag to True to prevent re-entry
            try:
                process_image(1, target_path)
                process_image(12, target_path)
            except Exception as e:
                cprint(f"Error processing image: {e}", "red", attrs=["bold"])
            finally:
                self.processing = False  # Reset flag after processing


def print_spotiwave():
    ascii_art = """
  .--.--.                           ___               ,----..             ,--,                     
 /  /    '. ,-.----.              ,--.'|_    ,--,    /   /   \          ,--.'|                     
|  :  /`. / \    /  \    ,---.    |  | :,' ,--.'|   |   :     :  ,---.  |  | :     ,---.    __  ,-.
;  |  |--`  |   :    |  '   ,'\   :  : ' : |  |,    .   |  ;. / '   ,'\ :  : '    '   ,'\ ,' ,'/ /|
|  :  ;_    |   | .\ : /   /   |.;__,'  /  `--'_    .   ; /--` /   /   ||  ' |   /   /   |'  | |' |
 \  \    `. .   : |: |.   ; ,. :|  |   |   ,' ,'|   ;   | ;   .   ; ,. :'  | |  .   ; ,. :|  |   ,'
  `----.   \|   |  \ :'   | |: ::__,'| :   '  | |   |   : |   '   | |: :|  | :  '   | |: :'  :  /  
  __ \  \  ||   : .  |'   | .; :  '  : |__ |  | :   .   | '___'   | .; :'  : |__'   | .; :|  | '   
 /  /`--'  /:     |`-'|   :    |  |  | '.'|'  : |__ '   ; : .'|   :    ||  | '.'|   :    |;  : |   
'--'.     / :   : :    \   \  /   ;  :    ;|  | '.'|'   | '/  :\   \  / ;  :    ;\   \  / |  , ;   
  `--'---'  |   | :     `----'    |  ,   / ;  :    ;|   :    /  `----'  |  ,   /  `----'   ---'    
            `---'.|                ---`-'  |  ,   /  \   \ .'            ---`-'                    
              `---`                         ---`-'    `---`                                        
"""
    cprint(ascii_art, "green", attrs=["bold"])


def process_image(cluster, image_path):
    NUM_CLUSTERS = cluster

    try:
        cprint('Reading image...', "yellow")
        im = Image.open(image_path)
        im = im.resize((1200, 1200))  # Resize to reduce processing time

        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.prod(shape[:2]), shape[2]).astype(float)

        cprint('Finding clusters...', "yellow")
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        cprint(f'Cluster centres:\n{codes}', "yellow")

        vecs, dist = scipy.cluster.vq.vq(ar, codes)  # Assign codes
        counts, _ = np.histogram(vecs, bins=len(codes))  # Count occurrences

        index_max = np.argmax(counts)  # Find the most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        cprint(f'Most frequent colour is {peak} (# {colour})', "yellow")

        # Save image using only the N most common colours
        save_clustered_image(ar, vecs, codes, shape, f'clustered_{NUM_CLUSTERS}.png')
    except Exception as e:
        cprint(f"Error during image processing: {e}", "red", attrs=["bold"])


def save_clustered_image(ar, vecs, codes, shape, filename):
    try:
        clustered_array = ar.copy()
        for i, code in enumerate(codes):
            clustered_array[np.where(vecs == i)] = code

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', filename)
        imageio.imwrite(desktop_path, clustered_array.reshape(*shape).astype(np.uint8))
        cprint(f'Saved clustered image to {desktop_path}', "green", attrs=["bold"])
    except Exception as e:
        cprint(f"Error saving clustered image: {e}", "red", attrs=["bold"])


def start_color():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    event_handler = ImageChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=desktop_path, recursive=False)
    observer.start()

    try:
        cprint("Monitoring for changes on the desktop...", "green", attrs=["bold"])
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cprint("Stopping observer...", "red", attrs=["bold"])
        observer.stop()
    observer.join()
