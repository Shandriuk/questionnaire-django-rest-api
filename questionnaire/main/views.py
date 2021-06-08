from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Questionnaire, Question, Answer
from .permissions import IsAdminOrReadOnly
from .serializers import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer
from django.http import HttpResponseBadRequest


class QuestionnairesAdminViewSet(viewsets.ModelViewSet):

    queryset = Questionnaire.objects.all().order_by('start_date')
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAdminOrReadOnly]

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
        questions = Question.objects.filter(title=questionnaire)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionsViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, pk=None):
        question = Question.objects.get(pk=pk)

        request.data['questionnaire_id'] = question.questionnaire_id.id

        print(question.questionnaire_id)

        if 'question_text' not in request.data:
            request.data['question_text'] = question.question_text
        if 'question_type' not in request.data:
            request.data['question_type'] = question.question_type
        print(request.data)
        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionnairesViewSet(viewsets.ModelViewSet):

    queryset = [elem for elem in Questionnaire.objects.all() if elem.is_active]
    serializer_class = QuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def completed(self, request):
        user_id = request.query_params.get('user_id', 0)
        data_set = [elem for elem in Questionnaire.objects.all() if elem.is_completed(user_id)]
        serializer = QuestionnaireSerializer(data_set, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def answers(self, request):
        if "id" not in request.data:
            return HttpResponseBadRequest('please add "id" in your request')
        user_id = request.query_params.get('user_id', 0)
        user_answers = []
        try:
            questionnaire = Questionnaire.objects.get(id=request.data['id'])
        except:
            return HttpResponseBadRequest(f'No questionnaire with "id" {request.data["id"]}')
        question = Question.objects.filter(questionnaire_id=questionnaire)
        for elem in question:
            user_answers += Answer.objects.filter(question=elem, user_id=user_id)
        serializer = AnswerSerializer(user_answers, many=True)
        return Response(serializer.data)


class CreateAnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AnswerSerializer

    def create(self, request):
        if "questionnaire_id" not in request.data:
            return HttpResponseBadRequest('please add "questionnaire_id" in your request')
        if "question_id" not in request.data:
            return HttpResponseBadRequest('please add "question_id" in your request')

        try:
            questionnaire = Questionnaire.objects.get(id=request.data['questionnaire_id'])
        except:
            return HttpResponseBadRequest(f'Problems with  "questionnaire_id"')

        try:
            question = Question.objects.get(questionnaire_id=questionnaire, id=request.data['question_id'])
        except:
            return HttpResponseBadRequest(f'Problems with "question_id"')

        Answer.objects.create(
                                question=question,
                                answer_text=request.data["answer_text"],
                                user_id=request.query_params.get('user_id', 0)
                              )

        result = Answer.objects.filter(question=question, user_id=request.query_params.get('user_id', 0))
        serializer = AnswerSerializer(result, many=True)
        return Response(serializer.data)
