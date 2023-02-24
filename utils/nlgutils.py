import glob
import itertools
from pathlib import Path
from tqdm import tqdm

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace

from opt import Opt
from genutils import mkdir, rmdir, parse_config

class Decoder_tokenizer:
    def __init__(self, svfile=None):
        self.tok = Tokenizer(BPE(unk_token="[UNK]"))
        self.tok.pre_tokenizer = Whitespace()
        if svfile is not None:
            try:
                self.tok.from_file(svfile)
            except:
                print(f"Failed to load from save file: '{svfile}'")
        
    def get_file_paths_to_labels(self):
        """
        Scans your train, val, and test directories for all text files
        """
        directories = Opt.train + Opt.val + Opt.test
        return list(itertools.chain.from_iterable(glob.glob(x + "/labels/*.txt") for x in directories))

    def preprocess(self, preproc_callback, filepaths):
        """
        @param preproc_callback
        @param filepaths ([str]):
        """
        return [preproc_callback(x) for x in tqdm(filepaths, desc="Preprocessing text files")]

    def train(self):
        
        rmdir(".cache")
        mkdir(".cache")

        label_paths = self.get_file_paths_to_labels()
        self.preprocess(librispeech_label_preproc, label_paths)
    
    
def librispeech_label_preproc(filepath):
    """
    Inputs: path to input text file
    outputs: path to processed text file.
            This function will also save 
            the processed text file at the 
            location specified by the returned
            file path.

    @param filepath (str): path to the input text file
    
    @return (str): path to the processed text file
    """

    filename = filepath.split("/")[-1]
    dest_path = Path(Opt.cache) / filename
    with open(filepath, "r") as infile:
        lines = [" ".join(x.split(" ")[1:]).lower() for x in infile.readlines()]
    with open(dest_path, "w") as outfile:
        outfile.writelines("".join(lines))
    return str(dest_path)




if __name__ == "__main__":
    parse_config("config/conf.yaml")

    dec_tok = Decoder_tokenizer()
    print(len(dec_tok.get_file_paths_to_labels()))
    dec_tok.train()
