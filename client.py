# RET_QUIT = 1
# RET_NORMAL = 0
import requests
URL = 'http://127.0.0.1:5000'

filter_keys = ['classtype', 'comparatortype']
filter_descriptor = ["classtype", "comparatortype"]
filter_msg = ["select a classtype",
              "select a comparatortype"]
filter_legit_input = [['math', 'computer science', 'art', 'language'],
                      ['difficulty', 'easy', 'final']]


def printMessage(msg: str) -> None:
    print("################")
    print(msg)
    print("################")


def getKeyboardInput(caseSensative=False) -> str:
    if caseSensative:
        return input().strip()
    return input().strip().lower()


def validate_input(input: str, valid_input: list) -> bool:
    if not valid_input:
        return True
    return input in valid_input


def menuEditFilter(filters: dict, filter_id: int) -> None:
    while True:
        filter_key = filter_keys[filter_id]
        if filter_key in filters:
            # filter already filled, needs to ask if clear
            print("1) modify filter")
            print("2) clear filter")
            print("b) Back")
            print("please choose an option:", end="")
            cmd = getKeyboardInput()
            if cmd == "b":
                return
            elif cmd == "2":
                del filters[filter_key]
                return
            elif cmd == "1":
                pass
            else:
                # error handling
                printMessage("invalid input")
                continue

        if filter_legit_input[filter_id]:
            for legit in filter_legit_input[filter_id]:
                print(f"- {legit}")
        print(filter_msg[filter_id] + ": ", end="")
        keyword = getKeyboardInput()
        if validate_input(keyword, filter_legit_input[filter_id]):
            filters[filter_key] = keyword
        else:
            printMessage("invalid input")
        return


def menuSelectFilter() -> dict:
    filters = dict()
    while True:
        for i, filter in enumerate(filter_keys):
            print(f"{i+1}) {filter_descriptor[i]} " +
                  f"({filters.get(filter, 'empty')})")

        if len(filters) == 2:
            # classtype and comparatortype are filled
            print("a) Apply filter and search")
        print("b) Back")
        print("please select a filter: ", end="")
        cmd = getKeyboardInput()

        if cmd == "b":
            return None
        elif len(filters) > 0 and cmd == "a":
            return filters
        elif len(cmd) == 1 and ("1" <= cmd <= "5"):
            filter_id = int(cmd) - 1
            menuEditFilter(filters, filter_id)
        else:
            printMessage("invalid input")


def menuSelectSource(filters: set) -> str:
    page = 0
    page_size = 10
    courses = []

    if "classtype" and "comparatortype" in filters.keys():
        p = {'classtype': str(filters.get("classtype")),
             'comparatortype': str(filters.get("comparatortype"))}
        resp = requests.get(url=URL+"/classes", params=p)
        courses = resp.json()['class_results']

    if len(courses) == 0:
        print("No courses found")
        return None

    pages = len(courses) // page_size
    if len(courses) % page_size:
        pages += 1

    while True:
        for i in range(page_size*page, min(page_size*(page+1), len(courses))):
            print(f"{i+1:4d}) {courses[i][0]} (score: {courses[i][1]})")

        if page > 0:
            print("p) previous page")
        if page < pages-1:
            print("n) next page")
        print("b) Back")

        print(f"please select a course (page {page+1}/{pages}): ", end="")
        cmd = getKeyboardInput()
        if cmd == "b":
            return None
        elif page > 0 and cmd == "p":
            page -= 1
        elif page < pages-1 and cmd == "n":
            page += 1
        elif cmd.isnumeric():
            id = int(cmd) - 1
            if id < len(courses):
                return courses[id][0]
            else:
                printMessage("invalid input")
        else:
            printMessage("invalid input")


def menuAddCourse() -> object:
    filters = menuSelectFilter()
    if filters is None:
        return None
    return menuSelectSource(filters)


def showCourses(courses: set) -> None:
    if len(courses) == 0:
        printMessage("You haven't added any courses")
        return

    id = 1
    print("You have added the following courses:")
    for c in courses:
        print(f'{id}) {c}')
        id += 1


def menuDropCourse(courses: set) -> set:
    course_list = list(courses)
    while True:
        if len(course_list) == 0:
            printMessage("You haven't added any courses")
            return set(course_list)

        for i, course in enumerate(course_list):
            print(f"{i+1}) {course}")
        print("b) Back")
        print("please select a course to drop: ", end="")
        cmd = getKeyboardInput()

        if cmd == "b":
            return set(course_list)
        elif len(cmd) == 1 and ("1" <= cmd <= "6"):
            course_id = int(cmd) - 1
            if course_id < len(course_list):
                del course_list[course_id]
        else:
            printMessage("invalid input")


def pressAnyKey():
    print("press ENTER to continue...")
    input()


def getProfReview():
    print("Please enter the professor's name:", end="")
    prof = getKeyboardInput(True)
    params = dict(profname=prof)

    try:
        resp = requests.get(url=URL+"/total_reviews", params=params)
        data = resp.json()
        print(f"Professor's Name: {data['professor_name']}")
        print(f"Total Reviews: {data['total_reviews']}")
        resp = requests.get(url=URL+"/sentiment", params=params)
        data = resp.json()
        print(f"  Positive Reviews: {data['positive_reviews']}")
        print(f"  Neutral Reviews: {data['neutral_reviews']}")
        print(f"  Negative Reviews: {data['negative_reviews']}")
        print(f"  Objective Reviews: {data['objective_reviews']}")
        print(f"  Subjective Reviews: {data['subjective_reviews']}")
        resp = requests.get(url=URL+"/extensions", params=params)
        data = resp.json()
        print(f"Extension Status: {data['extension_status']}")
        resp = requests.get(url=URL+"/easy", params=params)
        data = resp.json()
        print(f"# of mentioning easy: {data['easy_A']}")
        print(f"# of mentioning A+: {data['A_plus']}")
        print(f"# of mentioning lenient grading: {data['lenient_grading']}")
        print(f"# of mentioning I recommend: {data['I_recommend']}")
        resp = requests.get(url=URL+"/difficulty", params=params)
        data = resp.json()
        print(f"# of mentioning harsh grading: {data['harsh_grading']}")
        print(f"# of mentioning boring: {data['boring']}")
        print(f"# of mentioning hard: {data['hard']}")
        print(f"# of mentioning not recommend: {data['not_recommended']}")

        pressAnyKey()
        resp = requests.get(url=URL+"/professor", params=params)
        data = resp.json()
        print("====== Random Review ======")
        print(f"Course: {data['reviews'][1]}")
        print(f"Date: {data['reviews'][2]}")
        print(f"Review: {data['reviews'][3]}")
        print(f"Worload: {data['reviews'][4]}")
        print(f"Agree: {data['reviews'][5]}")
        print(f"Disagree: {data['reviews'][6]}")
        print(f"Funny: {data['reviews'][7]}")
    except Exception:
        printMessage(f"Couldn't find the professor {prof}")
    pressAnyKey()


def getCourseReview():
    print("Please enter the course title:", end="")
    course = getKeyboardInput(True)
    params = dict(course=course)

    try:
        resp = requests.get(url=URL+"/sentiment", params=params)
        data = resp.json()
        print(f"  Positive Reviews: {data['positive_reviews']}")
        print(f"  Neutral Reviews: {data['neutral_reviews']}")
        print(f"  Negative Reviews: {data['negative_reviews']}")
        print(f"  Objective Reviews: {data['objective_reviews']}")
        print(f"  Subjective Reviews: {data['subjective_reviews']}")
        resp = requests.get(url=URL+"/recommendProfessor", params=params)
        data = resp.json()
        print(f"Recommended Professor: {data['professor_name']}")
        resp = requests.get(url=URL+"/easy", params=params)
        data = resp.json()
        print(f"# of mentioning easy: {data['easy_A']}")
        print(f"# of mentioning A+: {data['A_plus']}")
        print(f"# of mentioning lenient grading: {data['lenient_grading']}")
        print(f"# of mentioning I recommend: {data['I_recommend']}")
        resp = requests.get(url=URL+"/difficulty", params=params)
        data = resp.json()
        print(f"# of mentioning harsh grading: {data['harsh_grading']}")
        print(f"# of mentioning boring: {data['boring']}")
        print(f"# of mentioning hard: {data['hard']}")
        print(f"# of mentioning not recommend: {data['not_recommended']}")
    except Exception:
        printMessage(f"Couldn't find the course {course}")
    pressAnyKey()


def main():
    courses = set()
    printMessage('Welcome to CU course wizard.')
    while True:
        print('============================')
        print("1) Add a course")
        print("2) Drop a course")
        print("3) List selected courses")
        print("4) Look up for a professor")
        print("5) Look up for a course")
        print("q) Quit")
        print("please choose an option:", end="")
        cmd = input()
        if cmd == "1":
            ret = menuAddCourse()
            if ret is not None:
                courses.add(ret)
                printMessage(f"{ret} is added")
        elif cmd == "2":
            courses = menuDropCourse(courses)
        elif cmd == "3":
            showCourses(courses)
        elif cmd == "4":
            getProfReview()
        elif cmd == "5":
            getCourseReview()
        elif cmd == "q":
            return
        else:
            printMessage("invalid input")


if __name__ == "__main__":
    main()
