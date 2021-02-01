"""
Created on Mon Mar 02 2020

@author Giovanni Gabbolini
"""

import re


def preprocess_track_name(track_name):
    """return the track name after having removed additional info like remix, remastered ecc.
       TODO: we should mine those info in a proper feature instead of throwing them away

    Arguments:
        track_name {string} -- 

    """
    preprocessed_track_name = re.sub(
        "([\(\[]).*?([\)\]])|-.*", "", track_name).strip()
    return preprocessed_track_name
