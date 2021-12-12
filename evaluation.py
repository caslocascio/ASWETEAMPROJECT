from flask import Flask, request, jsonify, abort
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
import db
import analysis
import random
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


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
regarding a professor, please see other endpoints below.
'''


@app.route('/professor', methods=['GET'])
def prof():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = []
    lst = db.get_entry_professor(profName)
    # return a random review from list
    if len(lst) > 0:
        num = random.randint(0, (len(lst) - 1))
        return jsonify(reviews=lst[num])
    else:
        return abort(404)


'''
'/summary' endpoint
Method Type: GET
return: 3 phrase summary of a professor's reviews
requires: desired professor name
'''


@app.route('/summary', methods=['GET'])
def summary():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get review records from the database of this professor
    lst = []
    lst = db.get_entry_professor(profName)
    # extract review strings and summarize
    conCat = ""
    if len(lst) > 0:
        for i in range(len(lst)):
            review = lst[i][3]
            conCat += review + ' '

        # summarizer logic
        parser = PlaintextParser.from_string(conCat, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        # return a three sentence summary based upon all reviews for prof
        summ = summarizer(parser.document, 3)
        return jsonify(professor_name=profName, summary_of_reviews=str(summ))
    else:
        return abort(404)


def get_easy(course, profName='', usage=1):
    lst = []

    # get review records from the database of this prof or class
    if profName is not None and profName != "":
        lst = db.get_entry_professor(profName)
    elif course is not None and course != "":
        lst = db.get_entry_class(course)

    if len(lst) > 0:
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

            if not (review is None):
                if 'easy' in review:
                    easyA += 1
                if 'A+' in review:
                    aPlus += 1
                if 'lenient grading' in review:
                    lenGrading += 1
                if 'I recommend' in review:
                    rec += 1

            elif not (workLoad is None):
                if 'easy' in workLoad:
                    easyA += 1
                if 'A+' in workLoad:
                    aPlus += 1
                if 'lenient grading' in workLoad:
                    lenGrading += 1
                if 'I recommend' in workLoad:
                    rec += 1

    else:
        return abort(404)

    easyLst = [easyA, aPlus, lenGrading, rec]

    if usage == 1:
        return easyLst
    elif usage == 2:
        score = easyA + aPlus + lenGrading + rec
        return score


'''
'/easy' endpoint
Method Type: GET
return: # of students who mentioned prof is easy/has lenient grading/etc
requires: desired professor name or course title
note: user will use this endpoint for either prof or course in one query
'''


@app.route('/easy', methods=['GET'])
def easy():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get course title from request URL
    course = request.args.get('course')

    eList = get_easy(course=course, profName=profName)

    # no instances found
    if eList[0] == 0 and eList[1] == 0 and eList[2] == 0 and eList[3] == 0:
        return jsonify(easy_status=False)
    else:
        # return counts of each ease phrase based on all reviews
        return jsonify(easy_A=eList[0], A_plus=eList[1],
                       lenient_grading=eList[2], I_recommend=eList[3])


def get_final(course, usage=1):
    lst = []
    # get review records from the database of this course
    lst = db.get_entry_class(course)

    if len(lst) > 0:
        # setting up variables to count instances of final information in entry
        noFinal = 0
        takeHome = 0
        finPaper = 0
        for extract in lst:
            review = extract[3]
            workLoad = extract[4]

            if not (review is None):
                if 'no final' in review:
                    noFinal += 1
                if 'take-home' in review:
                    takeHome += 1
                if 'final paper' in review:
                    finPaper += 1

            elif not (workLoad is None):
                if 'no final' in workLoad:
                    noFinal += 1
                if 'take-home' in workLoad:
                    takeHome += 1
                if 'final paper' in workLoad:
                    finPaper += 1
    else:
        return abort(404)

    finalLst = [noFinal, takeHome, finPaper]

    if usage == 1:
        return finalLst
    elif usage == 2:
        score = noFinal + takeHome + finPaper
        return score


'''
'/final' endpoint
Method Type: GET
return: # of students who mentioned course has no final/take home/final paper
requires: desired course title
'''


@app.route('/final', methods=['GET'])
def final_exam():
    # get course title from request URL
    course = request.args.get('course')

    finLst = get_final(course)

    # no instances found
    if finLst[0] == 0 and finLst[1] == 0 and finLst[2] == 0:
        return jsonify(final_exam='no sign class is final exam free')
    else:
        # return counts of each ease phrase based on all reviews
        return jsonify(no_final_exam=finLst[0], take_home=finLst[1],
                       final_paper=finLst[2])


'''
'/extensions' endpoint
Method Type: GET
return: # of students who mentioned professor gives extensions
requires: desired professor name
'''


@app.route('/extensions', methods=['GET'])
def extensions():
    # get professor name from request URL
    profName = request.args.get('profname')

    lst = []
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)

    if len(lst) > 0:
        # setting up variable to count instances of extension in entry
        extension = 0
        for extract in lst:
            review = extract[3]
            workLoad = extract[4]

            if not (review is None):
                if 'extension' in review:
                    extension += 1

            elif not (workLoad is None):
                if 'extension' in workLoad:
                    extension += 1
        # no instances found
        if extension == 0:
            return jsonify(extension_status='no sign prof gives extensions')
        else:
            # return counts of extension based on all reviews for professor
            return jsonify(extension=extension)
    else:
        return abort(404)


def get_difficulty(course='', profName='', usage=1):
    lst = []

    # get review records from the database of this prof or class
    if profName is not None and profName != "":
        lst = db.get_entry_professor(profName)
    elif course is not None and course != "":
        lst = db.get_entry_class(course)

    if len(lst) > 0:
        # setting up variable to count instances of difficulty phrases in entry
        harshGrading = 0
        boring = 0
        hard = 0
        notRec = 0
        for i in range(0, len(lst)):
            extract = lst[i]
            review = extract[3]
            workLoad = extract[4]

            if not (review is None):
                if 'harsh grading' in review:
                    harshGrading += 1
                if 'boring' in review:
                    boring += 1
                if 'hard' in review:
                    hard += 1
                if 'not recommend' in review:
                    notRec += 1

            elif not (workLoad is None):
                if 'harsh grading' in workLoad:
                    harshGrading += 1
                if 'boring' in workLoad:
                    boring += 1
                if 'hard' in workLoad:
                    hard += 1
                if 'not recommend' in workLoad:
                    notRec += 1

    else:
        return abort(404)

    diffLst = [harshGrading, boring, hard, notRec]

    if usage == 1:
        return diffLst
    elif usage == 2:
        score = harshGrading + boring + hard + notRec
        return score


'''
'/difficulty' endpoint
Method Type: GET
return: # of students who mentioned course has harsh grading/is boring/etc
requires: desired course title
'''


@app.route('/difficulty', methods=['GET'])
def difficulty():
    # get course title from request URL
    course = request.args.get('course')
    # get professor name from reuqest URL
    profName = request.args.get('profname')

    diffLst = get_difficulty(course, profName)

    # no instances found
    if diffLst[0] == 0 and diffLst[1] == 0\
       and diffLst[2] == 0 and diffLst[3] == 0:
        return jsonify(difficulty_status='no sign course is too tough')
    else:
        # return counts of difficulty phrases based on all reviews
        return jsonify(harsh_grading=diffLst[0], boring=diffLst[1],
                       hard=diffLst[2], not_recommended=diffLst[3])


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

    lst = []
    # get review records from the database of this professor
    lst = db.get_entry_professor(profName)

    if len(lst) > 0:
        return jsonify(professor_name=profName, total_reviews=len(lst))
    else:
        return abort(404)


# helper function to find classes based on category
def find_class(class_type):

    # fetching all the entries in the database
    allEntries = db.get_all()

    # creating a results list to hold classes for comparison
    results = []

    count = 0
    for entry in allEntries:
        # extracting course title from entry
        className = entry[1]

        if className is not None:
            '''representing four different types of classes: art, computer science,
               math and languages. We believe these are a diverse set of
               categories which encapsulate numerous classes.
            '''

            if class_type == 'art':
                artTypes = ['Art', 'Ceramics', 'Painting',
                            'Drawing', 'Photography']
                for category in artTypes:
                    if category in className and entry[1] not in results:
                        results.append(entry[1])
                        count += 1

            if class_type == 'computer science':
                compsciTypes = ['Computer Science', 'Computing',
                                'Artificial Intelligence', 'Machine Learning']
                for category in compsciTypes:
                    if category in className and entry[1] not in results:
                        results.append(entry[1])
                        count += 1

            if class_type == 'math':
                mathTypes = ['Math', 'Calculus', 'Statistics', 'Algebra']
                for category in mathTypes:
                    if category in className and entry[1] not in results:
                        results.append(entry[1])
                        count += 1

            if class_type == 'language':
                languageTypes = ['English', 'French', 'Spanish',
                                 'Chinese', 'Italian', 'Arabic']
                for category in languageTypes:
                    if category in className and entry[1] not in results:
                        results.append(entry[1])
                        count += 1

            if count == 5:
                break
        else:
            continue
    return results


'''comparator returns courses in increasing order of comparison type'''


# helper function to compare
def compare(comparison_type, class_type):
    # first get a list of classes based upon the class_type
    classes = find_class(class_type)
    sortedLst = []
    for c in classes:
        score = 0
        if comparison_type == 'difficulty':
            score = get_difficulty(course=c, usage=2)
        if comparison_type == 'easy':
            score = get_easy(course=c, usage=2)
        if comparison_type == 'final':
            score = get_final(course=c, usage=2)

        classScore = (c, score)
        sortedLst.append(classScore)

    # sort based off of score
    sortedLst.sort(key=lambda x: x[1])
    return sortedLst


'''
'classes' endpoint
Method Type: GET
return: list of desired classes for given category
requires: class type and desired comparator style
'''


@app.route('/classes', methods=['GET'])
def classes():
    # get class type from request URL
    classType = request.args.get('classtype')
    # get comparator from request URL
    comparator = request.args.get('comparatortype')

    if classType is not None and comparator is not None:
        # call upon find_class()
        results = compare(comparator, classType)
        # conduct appropriate comparison
        return jsonify(class_results=results)
    else:
        return abort(404)


'''
'/review_ages/<date>' endpoint
Method Type: GET
return: professor name along with the number of old/new reviews based upon date
requires: desired professor name and date
'''


@app.route('/review_ages/<date>', methods=['GET'])
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
return: sentiment analysis (eg. objective reviews) based on professor or course
requires: desired professor or course name
'''


@app.route('/sentiment', methods=['GET'])
def sentiment_analysis():
    # get professor name from request URL
    profName = request.args.get('profname')
    # get course title from request URL
    course = request.args.get('course')
    # get review records from the database of this prof or class
    lst = []
    if profName is not None and profName != "":
        lst = db.get_entry_professor(profName)
    elif course is not None and course != "":
        lst = db.get_entry_class(course)
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


'''
'/recommendProfessor' endpoint
Method Type: GET
return: name of the professor with the most positive sentiment out of all
        professors for a specified course
requires: desired course name
'''


@app.route('/recommendProfessor', methods=['GET'])
def recommend_professor():

    # get course title from request URL
    course = request.args.get('course')

    # get review records from the database of this class
    course_reviews = []

    if course is not None and course != "":
        course_reviews = db.get_entry_class(course)

    if len(course_reviews) > 0:

        # get the professors that teach this course

        professors_of_course = set()

        for element in course_reviews:
            professors_of_course.add(element[0])

        # Dictionary maps each professor name to a score

        scores = dict()

        for professor in professors_of_course:

            # get review records from the database of this professor
            prof_reviews = []

            if professor is not None and professor != "":
                prof_reviews = db.get_entry_professor(professor)
                # do a sentiment analysis on this professor
                # give the prof a score
                # based on diff of positive and negative reviews

                sentiment_analysis = analysis.review_analysis(prof_reviews)

                pos_rev_count = sentiment_analysis[3]
                neg_rev_count = sentiment_analysis[4]

                score = pos_rev_count - neg_rev_count

                scores[professor] = score

        best_professor = max(scores, key=scores.get)

        return jsonify(professor_name=best_professor)

    else:
        return abort(404)


if __name__ == '__main__':
    # run Flask app
    app.run(debug=True, host='127.0.0.1')
