from flask import Flask, request, jsonify
from functions import db
from functions import analysis
import random

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def hello_world():
    return jsonify(msg="ItWorksOnLocal Service")

@app.route('/total_reviews', methods=['GET'])
def total_reviews():
    # get professor name from the input parameter
    prof_name = request.args.get('profname')
    print('prof_name:', prof_name)
    # get review records from the database of this professor
    review_lst = db.get_entry_professor(prof_name)
    # compose result
    res = {
        'professor_name': prof_name,
        'total_reviews': len(review_lst)
        }
    return jsonify(res)

@app.route('/review_ages/<date>', methods=['POST'])
def review_ages(date):
    print('date:', date)
    # get professor name from the input parameter
    prof_name = request.args.get('profname')
    print('prof_name:', prof_name)
    # get review records from the database of this professor
    review_lst = db.get_entry_professor(prof_name)
    # check if the review is too old
    n_old_reviews, n_new_reviews = analysis.check_aged_reviews(review_lst, date)
    # compose result
    res = {
        'professor_name': prof_name,
        'threshold': date,
        'old_reviews': n_old_reviews,
        'new_reviews': n_new_reviews
        }
    return jsonify(res)

@app.route('/sentiment', methods=['GET'])
def sentiment_analysis():
    # get professor name from the input parameter
    prof_name = request.args.get('profname')
    print('prof_name:', prof_name)
    # get review records from the database of this professor
    review_lst = db.get_entry_professor(prof_name)
    # perform review analysis 
    df, _, _, n_pos, n_neu, n_neg, n_obj, n_sub = analysis.review_analysis(review_lst)
    # rename columns
    df = df.rename(columns={'senti_fl': 'sentiment', 'sub_fl': 'subjectivity'})
    # compose result
    fields = ['professor', 'class', 'date', 'review', 'workload', 'agree', 'disagree', 'funny', 'sentiment', 'subjectivity']
    review_dicts = [dict(zip(fields, d)) for d in df[fields].values.tolist()]
    res = {
        'professor_name': prof_name,
        'postive reviews': str(n_pos),
        'neutral reviews': str(n_neu),
        'negative reviews': str(n_neg),
        'objective reviews': str(n_obj),
        'subjective reviews': str(n_sub),
        'details': review_dicts
    }
    return jsonify(res)


if __name__ == '__main__':
    # run Flask app
    print(db.get_table_counts())
    db.init_db()
    print('Starting service...')
    app.run(debug=True, host='127.0.0.1')
