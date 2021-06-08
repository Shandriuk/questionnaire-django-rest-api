from rest_framework import serializers
from .models import Questionnaire, Question, Answer

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['title', 'description', 'start_date', 'stop_date', 'id']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['questionnaire_id', 'question_text', 'question_type', 'id']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text', 'user_id']