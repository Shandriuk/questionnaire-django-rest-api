### questionnaire-django-rest-api
API to create and manage questionnaire on django rest

Only auth, no registrations

# 1. questionnaires/admin/ 
### questionnaires` admin operations

    - http://0.0.0.0:8080/questionnaires/admin/ 
        - GET - view list of all questionnaires
        - POST - post {"title":"{}", "description":"{}"*, "start_date":"YYYY-MM-DD","stop_date":"YYYY-MM-DD"}
        *don`t required
    - http://0.0.0.0:8080/questionnaires/admin/id/
        - GET - view list of all questions in questionnaires["id"]
        - PUT - update questionnaires["id"] data
        - DELETE - delete questionnaires["id"]
    - http://0.0.0.0:8080/questionnaires/admin/active
        - GET - view list of active questionnaires
# 2. questions/admin/ 
### questions` admin operations

    - http://0.0.0.0:8080/questions/
        - GET - view list of all questions
        - POST - post {"questionnaire_id":" ","question_text":" ","question_type":" "} 
    - http://0.0.0.0:8080/questions/admin/id/    
        - PUT - update questions["id"] data
        - DELETE - delete questions["id"]
# 3. questionnaires/
### questionnaires` user operations     

    - http://0.0.0.0:8080/questionnaires/
        - GET - view list of active questionnaires
    - http://0.0.0.0:8080/questionnaires/answers_all
        - GET - view list of all user`s answers (only for authorised users)
    - http://0.0.0.0:8080/questionnaires/completed (only for authorised users)
        - GET - view list of completed questionnaires    
    - http://0.0.0.0:8080/questionnaires/id/
        - GET - view list of all questions in questionnaires["id"]
        - POST - answer {"question":"id","answer_text":"answer"}
    http://0.0.0.0:8080/questionnaires/id/answers
        - GET - view list of questionnaires["id"] user`s answers (only for authorised users)
 
 # Models:
   - Questionnaire:
       - title = CharField( max_length=100) 
       - description = TextField(blank=True) 
       - start_date = DateField() - can`t edit after creation
       - stop_date = DateField() 
  - Question:
     - QUESTION_TYPE_CHOICES = (('text', 'text_only'), ('sc', 'single_choice'), ('mc', 'multiple_choices'),)
     - questionnaire_id = ForeignKey(Questionnaire)
     - question_text = TextField() - question_text
     - question_type = CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='text') - question_type
  - Answer:
     - question = ForeignKey(Question) 
     - answer_text = TextField() 
     - user_id = IntegerField() - auth user id, if anonumous id = 0
    
 # Start in questionnaire folder run:
      docker-compose build
      docker-compose run createsuperuser
      docker-compose runserver
      
  Project will be available on local machine on 0.0.0.0:8080   

