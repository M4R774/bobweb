from django.test import TestCase
import datetime
from .models import Question

class QuestionModelTest(TestCase):

    def test_saving_and_retrieving_question(self):
        first_question = Question()
        first_question.question_text = "Tää on kyssäri jossa vaikka ja mitä merkkejä :ßð}ʒ}ð×æ"
        first_question.pub_date = datetime.datetime.now()
        first_question.save()

        second_question = Question()
        second_question.question_text = "Lisäm kysymyksiä"
        second_question.pub_date = datetime.datetime.now()
        second_question.save()

        saved_questions = Question.objects.all()
        self.assertEqual(saved_questions.count(), 2)

        first_saved_question = saved_questions[0]
        second_saved_question = saved_questions[1]

        self.assertEqual(first_saved_question.question_text, \
                         "Tää on kyssäri jossa vaikka ja mitä merkkejä :ßð}ʒ}ð×æ")
        self.assertEqual(second_saved_question.question_text, "Lisäm kysymyksiä")
