from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Questionnaire, Question, Answer

from .serializers import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

class QuestionnairesAdminViewSet(viewsets.ModelViewSet):

    queryset = Questionnaire.objects.all().order_by('start_date')
    serializer_class = QuestionnaireSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, pk=None):

        questionnaire = Questionnaire.objects.get(pk=pk)
        request.data['start_date'] = questionnaire.start_date
        if "title" not in request.data:
            request.data['title'] = questionnaire.title
        if 'description' not in request.data:
            request.data['description'] = questionnaire.description
        if 'stop_date' not in request.data:
            request.data['stop_date'] = questionnaire.stop_date
        serializer = QuestionnaireSerializer(questionnaire, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        questionnaire = Questionnaire.objects.get(pk=pk)
        questionnaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def active(self, request):
        data_set =[elem for elem in Questionnaire.objects.all() if elem.is_active]
        serializer = QuestionnaireSerializer(data_set, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def questions(self, request, pk=None):
        questionnaire = Questionnaire.objects.get(pk=pk)
        questions = Question.objects.filter(questionnaire_id=questionnaire.id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionsViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, pk=None):
        questionnaire = get_object_or_404(Questionnaire.objects, pk=pk)

        if not questionnaire.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(questionnaire_id=questionnaire.id)
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)

    def update(self, request, pk=None):
        question = Question.objects.get(pk=pk)

        request.data['questionnaire_id'] = question.questionnaire_id.id


        if 'question_text' not in request.data:
            request.data['question_text'] = question.question_text
        if 'question_type' not in request.data:
            request.data['question_type'] = question.question_type
        print(request.data)
        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionnairesViewSet(viewsets.ModelViewSet):

    #serializer_class = QuestionnaireSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request):

        questionnaires = [elem for elem in Questionnaire.objects.all() if elem.is_active]
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        questionnaire = get_object_or_404(Questionnaire.objects, pk=pk)

        if not questionnaire.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(questionnaire_id=questionnaire.id)
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)


    def post(self, request, pk=None):

        try:

            questionnaire = Questionnaire.objects.get(pk=pk)
            if not questionnaire.is_active:
                return Response(status=status.HTTP_204_NO_CONTENT)
            question = Question.objects.get(questionnaire_id=questionnaire, id=request.data['question'])
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

        user_id = request.user.id

        if user_id == None:
            user_id = 0

        data = {"question": question.id,
                "answer_text": request.data["answer_text"],
                "user_id": user_id
                }

        serializer = AnswerSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @action(detail=False)
    def completed(self, request):
        user_id = request.user.id
        if user_id == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data_set = [elem for elem in Questionnaire.objects.all() if elem.is_completed(user_id)]
        serializer = QuestionnaireSerializer(data_set, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def answers(self, request, pk=None):
        user_id = request.user.id
        if user_id == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user_answers = []
        try:
            questionnaire = Questionnaire.objects.get(pk=pk)
        except:
            return Response(QuestionnaireSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.filter(questionnaire_id=questionnaire)
        for elem in question:
            user_answers += Answer.objects.filter(question=elem, user_id=user_id)
        serializer = AnswerSerializer(user_answers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def answers_all(self, request):
        user_id = request.user.id
        if user_id == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user_answers = Answer.objects.filter(user_id=user_id)

        serializer = AnswerSerializer(user_answers, many=True)
        return Response(serializer.data)
