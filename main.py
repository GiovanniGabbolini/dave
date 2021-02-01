from user_trial.user_trial import save_answers, draw
import traceback
from flask_session import Session
from flask import Flask, redirect, url_for, render_template, request, session
import random
import time


app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

if app.env == 'production':
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

"""
    The enviroment has to be specifiend inside the .env file with such a line:
    FLASK_ENV=development or FLASK_ENV=production
"""


@app.errorhandler(Exception)
def internal_error(exception):
    # If we are excecuting the user trial and there is this error, let's start the trial from scratch
    test = KeyError('user_trial')
    if type(exception) is type(test) and exception.args == test.args:
        return redirect(url_for('user_trial'))

    # Log into python.log every other exception.
    app.logger.error(traceback.format_exc())
    return render_template('500.html'), 500


@app.before_request
def init_session():
    if 'number_ranked_segues' not in session:
        session['number_ranked_segues'] = 10
    if 'rar_w' not in session:
        session['rar_w'] = 0.5
    if 'unpop_w' not in session:
        session['unpop_w'] = 0.2
    if 'shortness_w' not in session:
        session['shortness_w'] = 0.3
    if 'main_text' not in session:
        session['main_text'] = 'short'



@app.route("/")
@app.route("/user_trial")
def user_trial():
    try:
        session['user_trial']['completed']
        return render_template("user_trial_page_done.html")
    except KeyError:
        session['user_trial'] = {}
        session['user_trial']['page_num'] = 1
        session['user_trial']['answers'] = {'starting_time': time.time()}

        session['user_trial']['trial_draw'] = []

        for trial_draw in draw(3):
            d1 = {'first_song': trial_draw['seed_song'], 'segue': trial_draw['segue_dave']['line'],
                  'second_song': trial_draw['song_dave'], 'idx': trial_draw['idx_user_trial_folder'], 'who': 'dave'}
            d2 = {'first_song': trial_draw['seed_song'], 'segue': trial_draw['segue_the_chain'],
                  'second_song': trial_draw['song_the_chain'], 'idx': trial_draw['idx_user_trial_folder'], 'who': 'the_chain'}
            if random.uniform(0, 1) > 0.5:
                session['user_trial']['trial_draw'] += [d1, d2]
            else:
                session['user_trial']['trial_draw'] += [d2, d1]

        return render_template("user_trial_page_intro.html", title="Instructions", button_text="Continue", insight_logo=True)


@app.route('/user_trial_answer', methods=['GET', ])
def user_trial_answer():
    question_id = request.args.get('question_id')
    answer = request.args.get('answer')
    session['user_trial']['answers'][question_id] = answer
    return ''


@app.route('/save_comment_survey', methods=['GET', ])
def save_comment_survey():
    comment = request.args.get('text')
    d = {'comment': comment, 'starting_time': session['user_trial']['answers']['starting_time']}
    save_answers(d, collection='comments')
    return ''


@app.route('/user_trial_increment_page', methods=['GET', ])
def user_trial_increment_page():
    if request.referrer.split('/')[-1] == '':
        session['user_trial']['page_num'] = 2
    else:
        session['user_trial']['page_num'] += 1
    return redirect(url_for('user_trial_next_page'))


@app.route('/user_trial_decrement_page', methods=['GET', ])
def user_trial_decrement_page():
    # When the survey is completed, the Back button cannot be hit
    if 'completed' not in session['user_trial']:
        session['user_trial']['page_num'] -= 1

    if session['user_trial']['page_num'] == 1:
        return redirect(url_for('user_trial'))
    else:
        return redirect(url_for('user_trial_next_page'))


@app.route('/user_trial_next_page', methods=['GET', ])
def user_trial_next_page():

    if 'user_trial' not in session:
        return redirect(url_for('user_trial'))

    if session['user_trial']['page_num'] == 2:
        return render_template("user_trial_page_user_infos.html", allow_back=True, title="Survey", button_text="Continue", render_template=render_template,)

    elif session['user_trial']['page_num'] in [3, 4, 5, 6, 7, 8]:
        return render_template("user_trial_page_segue_eval.html", allow_back=True, title="Survey", button_text="Continue",
                               render_template=render_template, n_segue=session['user_trial']['page_num']-3,
                               **session['user_trial']['trial_draw'][session['user_trial']['page_num']-3])

    elif session['user_trial']['page_num'] == 9:
        return render_template("user_trial_page_artists_familiarity.html", allow_back=True, title="Survey", button_text="Continue", render_template=render_template,
                               second_song_1=session['user_trial']['trial_draw'][0]['second_song'],
                               second_song_2=session['user_trial']['trial_draw'][1]['second_song'],
                               second_song_3=session['user_trial']['trial_draw'][2]['second_song'],
                               second_song_4=session['user_trial']['trial_draw'][3]['second_song'],
                               second_song_5=session['user_trial']['trial_draw'][4]['second_song'],
                               second_song_6=session['user_trial']['trial_draw'][5]['second_song'],
                               first_song_1=session['user_trial']['trial_draw'][0]['first_song'],
                               first_song_2=session['user_trial']['trial_draw'][2]['first_song'],
                               first_song_3=session['user_trial']['trial_draw'][4]['first_song'],)

    elif session['user_trial']['page_num'] == 10:
        return render_template("user_trial_page_songs_familiarity.html", allow_back=True, title="Survey", button_text="Continue", render_template=render_template,
                               second_song_1=session['user_trial']['trial_draw'][0]['second_song'],
                               second_song_2=session['user_trial']['trial_draw'][1]['second_song'],
                               second_song_3=session['user_trial']['trial_draw'][2]['second_song'],
                               second_song_4=session['user_trial']['trial_draw'][3]['second_song'],
                               second_song_5=session['user_trial']['trial_draw'][4]['second_song'],
                               second_song_6=session['user_trial']['trial_draw'][5]['second_song'],
                               first_song_1=session['user_trial']['trial_draw'][0]['first_song'],
                               first_song_2=session['user_trial']['trial_draw'][2]['first_song'],
                               first_song_3=session['user_trial']['trial_draw'][4]['first_song'],)

    elif session['user_trial']['page_num'] == 11:
        session['user_trial']['answers']['elapsed_time'] = time.time()-session['user_trial']['answers']['starting_time']
        save_answers(session['user_trial']['answers'])

        session['user_trial']['page_num'] += 1
        session['user_trial']['completed'] = True
        return render_template("user_trial_page_outro.html")
    else:
        return redirect(url_for('user_trial'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    # app.run(host="0.0.0.0", port=80)
