import pytest
from model import Question

@pytest.fixture
def question_with_choices():
    question = Question(title='What are primary colors?', max_selections=2)
    question.add_choice('Red', is_correct=True)
    question.add_choice('Green', is_correct=False)
    question.add_choice('Blue', is_correct=True)
    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=101)

def test_add_choice_with_empty_text_fails():
    question = Question(title='q1')
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice('')

def test_add_choice_with_too_long_text_fails():
    question = Question(title='q1')
    long_text = 'a' * 101
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice(long_text)

def test_adding_multiple_choices_generates_sequential_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('First choice')
    choice2 = question.add_choice('Second choice')
    
    assert choice1.id == 1
    assert choice2.id == 2

def test_remove_existing_choice_updates_list():
    question = Question(title='q1')
    question.add_choice('Choice A')
    question.add_choice('Choice B')
    
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'Choice B'

def test_remove_non_existent_choice_fails():
    question = Question(title='q1')
    question.add_choice('Choice A')
    
    with pytest.raises(Exception, match="Invalid choice id"):
        question.remove_choice_by_id(99)

def test_remove_all_choices_leaves_question_empty():
    question = Question(title='q1')
    question.add_choice('Choice A')
    question.add_choice('Choice B')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices_updates_is_correct_flag():
    question = Question(title='q1')
    question.add_choice('Choice A')
    question.add_choice('Choice B')
    
    question.set_correct_choices([2])
    
    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct

def test_correct_selected_choices_returns_only_correct_answers():
    question = Question(title='q1', max_selections=2)
    question.add_choice('Choice A', is_correct=True)
    question.add_choice('Choice B', is_correct=False)
    question.add_choice('Choice C', is_correct=True)
    
    correct_answers = question.correct_selected_choices([1, 2])
    
    assert correct_answers == [1]

def test_selecting_more_choices_than_allowed_fails():
    question = Question(title='q1', max_selections=1)
    question.add_choice('Choice A')
    question.add_choice('Choice B')
    
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([1, 2])

def test_correct_selected_choices_with_mixed_answers(question_with_choices):
    result = question_with_choices.correct_selected_choices([1, 2])
    
    assert result == [1]

def test_correct_selected_choices_with_all_correct_answers(question_with_choices):
    result = question_with_choices.correct_selected_choices([1, 3])
    
    assert result == [1, 3]

def test_remove_all_choices_clears_populated_question(question_with_choices):
    assert len(question_with_choices.choices) == 3
    
    question_with_choices.remove_all_choices()
    
    assert len(question_with_choices.choices) == 0

def test_set_correct_choices_modifies_existing_choices(question_with_choices):
    assert not question_with_choices.choices[1].is_correct
    
    question_with_choices.set_correct_choices([2])
    
    assert question_with_choices.choices[1].is_correct