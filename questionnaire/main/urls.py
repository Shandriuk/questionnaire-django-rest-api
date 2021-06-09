from rest_framework import routers
from .views import QuestionsViewSet, QuestionnairesAdminViewSet, QuestionnairesViewSet

router = routers.DefaultRouter()
router.register('api/questionnaires/admin', QuestionnairesAdminViewSet, 'questionnairesadmin')
router.register('api/questions/admin', QuestionsViewSet, 'questions')
router.register('api/questionnaires', QuestionnairesViewSet, 'questionnaires')

urlpatterns = router.urls