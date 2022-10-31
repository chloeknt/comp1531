'''
The backend for the lecture question asking application.

Each question is assigned an ID number when it is submitted to the app. This ID
can then be used to like and dismiss the question. The numbers are always
positive, but otherwise follow no defined ordering or structure. Questions have
the same ID from when they are submitted till they are dismissed.

When questions are first submitted, they have 0 likes.
'''
q_ids = []
questions = []
# Put any global variables your implementation needs here

def submit(question):
    '''
    Submits a question to the service.

    Returns the ID of the question but yields a ValueError if question is an
    empty string or exceeds 280 characters in length.
    '''
    if len(question) > 280:
        raise ValueError("Question is too long")
    if question = '':
        raise ValueError("Question is empty")

    q_id = len(q_ids)
    q_ids.append(q_id)
    q_dict = {'id' : q_id, 'question' : question, 'likes' : 0}
    questions.append(q_dict)

    return q_id


def questions():
    '''
    Returns a list of all the questions.

    Each question is represented as a dictionary of {id, question, likes}.

    The list is in order of likes, with the most liked questions first. When
    questions have the same number of "likes", their order is not defined.
    '''
    # Hint: For this question, there are still marks available if the returned
    # list is in the wrong order, so do not focus on that initially.
    sorted_questions = sorted(questions.items(), key=lambda x:x[1])
    return sorted_questions

def clear():
    '''
    Removes all questions from the service.
    '''
    questions = []

def like(id):
    '''
    Adds one "like" to the question with the given id.

    It does not return anything but raises a KeyError if id is not a valid
    question ID.
    '''
    if id < 0:
        raise KeyError("Id must be positive")
    if questions = []:
        raise KeyError("No questions")
    if len(questions) - 1 < id:
        raise KeyError("Invalid question id")
    if questions[id]['id'] == -1:
        raise KeyError("Question has been dismissed")

    questions[id]['likes'] += 1


def dismiss(id):
    '''
    Removes the question from the set of questions being stored.

    It does not return anything but raises a KeyError if id is not a valid
    question ID.
    '''
    if id < 0:
        raise KeyError("Id must be positive")
    if questions = []:
        raise KeyError("No questions")
    if len(questions) - 1 < id:
        raise KeyError("Invalid question id")
    if questions[id]['id'] == -1:
        raise KeyError("Question has been dismissed")

    questions[id]['id'] = -1
