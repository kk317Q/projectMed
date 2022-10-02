from django.db import models
from projectMed.settings import  DATE_INPUT_FORMATS
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime    




def custom_upload_to(instance):
    return "userDocs/{}/".format(instance.username)

def illnessFilesDirectory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patientFiles/{0}/illnesses/{1}/{2}'.format(instance.illness.registry.patient.user.username, instance.illness.id, instance.fileI.name)

def treatmentFilesDirectory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patientFiles/{0}/treatments/{1}/{2}'.format(instance.treatment.registry.patient.user.username, instance.treatment.id, instance.fileT.name)

def consultancyFilesDirectory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patientFiles/{0}/consultancies/{1}/{2}'.format(instance.consultancy.consultancyPatient.user.username, instance.consultancy.id, instance.fileC.name)

def profileImageDirectory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patientProfileImage/{0}/{1}'.format(instance.user.username, instance.profileIMG.name)

def requestFilesDirectory(instance, filename):
    return 'patientFiles/{0}/requests/{1}/{2}'.format(instance.request.requestPatient.user.username, instance.request.id, instance.fileR.name)

def doctorFilesDirectory(instance, filename):
    return 'doctorFiles/{0}/{1}'.format(instance.doctor.user.username, instance.fileD.name)

class Achievement(models.Model):
    code = models.IntegerField(unique = True)
    achName = models.CharField(max_length=300)
    achLogo = models.ImageField(default='achLogos/default.jpg', null=True)

class Anamnesis(models.Model):
    placeOfBirth = models.CharField(max_length=400, blank = True)
    parentsAgeAtBirth = models.CharField(max_length=400, blank = True)
    descriptionOfBirth = models.CharField(max_length=400, blank = True)
    aboutEAT = models.CharField(max_length=400, blank = True)
    premorbidState = models.CharField(max_length=400, blank = True)
    peculiaritiesInDevelopment = models.CharField(max_length=400, blank = True)
    lifeConditions = models.CharField(max_length=400, blank = True)
    jobDescription = models.CharField(max_length=400, blank = True)
    badHabits = models.CharField(max_length=400, blank = True)
    lifeStyle = models.CharField(max_length=400, blank = True)
    dietDescription = models.CharField(max_length=400, blank = True)
    pastIllnesses = models.CharField(max_length=400, blank = True)
    surgicalInterventions = models.CharField(max_length=400, blank = True)
    hereditaryDiseases = models.CharField(max_length=400, blank = True)
    pastInfections = models.CharField(max_length=400, blank = True)
    allergicHistory = models.CharField(max_length=400, blank = True)

class Registry(models.Model):
    registryOwner = models.CharField(max_length=400, blank = True)
    
class Illness(models.Model):
    registry = models.ForeignKey(Registry, blank = True, on_delete = models.CASCADE, null = True)
    dateI = models.DateField()
    specialization = models.CharField(max_length=400)
    describtion = models.CharField(max_length=400)
    diagnose = models.CharField(max_length=400)
    active = models.BooleanField()
    documents = models.FileField(upload_to='illnessDocs/')

class Treatment(models.Model):
    registry = models.ForeignKey(Registry, blank = True, on_delete = models.CASCADE, null = True)
    dateT = models.DateField( )
    specialization = models.CharField(max_length=400)
    describtion = models.CharField(max_length=400)
    methodology = models.CharField(max_length=400)
    result = models.CharField(max_length=400)
    documents = models.FileField(upload_to='illnessDocs/') #Trearment Docs???



class RegisteredUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique = True)
    malefemale = models.CharField(max_length=100, null = True)
    #password = models.CharField(max_length=1000)
    #firstName = models.CharField(max_length=100)
    #citation = models.CharField(max_length=100)
    dob = models.DateField()
    telphone = models.CharField(max_length=400)
    location = models.CharField(max_length=100)
    profileIMG = models.ImageField(default='patientIcon.png', upload_to=profileImageDirectory, null=True)
    documents = models.FileField(upload_to=custom_upload_to)


class Doctor(RegisteredUser):
    education = models.CharField(max_length=500)
    aboutMe = models.CharField(max_length=500)
    specialization = models.CharField(max_length=100)
    experience =  models.DateField(null=True)
    work = models.CharField(max_length=500, null=True)
    phoneNumber = models.CharField(max_length=100,null = True) #Delete it
    rating = models.IntegerField()
    achievementStatus = models.IntegerField()


class Patient(RegisteredUser):
    likedDoctors = models.ManyToManyField(Doctor, related_name='likesOnDoc')
    favouriteDoctors = models.ManyToManyField(Doctor, related_name='favouritesOnDoc')
    rating = models.IntegerField()
    anamnesis = models.OneToOneField(Anamnesis,on_delete = models.CASCADE)
    registry = models.OneToOneField(Registry, on_delete = models.CASCADE)

class Request(models.Model):
    requestDate = models.DateTimeField()
    requestPatient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    targetDoctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    message = models.CharField(max_length=400)
    documents = models.CharField(max_length=700) #Delete
    status = models.CharField(max_length=200)


class Consultancy(models.Model):
    consultancyStartDate = models.DateTimeField(default = datetime.now)
    consultancyEndDate = models.DateTimeField(null = True)
    consultancyPatient = models.ForeignKey(Patient, on_delete = models.SET_NULL, null = True   )
    consultancyDoctor = models.ForeignKey(Doctor, on_delete = models.SET_NULL, null = True   )
    patientMessage = models.CharField(max_length=700, null = True)
    doctorComments = models.CharField(max_length=700, null = True)
    doctorConclusion = models.CharField(max_length=700, null = True)
    status = models.CharField(max_length=700) #Active/Closed/Dispute/Awaiting
    closeStatusPatient = models.BooleanField(default = False) 
    closeStatusDoctor = models.BooleanField(default = False)

class Chat(models.Model):
    consultancy = models.OneToOneField(Consultancy, on_delete = models.CASCADE)
    countMSG = models.IntegerField(null = True)

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    author = models.ForeignKey(RegisteredUser, on_delete = models.CASCADE)  
    authorType = models.CharField(max_length=1000) #Doctor/Patient DELETE
    messageText = models.CharField(max_length=1000)
    datePosted = models.DateTimeField(default = datetime.now())


class DoctorFile(models.Model):
    fileD = models.FileField(upload_to=doctorFilesDirectory, null=True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)


class IllnessFile(models.Model):
    fileI = models.FileField(upload_to=illnessFilesDirectory, null=True)
    illness = models.ForeignKey(Illness, on_delete = models.CASCADE)

class TreatmentFile(models.Model):
    fileT = models.FileField(upload_to=treatmentFilesDirectory, null=True)
    treatment = models.ForeignKey(Treatment, on_delete = models.CASCADE) 

class ConsultancyFile(models.Model):
    fileC = models.FileField(upload_to=consultancyFilesDirectory, null=True)
    consultancy = models.ForeignKey(Consultancy, on_delete = models.CASCADE) 
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

class RequestFile(models.Model):
    fileR = models.FileField(upload_to=requestFilesDirectory, null=True)
    request = models.ForeignKey(Request, on_delete = models.CASCADE) 

class Moderator(models.Model):
    employeeID = models.CharField(max_length=400, primary_key = True)
    password = models.CharField(max_length=1000) #Delete
    firstName =  models.CharField(max_length=400) #Delete
    secondName =  models.CharField(max_length=400) #Delete

class Enquiry(models.Model):
    enquiryID = models.CharField(max_length=400, primary_key = True)
    username = models.ForeignKey(RegisteredUser, on_delete = models.CASCADE)
    moderator = models.ForeignKey(Moderator, blank = True, on_delete = models.CASCADE)
    topic = models.CharField(max_length=400)
    body = models.CharField(max_length=400)
    enquiryDate = models.DateTimeField()
    status = models.IntegerField()

class reviewDoctor(models.Model):
    targetDoctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    authorPatient = models.ForeignKey(Patient, on_delete = models.SET_NULL, null = True)
    reviewText = models.CharField(max_length=2000)
    dateOfPublish = models.DateField(default = datetime.now, blank = True)
    stars = models.IntegerField()

#Liking


#Articles section

class Article(models.Model):
    title = models.CharField(max_length=400)
    body = models.CharField(max_length=10000)
    articleIMG = models.ImageField(default='articleIMG/default.jpg', upload_to="articleIMG/", null=True)
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctorsArticles')
    datePosted = models.DateField(default = datetime.now)
    approved = models.BooleanField()
    numOfApprovals = models.IntegerField()
    numOfDisapprovals = models.IntegerField(default = 0)
    usersLiked = models.ManyToManyField(RegisteredUser, related_name='likedArticle')
    usersFaved = models.ManyToManyField(RegisteredUser, related_name='favouriteArticle')
    doctorsApprove = models.ManyToManyField(Doctor, related_name='approvedArticles')
    doctorsDisapprove = models.ManyToManyField(Doctor, related_name='disapprovedArticles')
    rating = models.IntegerField(default = 5)


class reviewArticle(models.Model): #Review Article/DOctors should have one super class as to class diagramm!
    author = models.ForeignKey(RegisteredUser, on_delete = models.CASCADE, related_name='usersReviewOnArticle')
    authorType = models.CharField(max_length = 100)
    article = models.ForeignKey(Article, on_delete = models.CASCADE, null = True)
    datePosted =  models.DateField(default = datetime.now())
    body = models.CharField(max_length=1000)
    stars = models.IntegerField()

class respondComment(models.Model):
    author = models.ForeignKey(RegisteredUser, on_delete = models.CASCADE)
    authorType = models.CharField(max_length = 100)
    datePosted =  models.DateField(default = datetime.now())
    body = models.CharField(max_length=1000, null = True)
    reviewArticle = models.ForeignKey(reviewArticle, on_delete = models.CASCADE)




