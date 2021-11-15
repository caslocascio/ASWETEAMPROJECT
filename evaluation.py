from flask import Flask, request, jsonify
import db
# import analysis commented out for use in second iter
import random

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


'''
running the service on localhost in similar fashion to
the miniproject. Therefore, the '/' of method type GET will confirm
to those wishing to utilize our service that they are in the right place
'''


@app.route('/')
def hello_world():
    return jsonify(msg="ItWorksOnLocal Service")


'''
'/professor' endpoint
Method Type: GET
return: 1 comprehensive review for a professor
requires: desired professor name

note: random utilized here so a different review for a professor
will be provided upon each call.This will make it easier for
service utilizers to visualize needed information instead of bombarding
with all reviews. If they wish for specific information
regarding a professor such as if they are easy or provide extensions,
please see '/easy' and '/extensions' endpoints.
'''


# will test this in second iteration since it is randomized
@app.route('/professor', methods=['GET'])
def prof():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)
    # return a random review from list
    num = random.randint(0, len(lst))
    return jsonify(entry=lst[num])


'''
'/easy' endpoint
Method Type: GET
return: # of students who mentioned prof is easy/has lenient grading/etc
requires: desired professor name
'''


# starting off with professor
# will build logic in second iteration to include class, date, etc
@app.route('/easy', methods=['GET'])
def easy():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)

    # setting up variables to count instances of ease in entry
    easyA = 0
    aPlus = 0
    lenGrading = 0
    rec = 0
    # searching through each review and workload for such ease phrases
    for i in range(0, len(lst)):
        extract = lst[i]
        review = extract[3]
        workLoad = extract[4]

        if 'easy' in review or 'easy' in workLoad:
            easyA += 1
        if 'A+' in review or 'A+' in workLoad:
            aPlus += 1
        if 'lenient grading' in review or 'lenient grading' in workLoad:
            lenGrading += 1
        if 'I recommend' in review or 'I recommend' in workLoad:
            rec += 1
    # no instances found
    if easyA == 0 and aPlus == 0 and lenGrading == 0 and rec == 0:
        return jsonify(easy_status=False)
    else:
        # return counts of each ease phrase based on all reviews for professor
        return jsonify(easy_A=easyA, A_plus=aPlus,
                       lenient_grading=lenGrading, I_recommend=rec)


'''
'/final' endpoint
Method Type: GET
return: # of students who mentioned course has no final/take home/final paper
requires: desired course title
'''


# starting off with class
# will build logic in second iteration to include professor, date, etc
@app.route('/final', methods=['GET'])
def final_exam():
    # get course title from request URL
    course = request.args.get('course')
    # get review records from the database of this course
    lst = db.get_entry_class(course)

    # setting up variables to count instances of final information in entry
    noFinal = 0
    takeHome = 0
    finPaper = 0
    for i in range(0, len(lst)):
        extract = lst[i]
        review = extract[3]
        workLoad = extract[4]

        if 'no final' in review or 'no final' in workLoad:
            noFinal += 1
        if 'take-home' in review or 'take-home' in workLoad:
            takeHome += 1
        if 'final paper' in review or 'final paper' in workLoad:
            finPaper += 1
    # no instances found
    if noFinal == 0 and takeHome == 0 and finPaper == 0:
        return jsonify(final_exam='no indicator that class is final exam free')
    else:
        # return counts of each ease phrase based on all reviews for professor
        return jsonify(no_final_exam=noFinal, take_home=takeHome,
                       final_paper=finPaper)


'''
'/extensions' endpoint
Method Type: GET
return: # of students who mentioned professor gives extensions
requires: desired professor name
'''


# starting off with professor
# will build logic in second iteration to include class, date, etc
@app.route('/extensions', methods=['GET'])
def extensions():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)

    # setting up variable to count instances of extension in entry
    extension = 0
    for i in range(0, len(lst)):
        extract = lst[i]
        review = extract[3]
        workLoad = extract[4]

        if 'extension' in review or 'extension' in workLoad:
            extension += 1
    # no instances found
    if extension == 0:
        return jsonify(extension_status='no indicator prof gives extensions')
    else:
        # return counts of extension based on all reviews for professor
        return jsonify(extension=extension)


'''
'/difficulty' endpoint
Method Type: GET
return: # of students who mentioned course has harsh grading/is boring/etc
requires: desired course title
'''


# starting off with class
# will build logic in second iteration to include professor, date, etc
@app.route('/difficulty', methods=['GET'])
def difficulty():
    # get course title from request URL
    course = request.args.get('course')
    # get review records from the database of this course
    lst = db.get_entry_class(course)

    # setting up variable to count instances of difficulty phrases in entry
    harshGrading = 0
    boring = 0
    hard = 0
    notRec = 0
    for i in range(0, len(lst)):
        extract = lst[i]
        review = extract[3]
        workLoad = extract[4]

        if 'harsh grading' in review or 'harsh grading' in workLoad:
            harshGrading += 1
        if 'boring' in review or 'boring' in workLoad:
            boring += 1
        if 'hard' in review or 'hard' in workLoad:
            hard += 1
        if 'not recommend' in review or 'not recommend' in workLoad:
            notRec += 1
    # no instances found
    if harshGrading == 0 and boring == 0 and hard == 0 and notRec == 0:
        return jsonify(difficulty_status='no indicator course is too tough')
    else:
        # return counts of difficulty phrases based on all reviews for prof
        return jsonify(harsh_grading=harshGrading, boring=boring,
                       hard=hard, not_recommended=notRec)


'''
'/total_reviews' endpoint
Method Type: GET
return: total number of reviews for a given professor
requires: desired professor name
'''


@app.route('/total_reviews', methods=['GET'])
def total_reviews():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)
    return jsonify(professor_name=profName, total_reviews=len(lst))


"""
Commenting these two endpoints out as they need a bit more work
which will be completed by the second iteration.
"""

"""
'''
'/review_ages/<date>' endpoint
Method Type: POST
return: professor name along with the number of old/new reviews based upon date
requires: desired professor name and date
'''


@app.route('/review_ages/<date>', methods=['POST'])
def review_ages(date):
    print('date:', date)
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)
    # check if the review is too old
    n_old_reviews, n_new_reviews = analysis.check_aged_reviews(lst, date)
    return jsonify(professor_name=profName, threshold=date,
                   old_reviews=n_old_reviews, new_reviews=n_new_reviews)


'''
'/sentiment' endpoint
Method Type: GET
return: sentiment analysis (eg. objective reviews) based upon professor
requires: desired professor name
'''


@app.route('/sentiment', methods=['GET'])
def sentiment_analysis():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)
    # perform review analysis
    df, _, _, n_pos, n_neu, n_neg, n_obj, n_sub = analysis.review_analysis(lst)
    # rename columns
    df = df.rename(columns={'senti_fl': 'sentiment', 'sub_fl': 'subjectivity'})
    # compose result
    fields = ['professor', 'class', 'date', 'review', 'workload',
              'agree', 'disagree', 'funny', 'sentiment', 'subjectivity']
    review_dicts = [dict(zip(fields, d)) for d in df[fields].values.tolist()]
    return jsonify(professor_name=profName, positive_reviews=str(n_pos),
                   neutral_reviews=str(n_neu), negative_reviews=str(n_neg),
                   objective_reviews=str(n_obj), subjective_reviews=str(n_sub),
                   details=review_dicts)
"""

if __name__ == '__main__':
    # run Flask app
    app.run(debug=True, host='127.0.0.1')
