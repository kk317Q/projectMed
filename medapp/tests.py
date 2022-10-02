from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.contrib.auth.models import User




# Create your tests here.

class LogInTest(TestCase):

    def setUp(self):
        # Установки запускаются перед каждым тестом
        pass
    
    def tearDown(self):
        # Очистка после каждого метода
        pass

    def testLoginPage(self):

        print('   ')
        print('----------------------------------------------------')
        print('--------------------testLoginPage()-----------------')
        print('----------------------------------------------------')
        print('   ')

        client = Client()

       
        # send GET request.
        response = client.get('/goLogIn')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medapp/logIn.html')

        print('Response status code : ' + str(response.status_code))
        print('Login page is received')

        
    def testAuthentication(self):

        print('   ')
        print('----------------------------------------------------')
        print('--------------------testAuthentication()-----------------')
        print('----------------------------------------------------')
        print('   ')

        client = Client()
        testLoginCredentials = {'usernameInput':'khuseyn', 'password':'khuseyn'}
        # send POST request.
        response = client.post(path='/logIn', data=testLoginCredentials)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn( "This pair of username/password was not found!", response) 
        
        print('Response status code : ' + str(response.status_code))
        print('Successfull Authentication')



   


 

 