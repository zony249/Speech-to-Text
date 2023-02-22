import glob

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace

from genutils import mkdir

def initTokenizer(svfile=None):
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    if svfile is not None:
        try:
            tokenizer.from_file(svfile)
        except:
            print(f"Failed to load from save file: '{svfile}'")
            return tokenizer
    



if __name__ == "__main__":
    print(glob.glob("data/*/*/*/*.txt"))