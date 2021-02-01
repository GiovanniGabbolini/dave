import json
import numpy as np
import re
import pandas as pd
import re
from playlist_explanation.src.data.data import preprocessed_dataset_path
import logging

path_answers = f"{preprocessed_dataset_path}/answers/answers.json"
path_comments = f"{preprocessed_dataset_path}/answers/comments.json"


def pull_treatment(idx):
    with open(f"{preprocessed_dataset_path}/user_trial_sample/{idx}.json") as fp:
        d = json.load(fp)
    return d


def load_answers():
    with open(path_answers) as fp:
        answers = json.load(fp)
    answers = [{k: v for k, v in a.items() if k != '_id'} for a in answers]
    # filter by completion time
    answers = [a for a in answers if a['elapsed_time']/60 >= 3]
    # answers = [a for a in answers if a['elapsed_time']/60 <= 40]
    # filter by language proficiency
    answers = [a for a in answers if 'proficiency_q_0' not in a or a['proficiency_q_0'] != 'Mid']
    return answers


def load_comments():
    with open(path_comments) as fp:
        comments = json.load(fp)
    return comments


def interestingness_df(answers):
    interestingness, rarity, unpopularity, shortness, segue_idx = ([] for _ in range(5))
    df = segue_eval_df(answers)
    df = df[df.treatment == 'dave']
    for idx in df.segue_idx:
        segue_idx.append(idx)
        d = pull_treatment(idx)
        interestingness.append(float(d['segue_dave']['score']))
        rarity.append(float(d['segue_dave']['rarity']))
        unpopularity.append(float(d['segue_dave']['unpopularity']))
        shortness.append(float(d['segue_dave']['shortness']))
    df = pd.DataFrame({
        "segue_idx": segue_idx,
        "interestingness": interestingness,
        "rarity": rarity,
        "unpopularity": unpopularity,
        "shortness": shortness,
    })
    return df.drop_duplicates()


def segue_text_df():
    text, treatment, segue_idx = ([] for _ in range(3))
    for idx in set(segue_eval_df(load_answers()).segue_idx.values):
        d = pull_treatment(idx)
        segue_idx.append(idx)
        text.append(d['segue_dave']['line'])
        treatment.append('dave')
        segue_idx.append(idx)
        text.append(d['segue_the_chain'])
        treatment.append('the_chain')
    df = pd.DataFrame({
        "segue_idx": segue_idx,
        "treatment": treatment,
        "text": text,
    })
    return df.drop_duplicates()


def segue_eval_df(answers):

    def append_to_list(answer, s_idx, key, l):
        pattern = f"segue_eval_[0-5]_{s_idx}_{key}"
        for k in a.keys():
            if re.search(pattern, k):
                l.append(answer[k])
                return
        logging.getLogger().warning(f"Key {pattern} not found in answer! Using nan")
        l.append(np.nan)

    likeable, high_quality, understandable, sparked_interest, funny, informative, creative, well_written, segue_idx, user_idx, treatment, kind = ([
    ] for _ in range(12))
    for u_idx, a in enumerate(answers):

        segues_idxs = set()
        for k in a.keys():
            r = re.search(r"segue_eval_[0-5]_([0-9]+)_dave_q_0", k)
            if r:
                segues_idxs.add(r.group(1))
        if len(segues_idxs) != 3:
            logging.getLogger().warning(f"Evaluating {len(segues_idxs)} instead of 3! Continuing anyway ...")

        for s_idx in segues_idxs:
            segue_idx.append(int(s_idx))
            user_idx.append(u_idx)
            treatment.append('dave')
            append_to_list(a, s_idx, 'dave_q_0', likeable)
            append_to_list(a, s_idx, 'dave_q_1', high_quality)
            append_to_list(a, s_idx, 'dave_q_2', understandable)
            append_to_list(a, s_idx, 'dave_q_3', sparked_interest)
            append_to_list(a, s_idx, 'dave_q_4', funny)
            append_to_list(a, s_idx, 'dave_q_5', informative)
            append_to_list(a, s_idx, 'dave_q_6', creative)
            append_to_list(a, s_idx, 'dave_q_7', well_written)

            segue_idx.append(int(s_idx))
            user_idx.append(u_idx)
            treatment.append('the_chain')
            append_to_list(a, s_idx, 'the_chain_q_0', likeable)
            append_to_list(a, s_idx, 'the_chain_q_1', high_quality)
            append_to_list(a, s_idx, 'the_chain_q_2', understandable)
            append_to_list(a, s_idx, 'the_chain_q_3', sparked_interest)
            append_to_list(a, s_idx, 'the_chain_q_4', funny)
            append_to_list(a, s_idx, 'the_chain_q_5', informative)
            append_to_list(a, s_idx, 'the_chain_q_6', creative)
            append_to_list(a, s_idx, 'the_chain_q_7', well_written)

    df = pd.DataFrame({
        "segue_idx": segue_idx,
        "user_idx": user_idx,
        "treatment": treatment,
        "likeable": likeable,
        "high_quality": high_quality,
        "understandable": understandable,
        "sparked_interest": sparked_interest,
        "funny": funny,
        "informative": informative,
        "creative": creative,
        "well_written": well_written,
        # "kind": kind,
    })
    df = df.replace('Strongly disagree', 1)
    df = df.replace('Disagree', 2)
    df = df.replace('Neutral', 3)
    df = df.replace('Agree', 4)
    df = df.replace('Strongly agree', 5)
    return df


def user_traits_df(answers):
    answers = load_answers()
    active_engagement_q_0, active_engagement_q_1, active_engagement_q_2, active_engagement_q_3, active_engagement_q_4, active_engagement_q_5, active_engagement_q_6, active_engagement_q_7, active_engagement_q_8, proficiency, user_idx = ([
    ] for _ in range(11))
    for u_idx, a in enumerate(answers):
        user_idx.append(u_idx)
        active_engagement_q_0.append(a['active_engagement_q_0'] if 'active_engagement_q_0' in a else np.nan)
        active_engagement_q_1.append(a['active_engagement_q_1'] if 'active_engagement_q_1' in a else np.nan)
        active_engagement_q_2.append(a['active_engagement_q_2'] if 'active_engagement_q_2' in a else np.nan)
        active_engagement_q_3.append(a['active_engagement_q_3'] if 'active_engagement_q_3' in a else np.nan)
        active_engagement_q_4.append(a['active_engagement_q_4'] if 'active_engagement_q_4' in a else np.nan)
        active_engagement_q_5.append(a['active_engagement_q_5'] if 'active_engagement_q_5' in a else np.nan)
        active_engagement_q_6.append(a['active_engagement_q_6'] if 'active_engagement_q_6' in a else np.nan)
        active_engagement_q_7.append(a['active_engament_q_7_q_0'] if 'active_engament_q_7_q_0' in a else np.nan)
        active_engagement_q_8.append(a['active_engament_q_8_q_0'] if 'active_engament_q_8_q_0' in a else np.nan)
        proficiency.append(a['proficiency_q_0'] if 'proficiency_q_0' in a else np.nan)
    df = pd.DataFrame({
        'user_idx': user_idx,
        'active_engagement_q_0': active_engagement_q_0,
        'active_engagement_q_1': active_engagement_q_1,
        'active_engagement_q_2': active_engagement_q_2,
        'active_engagement_q_3': active_engagement_q_3,
        'active_engagement_q_4': active_engagement_q_4,
        'active_engagement_q_5': active_engagement_q_5,
        'active_engagement_q_6': active_engagement_q_6,
        'active_engagement_q_7': active_engagement_q_7,
        'active_engagement_q_8': active_engagement_q_8,
        'proficiency': proficiency,
    })
    df.active_engagement_q_7 = df.active_engagement_q_7.replace("0", 1).replace("1", 2).replace(
        "2", 3).replace("3", 4).replace("4-6", 5).replace("7-10", 6).replace("11 or more", 7)
    df.active_engagement_q_8 = df.active_engagement_q_8.replace("0-15mins", 1).replace("15-30mins", 2).replace(
        "30-60mins", 3).replace("60-90mins", 4).replace("2hrs", 5).replace("2-3hrs", 6).replace("4hrs or more", 7)
    df = df.replace('Strongly  disagree', 1)
    df = df.replace('Somewhat  disagree', 2)
    df = df.replace('Disagree', 3)
    df = df.replace('Neutral', 4)
    df = df.replace('Agree', 5)
    df = df.replace('Somewhat  agree', 6)
    df = df.replace('Strongly agree', 7)
    return df


def familiarity_df():
    segue_idx, user_idx, treatment, familiarity_first_artist, familiarity_second_artist, familiarity_first_song, familiarity_second_song = ([
    ] for _ in range(7))

    answers = load_answers()
    for u_idx, a in enumerate(answers):
        for i in range(6):

            key = set()
            for k in a.keys():
                match = re.match(f"segue_eval_{i}_(\d+)_(the_chain|dave)_q_\d", k)
                if match:
                    key.add((match.group(1), match.group(2)))
            if len(key) != 1:

                if len(key) > 1:
                    logging.getLogger().warning("Found two couples segues_idx, treatment in answer, skipping")
                    continue
                else:
                    logging.getLogger().warning("Did not found any couples segues_idx, treatment in answer, skipping")
                    continue

            segue_idx.append(int(list(key)[0][0]))
            treatment.append(list(key)[0][1])
            user_idx.append(u_idx)

            key = f'familiarity_artists_q_{i//2+6}'
            if key in a:
                familiarity_first_artist.append(a[key])
            else:
                familiarity_first_artist.append(np.nan)
                logging.getLogger().warning("Cannot find familiarity with the artist of first song, using nan")

            key = f'familiarity_artists_q_{i}'
            if key in a:
                familiarity_second_artist.append(a[key])
            else:

                familiarity_second_artist.append(np.nan)
                logging.getLogger().warning("Cannot find familiarity with the artist of second song, using nan")

            key = f'familiarity_songs_q_{i//2+6}'
            if key in a:
                familiarity_first_song.append(a[key])
            else:
                familiarity_first_song.append(np.nan)
                logging.getLogger().warning("Cannot find familiarity with the first song, using nan")

            key = f'familiarity_songs_q_{i}'
            if key in a:
                familiarity_second_song.append(a[key])
            else:
                familiarity_second_song.append(np.nan)
                logging.getLogger().warning("Cannot find familiarity with the first song, using nan")

    df = pd.DataFrame({
        'segue_idx': segue_idx,
        'user_idx': user_idx,
        'treatment': treatment,
        'familiarity_first_artist': familiarity_first_artist,
        'familiarity_second_artist': familiarity_second_artist,
        'familiarity_first_song': familiarity_first_song,
        'familiarity_second_song': familiarity_second_song,
    })
    return df


def segue_category_df():
    df_dave = pd.read_csv(f'{preprocessed_dataset_path}/answers/df_segue_category_dave.csv', index_col=0).drop(['text'], axis=1)
    df_dave['treatment'] = 'dave'
    df_dave = df_dave.rename({'category (F/I)': 'segue_category'}, axis=1)
    df_the_chain = pd.read_csv(f'{preprocessed_dataset_path}/answers/df_segue_category_the_chain.csv', index_col=0).drop(['first_song', 'segue', 'second_song'], axis=1)
    df_the_chain['treatment'] = 'the_chain'
    df_the_chain = df_the_chain.rename({'category (F/I)': 'segue_category'}, axis=1)
    return pd.concat([df_dave, df_the_chain], axis=0)


def user_category_df(separation='fourway'):
    user_idx, user_category = ([] for _ in range(2))
    df_user_traits = user_traits_df(load_answers()).drop("proficiency", axis=1)
    df_user_traits['gold_msi'] = df_user_traits[df_user_traits.columns[1:]].sum(axis=1)

    quartiles = df_user_traits['gold_msi'].quantile([0.25, 0.50, 0.75])
    threetiles = df_user_traits['gold_msi'].quantile([0.33, 0.66])

    for u_idx, gold_msi in zip(df_user_traits.user_idx, df_user_traits.gold_msi):
        user_idx.append(u_idx)
        if separation == 'fourway':
            if gold_msi < quartiles.values[0]:
                user_category.append('1')
            elif gold_msi >= quartiles.values[0] and gold_msi < quartiles.values[1]:
                user_category.append('2')
            elif gold_msi >= quartiles.values[1] and gold_msi < quartiles.values[2]:
                user_category.append('3')
            else:
                user_category.append('4')

        elif separation == 'threeway':
            if gold_msi < threetiles.values[0]:
                user_category.append('1')
            elif gold_msi >= threetiles.values[0] and gold_msi < threetiles.values[1]:
                user_category.append('2')
            else:
                user_category.append('3')

        elif separation == 'twoway':
            if gold_msi < quartiles.values[1]:
                user_category.append('1')
            else:
                user_category.append('2')

    return pd.DataFrame({
        'user_idx': user_idx,
        'user_category': user_category,
    })


def comments_df():
    user_idx, comment = ([] for _ in range(2))
    answers = load_answers()
    comments = load_comments()
    for c in comments:
        author = [u_idx for u_idx, a in enumerate(answers) if a['starting_time'] == c['starting_time']]
        if len(author) == 1:
            user_idx.append(author[0])
            comment.append(c['comment'])
        elif len(author) == 0:
            continue
        else:
            raise ValueError(f"Comment have left more than author, this is not possible.")
    return pd.DataFrame({
        'comment_idx': list(range(len(user_idx))),
        'user_idx': user_idx,
        'comment': comment,
    })


if __name__ == "__main__":
    # comments_df()
    load_answers()
    # user_category_df(separation='twoway')
    # segue_category_df()
    # elapsed_time()
    # user_traits_df(load_answers())
    # familiarity_df()
    # segue_eval_df(load_answers())
    # segue_text_df()
    # heatmap_partition()
