"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    project_and_grade = hackbright.get_grades_by_github(github)

    # return "{} is the GitHub account for {} {}".format(github, first, last)

    return render_template('student_info.html', 
                            first=first, 
                            last=last, 
                            github=github,
                            project_and_grade=project_and_grade)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")



@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template('student_add.html')


@app.route("/add-confirmation", methods=['POST'])
def send_confirmation():
    '''Confirms student has been added'''

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('add_confirmation.html', github=github)


@app.route('/get-project-title')
def get_project_title():
    '''Get project title'''

    return render_template('get_project_title.html')

@app.route('/project')
def show_project():
    '''Show project info when given title'''

    project_title = request.args.get('project_title')

    title, description, max_grade = hackbright.get_project_by_title(project_title)

    #return list of tuples
    github_and_grade = hackbright.get_grades_by_title(project_title) 


    return render_template('project_info.html', 
                            title=title, 
                            description=description, 
                            max_grade=max_grade, 
                            github_and_grade=github_and_grade)




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
