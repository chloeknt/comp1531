'''
Tests for the lecture question asking service.
'''
from questions import submit, like, dismiss, questions, clear

def test_simple():
    clear()
    q1 = submit("How long is a piece of string?")
    q2 = submit("What's your shoe size?")
    like(q1)
    assert questions() == [
        {"id": q1, "question": "How long is a piece of string?", "likes": 1},
        {"id": q2, "question": "What's your shoe size?", "likes": 0}]

# Write your tests here
