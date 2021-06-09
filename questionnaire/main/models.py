from django.db import models
import datetime
# Create your models here.


class Questionnaire(models.Model):
    title = models.CharField("title", max_length=100)
    description = models.TextField("description", blank=True)
    start_date = models.DateField("start_date")
    stop_date = models.DateField("stop_date")

    def __str__(self):
        return f'title :{self.title}, questionnaire_id: {self.id}'

    @property
    def is_active(self):

        return self.start_date <= datetime.date.today() <= self.stop_date

    def is_completed (self, user_id):
        questions = Question.objects.filter(questionnaire_id=self)
        if len(questions)==0:
            return False
        for elem in questions:
            answers = Answer.objects.filter(question=elem, user_id=user_id)
            if len(answers)==0:
                return False
        return True


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('text', 'text_only'),
        ('sc', 'single_choice'),
        ('mc', 'multiple_choices'),
    )

    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_text = models.TextField("text_of_question")
    question_type = models.CharField("type_of_question", max_length=20, choices=QUESTION_TYPE_CHOICES, default='text')

    def __str__(self):
        return f'questionnaire_id: {self.questionnaire_id}, question_id: {self.id}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField("answer_text")
    user_id = models.IntegerField()

    def __str__(self):
        return f' question : {self.question},  id: {self.id}'
