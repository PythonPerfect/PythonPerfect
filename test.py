
#Python package functions are ommitted from testing 
import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from app.controller import *

class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #User Table Tests
    def test_addNewUser(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        u2 = add_new_user('TestUser2', 'testuser2@example.com', 'testuser2123')
        us = get_all_user()
        self.assertEqual(u1, us[0])
        self.assertEqual(u2, us[1])
    
    def test_addNewAdmin(self):
        ad1 = add_new_admin('TestAdmin1', 'testadmin1@example.com', 'testadmin1123')
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        self.assertTrue(ad1.admin)
        self.assertFalse(u1.admin)

    def test_deleteUser(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        ad1 = add_new_admin('TestAdmin1', 'testadmin1@example.com', 'testadmin1123')
        size = len(get_all_user())
        self.assertEqual(2, size)
        delete_user(u1)
        size = len(get_all_user())
        self.assertEqual(1, size)

    def test_checkPassword(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'correctpassword123')
        self.assertTrue(u1.check_password('correctpassword123'))
        self.assertFalse(u1.check_password('incorrectpassword123'))


    #For Course Model
    def test_addNewCourse(self):
        cour1 = add_new_course('TestCourse1')
        cour2 = add_new_course('TestCourse2')
        cours = get_all_courses()
        self.assertEqual(cour1, cours[0])
        self.assertEqual(cour2, cours[1])

    def test_deleteCourse(self):
        cour1 = add_new_course('TestCourse1')
        cour2 = add_new_course('TestCourse2')
        size = len(get_all_courses())
        self.assertEqual(2, size)
        delete_course(cour1)
        size = len(get_all_courses())
        self.assertEqual(1, size)

    #For Content Model
    def test_addNewContent(self):
        cour1 = add_new_course('TestCourse1')
        cour2 = add_new_course('TestCourse2')
        con1 = add_new_content('TestCon1', 'This is test content1', cour1)
        con2 = add_new_content('TestCon2', 'This is test content2', cour2)
        cons = get_all_content()
        self.assertEqual(con1, cons[0])
        self.assertEqual(con2, cons[1])

    def test_deleteCourse(self):
        cour1 = add_new_course('TestCourse1')
        con1_1 = add_new_content('TestCon1_1', 'This is test content1_1', cour1)
        con1_2 = add_new_content('TestCon1_2', 'This is test content1_2', cour1)
        size = len(get_contents_by_course(cour1))
        self.assertEqual(2, size)
        delete_content(con1_1)
        size = len(get_contents_by_course(cour1))
        self.assertEqual(1, size)

    #For Quiz Model
    def test_addNewQuiz(self):
        cour1 = add_new_course('TestCourse1')
        cour2 = add_new_course('TestCourse2')
        q1 = add_new_quiz('TestQ1', cour1)
        q2 = add_new_quiz('TestQ2', cour2)
        qs = get_all_quiz()
        self.assertEqual(q1, qs[0])
        self.assertEqual(q2, qs[1])

    def test_deleteQuiz(self):
        cour1 = add_new_course('TestCourse1')
        q1_1 = add_new_quiz('TestQ1_1', cour1)
        q1_2 = add_new_quiz('TestQ1_2', cour1)
        size = len(get_quiz_by_course(cour1))
        self.assertEqual(2, size)
        delete_quiz(q1_1)
        size = len(get_quiz_by_course(cour1))
        self.assertEqual(1, size)

    #For Question Model
    def test_addNewQuestion(self):
        cour1 = add_new_course('TestCourse1')
        q1 = add_new_quiz('TestQ1', cour1)
        que1 = add_new_question('TestQuestion1?', 'TestAnswer1', q1)
        que2 = add_new_question('TestQuestion2?', 'TestAnswer2', q1)
        ques = get_all_question()
        self.assertEqual(que1, ques[0])
        self.assertEqual(que2, ques[1])

    def test_deleteQuestion(self):
        cour1 = add_new_course('TestCourse1')
        q1 = add_new_quiz('TestQ1', cour1)
        que1 = add_new_question('TestQuestion1?', 'TestAnswer1', q1)
        que2 = add_new_question('TestQuestion2?', 'TestAnswer2', q1)
        size = len(get_all_question())
        self.assertEqual(2, size)
        delete_from_database(que1)
        size = len(get_all_question())
        self.assertEqual(1, size)

    #For Question_Response Model
    def test_addNewQuestion_Response(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        cour1 = add_new_course('TestCourse1')
        q1 = add_new_quiz('TestQ1', cour1)
        que1 = add_new_question('TestQuestion1?', 'TestAnswer1', q1)
        que2 = add_new_question('TestQuestion2?', 'TestAnswer2', q1)
        q_r1 = add_new_question_response('This is a response', que1, u1)
        q_r2 = add_new_question_response('This is a response', que2, u1)
        q_rs = get_all_question_response()
        self.assertEqual(q_r1, q_rs[0])
        self.assertEqual(q_r2, q_rs[1])
    
    def test_correctResponse(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        cour1 = add_new_course('TestCourse1')
        q1 = add_new_quiz('TestQ1', cour1)
        que1 = add_new_question('TestQuestion1?', 'CorrectAnswer1', q1)
        q_r1 = add_new_question_response('CorrectAnswer1', que1, u1)
        self.assertTrue(q_r1.check_correct())


    def test_deleteNewQuestion_Response(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        cour1 = add_new_course('TestCourse1')
        q1 = add_new_quiz('TestQ1', cour1)
        que1 = add_new_question('TestQuestion1?', 'TestAnswer1', q1)
        que2 = add_new_question('TestQuestion2?', 'TestAnswer2', q1)
        q_r1 = add_new_question_response('This is a response', que1, u1)
        q_r2 = add_new_question_response('This is a response', que2, u1)
        q_r_test = len(get_all_question_response())
        self.assertEqual(2, q_r_test)
        delete_question_response(u1, que1)
        q_r_test = len(get_all_question_response())
        self.assertEqual(1, q_r_test)

    #For Content_Viewed Model
    def test_addNewContent_Viewed(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        cour1 = add_new_course('TestCourse1')
        con1 = add_new_content('TestCon1', 'This is test content1', cour1)
        c_v = add_new_content_viewed(u1, con1)
        c_v_test = get_user_content_viewed(u1, con1)
        self.assertEqual(c_v, c_v_test)

    def test_deleteContent_Viewed(self):
        u1 = add_new_user('TestUser1', 'testuser1@example.com', 'testuser1123')
        cour1 = add_new_course('TestCourse1')
        con1 = add_new_content('TestCon1', 'This is test content1', cour1)
        c_v = add_new_content_viewed(u1, con1)
        delete_all_content_viewed()
        c_v_test = len(get_all_content_viewed())
        self.assertEqual(0, c_v_test)

if __name__ == '__main__':
    unittest.main()