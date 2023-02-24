import os
import pathlib
import glob
from pathlib import Path
import yaml
from tqdm import tqdm
import shutil


from opt import Opt


def mkdir(filepath):
    """
    recursively creates directories until 
    the leaf direcory/file is reached. If the last
    token has a file extension, then the last element
    will be a file. Otherwise, the last element will
    be a directory.
    """
    fpath = str(Path(filepath))
    tokens = fpath.split("/")
    print(tokens)
    print(fpath)
    if not tokens[-1].startswith("."):
        os.makedirs("/".join(tokens[:-1]), exist_ok=True)
        with open(fpath, "w") as f:
            f.write('\n')
    else: 
        os.makedirs(fpath, exist_ok=True)

def rmdir(filepath):
    shutil.rmtree(filepath, ignore_errors=True)


def restructure_folder(dirname, ext):
    """
    Converts the nested mess of directories that is the 
    LibriSpeech Dataset into something easier to work with.

    Params: 
        dirname: the name of the base directory with the file structure as shown:
            dirname/X/X/.../X/<audio_files.ext> (ext could be flac, mp3, etc...)
            dirname/X/X/.../X/<lable_files.txt>
        ext: filename extension for audio files

    Result:
        dirname/audio/<audio_files.ext>
        dirname/labels/<lable_files.txt>
    """

    max_depth = 10
    basepath = Path(dirname)

    audio_paths = []
    label_paths = []

    for i in range(max_depth):
        searchpath = basepath / f"*.{ext}"
        audio_paths += glob.glob(str(searchpath))
        searchpath = basepath / f"*.txt"
        label_paths += glob.glob(str(searchpath))
        basepath = basepath / "*"

    mkdir(dirname + "/audio/")
    mkdir(dirname + "/labels/")


    for i in tqdm(range(len(audio_paths)), desc=f"Reorganizing {dirname} audio files"):
        Path(audio_paths[i]).rename(dirname + "/" + "audio/" + audio_paths[i].split("/")[-1])
    for i in tqdm(range(len(label_paths)), desc=f"Reorganizing {dirname} label files"):
        Path(label_paths[i]).rename(dirname + "/" + "labels/" + label_paths[i].split("/")[-1])

    for x in glob.glob(dirname + "/*/"):
        if "audio" not in x and "labels" not in x:
            shutil.rmtree(x, ignore_errors=True)
            # print(x)


def parse_config(config_filename):
    """
    Parses the config YAML file and updates the Opt 
    environment class

    @param config_filename (str): filename to the YAML file
    """
    with open(config_filename, "r") as f:
        items = yaml.safe_load(f)
        for key in items:
            setattr(Opt, key, items[key])

    print(Opt.info())


if __name__ == "__main__":

    CACHE = ".cache"

    # mkdir("dir1/dir2/dir3/file.py")
    # mkdir("dir1/dir2/dir3/file")

    # restructure_folder("data/dev-clean/", "flac")
    # restructure_folder("data/dev-other/", "flac")
    # restructure_folder("data/test-clean/", "flac")
    # restructure_folder("data/test-other/", "flac")
    # restructure_folder("data/train-clean-100/", "flac")

    parse_config("config/conf.yaml")

    os.makedirs("test/testing", exist_ok=True)
    os.makedirs("test/.testing", exist_ok=True)
    os.makedirs("test/testing.txt", exist_ok=True)