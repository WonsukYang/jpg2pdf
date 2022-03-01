import os
import time
import shutil
from glob import glob
import subprocess as sp

import fire
from PIL import Image


DOWNLOAD_PATH = "/mnt/c/Users/USER/Downloads"


def is_created_within_hour(fpath: str) -> bool:
    current_time = time.time()
    modified_time = os.path.getmtime(fpath)
    return current_time - modified_time < 3600

def convert(dir_path: str, pdf_path: str):
    images = [
        Image.open(fname) for fname in sorted(glob(f"{dir_path}/*.jpg"))
    ]
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:] 
    )

def main(directory: str = DOWNLOAD_PATH):
    tmp_dir = os.path.join(directory, "tmp")
    n_created = 0
    for fname in glob(f"{directory}/*.zip"):
        if is_created_within_hour(fname):
            try:
                os.makedirs(tmp_dir, exist_ok=True)
                sp.run(["unzip", f"{fname}", "-d", f"{tmp_dir}"])
                pdf_path = os.path.join(directory,
                                        f"jpg2pdf ({n_created}).pdf")
                convert(tmp_dir, pdf_path)
                n_created += 1
            except:
                print(f"failed to convert {fname}")
            else:
                os.remove(fname)
            finally:
                shutil.rmtree(tmp_dir)
            
if __name__ == "__main__":
    fire.Fire(main)