'''
Created on Sun Feb 16 2020

@author Giovanni Gabbolini
'''
import os
import gzip
import shutil
from src.data import data
import gensim
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


def download_original_embeddings():
    """downloads the original vectors by milkolv et al
    """
    target_path = os.path.join(
        data.raw_dataset_path, "GoogleNews-vectors-negative300.bin")
    if not os.path.exists(target_path):
        os.makedirs(data.raw_dataset_path, exist_ok=True)
        os.makedirs(data.preprocessed_dataset_path, exist_ok=True)

        os.system(
            'wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"')
        os.system(
            'mv GoogleNews-vectors-negative300.bin.gz {}.gz'.format(target_path))

        with gzip.open('{}.gz'.format(target_path), 'rb') as f_in:
            with open(target_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.system('rm {}.gz'.format(target_path))


def save_1m_opt_format_embeddings_w2vec(target_path):
    """ saves the 1M embeddings of most frequent words, in a read optimized format
    """
    download_original_embeddings()
    model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(
        data.raw_dataset_path, 'GoogleNews-vectors-negative300.bin'), binary=True, limit=1000000)
    model.save(target_path)


def save_1m_opt_format_embeddings_glove(target_path):
    """ saves the 1M embeddings of most frequent words, in a read optimized format
    """
    glove_path = os.path.join(
        data.raw_dataset_path, "glove.42B.300d.txt")
    tmp_path = os.path.join(
        data.raw_dataset_path, "glove.42B.300d_temp.txt")

    _ = glove2word2vec(glove_input_file=glove_path,
                       word2vec_output_file=tmp_path)

    model = KeyedVectors.load_word2vec_format(
        tmp_path, binary=False)
    model.save(target_path)


if __name__ == "__main__":
    save_1m_opt_format_embeddings_glove(os.path.join(
        data.preprocessed_dataset_path, "glove_raw_1m"))
