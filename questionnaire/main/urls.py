from rest_framework import routers
from .views import QuestionsViewSet, QuestionnairesAdminViewSet, QuestionnairesViewSet, CreateAnswerViewSet

router = routers.DefaultRouter()
router.register('api/questionnaires/admin', QuestionnairesAdminViewSet, 'questionnairesadmin')
router.register('api/questions', QuestionsViewSet, 'questions')
router.register('api/questionnaires', QuestionnairesViewSet, 'questionnaires')
router.register('api/createanswer', CreateAnswerViewSet, 'createanswer')

urlpatterns = router.urls
