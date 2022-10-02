from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
import openpyxl
from django.core.files import File
import os
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_deny, xframe_options_sameorigin
from django.core.exceptions import ValidationError
import time
from random import randint





from django.http import HttpResponse, JsonResponse
from datetime import datetime    

from django.utils import timezone


from .models import RegisteredUser, Patient, Anamnesis, Registry, Illness, Treatment, Doctor, Request, Consultancy, reviewDoctor, Article, reviewArticle, respondComment, IllnessFile, TreatmentFile, ConsultancyFile, RequestFile, DoctorFile, Chat, ChatMessage

# Create your views here.

def index(request):
    #send_mail('Пароль и Пользователь для олимпиады', str2, 'ihuseyn5@gmail.com', [firstRow[4]])
    

    #for a in Article.objects.all():
    #    a.rating = 5
    #    a.save()
    #deleteAll()

   


    print("Hi")

    #print(Doctor.objects.filter(username="kkuliev1").exists())
    #print(Doctor.objects.get(username="kkuliev1").experience)
    #print(Doctor.objects.get(username="kkuliev1").experience.year - Doctor.objects.get(username="kkuliev1").dob.year)
    
    return render (request, 'medapp/base.html')

def deleteAll():

    for c in Consultancy.objects.all():
       c.delete()

    for r in Request.objects.all():
        r.delete()    

    for rd in reviewDoctor.objects.all():
        rd.delete() 

    for ra in reviewArticle.objects.all():
        ra.delete()     

    for rc in respondComment.objects.all():
        rc.delete()               

def checkChatMessages(request):

    chatNeeded = Chat.objects.get(id = request.GET['chatID'])
    numberOfElement = len(chatNeeded.chatmessage_set.all())
    messageTextList = []
    messageDateList = []
    authorList = []

    print(int(request.GET['chatCount']))
    print(numberOfElement)
    print(int(request.GET['chatCount']) < numberOfElement)
    
    i = 0
    if int(request.GET['chatCount']) < numberOfElement:
        for c in chatNeeded.chatmessage_set.all():
            if i > int(request.GET['chatCount']) - 1:
                messageTextList.append(c.messageText)
                
                messageDateList.append(c.datePosted.strftime("%B %d %Y, %H:%M"))
                authorList.append(c.author.user.username)
            i += 1    

        for m in messageTextList:
            print(m)
        data = {'updateInfo' : "newMessageExists", 'newMessagesList' : messageTextList, 'messageDatesList' : messageDateList, 'authorList' : authorList, 'newCountValue' : numberOfElement}
        return JsonResponse(data) 

    data = {'updateInfo' : "noNew ", 'newCountValue' : numberOfElement}
    print(numberOfElement)

    print(data)
    return JsonResponse(data)     

def deleteIllness(request, illnessID):
    illnessNeeded = Illness.objects.get(id = illnessID)
    illnessNeeded.delete()

    return redirect('http://10.0.1.2/getRegistry', request)

def deleteTreatment(request, treatmentID):
    treatmentNeeded = Treatment.objects.get(id = treatmentID)
    treatmentNeeded.delete()

    return redirect('http://10.0.1.2/getRegistry', request)


def createChatMessage(request):
    chatNeeded = Chat.objects.get(id = request.POST['chatID'])
    currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))
    if Patient.objects.filter(user = currentUser.user):
        currentAuthorType = "Patient"
    elif Doctor.objects.filter(user = currentUser.user):    
        currentAuthorType = "Doctor"

    newMessage = ChatMessage(chat = chatNeeded, author = currentUser, authorType = currentAuthorType, messageText = request.POST['newMessage'])
    newMessage.save()
    chatNeeded.countMSG = chatNeeded.countMSG +  1 
    chatNeeded.save()
    print(newMessage.datePosted)
    print(newMessage.datePosted)

   

    data = {'newMessage' : newMessage.messageText, 'messageDate' : newMessage.datePosted.strftime("%B %d %Y, %H:%M")}

    return JsonResponse(data)


def checkUsername(request):

    if User.objects.filter(username = request.GET['usernameToCheck']).exists():
        data = {'checkResult' : 'Exists'}
        return JsonResponse(data)


    data = {'checkResult' : 'Free'}
    return JsonResponse(data)



def addConsultancyFiles(request):
    currentUser = User.objects.get(username = request.user.username)
    consultancyNeeded = Consultancy.objects.get(id = request.POST['consultancyID'])
    sentFiles = request.FILES.getlist('consultancyFiles')

    for f in sentFiles:
        newConsultancyFile = ConsultancyFile(fileC = f, consultancy = consultancyNeeded, author = request.user)
        #initial_path = newIllnessFile.fileI.path
        #new_path = settings.MEDIA_ROOT + 'patientFiles' + str(currentPatient.user.username)
        #os.rename(initial_path, new_path)
        newConsultancyFile.save()

    return redirect('http://10.0.1.2/getConsultancy/' + str(consultancyNeeded.id) + '/', request)

def deleteConsultancyFile(request, consultancyFileID):
    consultancyFile = ConsultancyFile.objects.get(id = consultancyFileID)
    ConsultancyFile.objects.filter(id = consultancyFileID).delete()
    

    return redirect('http://10.0.1.2/getConsultancy/' + str(consultancyFile.consultancy.id) + '/', request)

def addTreatmentFiles(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    treatmentNeeded = Treatment.objects.get(id = request.POST['treatmentID'])
    sentFiles = request.FILES.getlist('treatmentFiles')

    for f in sentFiles:
        newTreatmentFile = TreatmentFile(fileT = f, treatment = treatmentNeeded)
        #initial_path = newIllnessFile.fileI.path
        #new_path = settings.MEDIA_ROOT + 'patientFiles' + str(currentPatient.user.username)
        #os.rename(initial_path, new_path)
        newTreatmentFile.save()

    return redirect('http://10.0.1.2/getRegistry')

def deleteTreatmentFile(request, treatmentFileID):
    TreatmentFile.objects.filter(id = treatmentFileID).delete()

    return redirect('http://10.0.1.2/getRegistry', request)


def addIllnessFiles(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    illnessNeeded = Illness.objects.get(id = request.POST['illnessID'])
    sentFiles = request.FILES.getlist('illnessFiles')

    for f in sentFiles:
        newIllnessFile = IllnessFile(fileI = f, illness = illnessNeeded)
        #initial_path = newIllnessFile.fileI.path
        #new_path = settings.MEDIA_ROOT + 'patientFiles' + str(currentPatient.user.username)
        #os.rename(initial_path, new_path)
        newIllnessFile.save()

    return redirect('http://10.0.1.2/getRegistry', request)

def deleteIllnessFile(request, illnessFileID):
    IllnessFile.objects.filter(id = illnessFileID).delete()
    
    return redirect('http://10.0.1.2/getRegistry', request)

def addDoctorsFiles(request):
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    filesSent = request.FILES.getlist('doctorFiles')    
    for f in filesSent:
        newDoctorFile = DoctorFile(fileD = f, doctor = currentDoctor)
        newDoctorFile.save()
        
    return redirect('http://10.0.1.2/getProfile', request)


def deleteDoctorFile(request, doctorFileID):
    DoctorFile.objects.filter(id = doctorFileID).delete()

    return redirect('http://10.0.1.2/getProfile', request)





def addRequestFiles(request):
    requestNeeded = Request.objects.get(id = request.POST['requestID'])
    filesSent = request.FILES.getlist('requestFiles')    
    for f in filesSent:
        newRequestFile = RequestFile(fileR = f, request = requestNeeded)
        newRequestFile.save()

    return redirect('http://10.0.1.2/getProfile', request)

def deleteRequestFile(request, requestFileID):
    RequestFile.objects.filter(id = requestFileID).delete()

    return redirect('http://10.0.1.2/getProfile', request)


def processPhoto(request):
    currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))
    if  request.FILES.get('uploadedImg', False) == False:
        return redirect('http://10.0.1.2/getProfile', request)
    else:

        currentUser.profileIMG = request.FILES.get('uploadedImg')
        currentUser.save()

    return redirect('http://10.0.1.2/getProfile', request)


def createResponseOnReview(request):
    currentUser = RegisteredUser.objects.get( user = User.objects.get(username = request.user.username))
    reviewArticleNeeded = reviewArticle.objects.get(id = request.POST['reviewArticleID'])
    authorType2 = "Patient"

    if Doctor.objects.filter(user = currentUser.user).exists():
        authorType2 = "Doctor"
        
    newRespondComment = respondComment(author = currentUser, authorType =  authorType2, body = request.POST['responseText'], reviewArticle = reviewArticleNeeded)
    newRespondComment.save()

    data = {'fullName' : getFullName(currentUser), 'responseText' : newRespondComment.body, 'responseDate' : newRespondComment.datePosted}
    return JsonResponse(data)

def editReviewField(request):
    currentUser = RegisteredUser.objects.get( user = User.objects.get(username = request.user.username))

    print(request.POST['objectType'])

    if reviewArticle.objects.filter(id = request.POST['reviewArticleID']).exists() and request.POST['objectType'] == "ReviewArticle":
        print("ssjsjsj")

        reviewArticleNeeded = reviewArticle.objects.get( id = request.POST['reviewArticleID'])
        setattr(reviewArticleNeeded, request.POST['fieldToChange'],  request.POST['newData'])
        reviewArticleNeeded.save()

    elif respondComment.objects.filter(id = request.POST['reviewArticleID']).exists() and request.POST['objectType'] == "Response":
        print("changeresponde")
        respondReviewArticleNeeded = respondComment.objects.get( id = request.POST['reviewArticleID'])
        setattr(respondReviewArticleNeeded, request.POST['fieldToChange'],  request.POST['newData'])
        respondReviewArticleNeeded.save()    

    print(request.POST['fieldToChange'] + request.POST['newData'])

    return HttpResponse("OK")

def deleteArticleReview(request, reviewID, articleID):
    
    reviewNeeded = reviewArticle.objects.get(id = reviewID)
    articleNeeded = reviewNeeded.article

    reviewNeeded.delete()
    scoreList =[]
    for r in articleNeeded.reviewarticle_set.all():
        scoreList.append(r.stars)

        articleNeeded.rating = sum(scoreList)/len(scoreList)
        articleNeeded.save()
            

    return redirect('http://10.0.1.2/showFullArticle/'+str(articleID)+'/', request)



def deleteResponseReview(request, responseID, articleID):

    responseNeeded = respondComment.objects.get(id = responseID)
    responseNeeded.delete()

    return redirect('http://10.0.1.2/showFullArticle/'+str(articleID)+'/', request)

def createArticleReview(request):
    context = {}
    articleNeeded = Article.objects.get(id = request.POST['articleID'])
    if Doctor.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))
        if currentUser.usersReviewOnArticle.filter(article = articleNeeded).exists():
            data = {'exists' : "True"}
            return JsonResponse(data)

        else:
            newReview = reviewArticle(author = currentUser, authorType = "Doctor", article = articleNeeded, body = request.POST['reviewAboutArticle'], stars = request.POST['ratingToArticle'])
            newReview.save()  
            scoreList =[]
            for r in articleNeeded.reviewarticle_set.all():
                scoreList.append(r.stars)

            articleNeeded.rating = sum(scoreList)/len(scoreList)
            articleNeeded.save()
            

            #data = {'exists' : "False", 'authorFullName' : getFullName(currentDoctor), 'articleBody' : articleNeeded.body, 'datePublished' : articleNeeded.datePosted, 'stars' : articleNeeded.stars }

    elif Patient.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))

        if currentUser.usersReviewOnArticle.filter(article = articleNeeded).exists():
            data = {'exists' : "True"}
            return JsonResponse(data)
        else:
            newReview = reviewArticle(author = currentUser, authorType = "Patient", article = articleNeeded, body = request.POST['reviewAboutArticle'], stars = request.POST['ratingToArticle'])
            newReview.save() 
            scoreList =[]
            for r in articleNeeded.reviewarticle_set.all():
                scoreList.append(r.stars)

            articleNeeded.rating = sum(scoreList)/len(scoreList)
            articleNeeded.save()
            #data = {'exists' : "False", 'authorFullName' : getFullName(currentDoctor), 'articleBody' : articleNeeded.body, 'datePublished' : articleNeeded.datePosted, 'stars' : articleNeeded.stars }
    
    return HttpResponse("OK")

def showFullArticle(request, articleID):
    context = {}
    articleToSend = Article.objects.get(id = articleID)
    context['Article'] = articleToSend
    context['isLiked'] = False
    context['isFavourite'] = False
    context['reviewArticleList'] = articleToSend.reviewarticle_set.all()
    reviewResponses = []


    for r in articleToSend.reviewarticle_set.all():
        reviewResponses.append(r.respondcomment_set.all())

    context['respondCommentList'] = reviewResponses

    if request.user.is_authenticated:
        currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))
        if articleToSend in currentUser.likedArticle.all():
            context['isLiked'] = True

        if articleToSend in currentUser.favouriteArticle.all():
            context['isFavourite'] = True
        

    

    return render(request, 'medapp/fullArticles.html', context) 




def searchArticles(request):
    context = {}
    likedArticlesList = []
    favouriteArticlesList = []
    articlesList = []

    if request.user.is_authenticated:
        currentUser = RegisteredUser.objects.get(user = User.objects.get(username = request.user.username))
        for a in Article.objects.all():
            if a in currentUser.likedArticle.all():
                likedArticlesList.append(a.id)
            
 

        for a in Article.objects.all():
            if a in currentUser.favouriteArticle.all():
                favouriteArticlesList.append(a.id)    

        context['likedArticlesList'] = likedArticlesList      
        context['favouriteArticlesList'] = favouriteArticlesList      

    

    searchQuery = request.GET['articleTitleforSearch'].lower()

    if searchQuery.endswith(' '):
        lastPosition = len(searchQuery)-1
        searchQuery = searchQuery[:lastPosition]


    approvedArticles = Article.objects.filter(numOfApprovals__gte = 2)

    for a in approvedArticles:
        if searchQuery in a.title.lower() or searchQuery in a.body.lower():
            articlesList.append(a)
        elif searchQuery in getFullName(a.author).lower():
            articlesList.append(a)

    context['articlesList'] = articlesList   
      
    context['searchQuery'] =   searchQuery  


    return render(request, 'medapp/browseArticles.html', context)

def articlesSection(request):
    
    return render(request, 'medapp/articlesHomePage.html')

def approveArticle(request):
    articleNeeded = Article.objects.get(id = request.POST['articleID'])
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    if request.POST['action'] == "Approve":
        if Doctor.objects.filter(disapprovedArticles = articleNeeded).exists():
            articleNeeded.doctorsDisapprove.remove(currentDoctor)
            articleNeeded.numOfDisapprovals -= 1

        articleNeeded.doctorsApprove.add(currentDoctor)
        articleNeeded.numOfApprovals += 1
        articleNeeded.save()

    elif request.POST['action'] == "Unapprove":
        articleNeeded.doctorsApprove.remove(currentDoctor)
        articleNeeded.numOfApprovals -= 1
        articleNeeded.save()
    elif request.POST['action'] == "Disapprove":
        if Doctor.objects.filter(approvedArticles = articleNeeded).exists():
            articleNeeded.doctorsApprove.remove(currentDoctor)
            articleNeeded.numOfApprovals -= 1

        articleNeeded.doctorsDisapprove.add(currentDoctor)
        articleNeeded.numOfDisapprovals += 1
        articleNeeded.save()
    elif request.POST['action'] == "Undisapprove":
        articleNeeded.doctorsDisapprove.remove(currentDoctor)
        articleNeeded.numOfDisapprovals -= 1
        articleNeeded.save()

    data = {'numOfApprovals' : articleNeeded.numOfApprovals}
    return JsonResponse(data)    



def viewArticleToApprove(request, articleID):
    context = {}
    likingArticleList = []
    favArticleList = []
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    articleNeeded = Article.objects.get(id = articleID)
    authorDoctor = Doctor.objects.get(id = articleNeeded.author.id)

    
    if articleNeeded in currentDoctor.approvedArticles.all():
        context['approvedByCurrentDoctor'] = True

    if articleNeeded in currentDoctor.disapprovedArticles.all():
        context['disapprovedByCurrentDoctor'] = True    

    for a in Article.objects.filter(usersLiked = currentDoctor):
        likingArticleList.append(a.id)

    for a in Article.objects.filter(usersFaved = currentDoctor):
        favArticleList.append(a.id)    


    context['likingArticleList'] = likingArticleList
    context['favArticleList'] = favArticleList
    context['Article'] = articleNeeded
    context['authorsFullName'] = getFullName(authorDoctor)

    

    return render(request, 'medapp/fullArticlesforApprove.html', context)


def writeArticle(request):
    context = {}
    context['Doctor'] = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    context['fullName'] = getFullName(Doctor.objects.get(user = User.objects.get(username = request.user.username)))


    return render(request, 'medapp/writeArticle.html', context)

def editArticleData(request):
    articleNeeded = Article.objects.get(id = request.POST['articleID'])
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    
    articleNeeded.title = request.POST['article_title']
    articleNeeded.body = request.POST['article_body']
    articleNeeded.save()

    return goToEditArticle(request, articleNeeded.id)

def deleteArticle(request, articleID):
    articleNeeded = Article.objects.get(id = articleID)
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    
    if currentDoctor == articleNeeded.author:
        articleNeeded.delete()

    return redirect('http://10.0.1.2/getProfile', request)
    

def goToEditArticle(request, articleID):
    context = {}
    articleNeeded = Article.objects.get(id = articleID)
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    context['Doctor'] = currentDoctor
    context['fullName'] = getFullName(Doctor.objects.get(user = User.objects.get(username = request.user.username)))
    context['articleNo'] = getIndexQuerySet(currentDoctor.doctorsArticles.all(), articleID)
    context['Article'] = articleNeeded
    print('sdj')


    return render(request, 'medapp/editArticle.html', context)


def createArticle(request):
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    context = {}
    newArticle = Article(title = request.POST['article_title'], body = request.POST['article_body'], author = currentDoctor, approved = False, numOfApprovals = 0, articleIMG = request.FILES.get('article_image'))
    newArticle.save()
    
    return getProfile(request)

def likeArticle(request):
    if Patient.objects.filter(username = User.objects.get(username = request.user.username) ).exists():
        currentUser = Patient.objects.get(username = User.objects.get(username = request.user.username) )

    if Doctor.objects.filter(username = User.objects.get(username = request.user.username) ).exists():
        currentUser = Doctor.objects.get(username = User.objects.get(username = request.user.username) )    
    

    if Article.objects.get(id = request.POST['targetDoctor']) in currentUser.likedArticle.all():
        currentUser.likedArticle.remove(Article.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Dislike")
    else:
        currentUser.likedArticle.add(Article.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Like")

@login_required
def favouriteArticle(request):
    if Patient.objects.filter(username = User.objects.get(username = request.user.username) ).exists():
        currentUser = Patient.objects.get(username = User.objects.get(username = request.user.username) )

    if Doctor.objects.filter(username = User.objects.get(username = request.user.username) ).exists():
        currentUser = Doctor.objects.get(username = User.objects.get(username = request.user.username) )    
        
    if Article.objects.get(id = request.POST['targetDoctor']) in currentUser.favouriteArticle.all():
        currentUser.favouriteArticle.remove(Article.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Unfavourite")
    else:
        currentUser.favouriteArticle.add(Article.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Favourite")

@login_required
def likeDoctor(request):
    currentPatient = Patient.objects.get(username = User.objects.get(username = request.user.username) )
    
    if Doctor.objects.get(id = request.POST['targetDoctor']) in currentPatient.likedDoctors.all():
        currentPatient.likedDoctors.remove(Doctor.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Dislike")
    else:
        currentPatient.likedDoctors.add(Doctor.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Like")

@login_required
def favouriteDoctor(request):
    currentPatient = Patient.objects.get(username = User.objects.get(username = request.user.username) )
    
    if Doctor.objects.get(id = request.POST['targetDoctor']) in currentPatient.favouriteDoctors.all():
        currentPatient.favouriteDoctors.remove(Doctor.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Unfavourite")
    else:
        currentPatient.favouriteDoctors.add(Doctor.objects.get(id = request.POST['targetDoctor']))
        return HttpResponse("Favourite")




def editProfileField(request):
    fieldToChange = request.POST['fieldToChange']

    if fieldToChange == 'email' or fieldToChange == 'first_name' or fieldToChange == 'last_name' or fieldToChange == 'username':
        currentUser = User.objects.get(username = request.user.username )

       
    else:
        if Patient.objects.filter(username=request.user.username).exists():
            currentUser = Patient.objects.get(username = request.user.username)

        elif Doctor.objects.filter(username=request.user.username).exists():
            currentUser = Doctor.objects.get(username = request.user.username)



    fieldToChange = "'" + request.POST['fieldToChange'] + "'" 
    print(fieldToChange)
    #currentAnamnesis.placeOfBirth = request.POST['newData']
    setattr(currentUser, request.POST['fieldToChange'],  request.POST['newData'])
    currentUser.save()

    return HttpResponse(request.POST['newData'])
    

@login_required
def editProfilePatient(request):
    context = {}
    context['Patient'] = Patient.objects.get(username = request.user.username)

    return render(request, 'medapp/editProfilePatient.html', context)

@login_required
def editProfileDoctor(request):
    context = {}
    existingSpecializations = []
    context['Doctor'] = Doctor.objects.get(username = request.user.username)
    specializationsToSend = ['Allergist', 'Therapist', 'Cardiologist', 'Neurologist', 'Oncologist', 'Immunologist', 'Ophtalmologist', 'Dietologist', 'ENT']
    for s in specializationsToSend:
        if s in context['Doctor'].specialization:
            existingSpecializations.append(1)
        else:
            existingSpecializations.append(0)
    sendList1 = zip(specializationsToSend, existingSpecializations)

    context['specializationList'] = sendList1 

    return render(request, 'medapp/editProfileDoc.html', context)

def registryToDoctor(request, patientID):

    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    currentPatient = Patient.objects.get(id = patientID)
    context = {}
    for c in Consultancy.objects.filter(consultancyDoctor = currentDoctor):

        if c.consultancyPatient.user.username == currentPatient.user.username and c.status == "Active":
            currentAnamnesis = Anamnesis.objects.get( id = c.consultancyPatient.anamnesis.id)
            context['Registry'] = currentPatient.registry
            context['OwnersFullName'] = getFullName(currentPatient)
            context['Illnesses'] = currentPatient.registry.illness_set.all()
            context['Treatments'] = currentPatient.registry.treatment_set.all()
            return render(request, 'medapp/viewRegistry.html', context)





    return render(request, 'medapp/base.html', context)

def getFullName(currentUser):

    return currentUser.user.first_name + " " + currentUser.user.last_name

@xframe_options_sameorigin
def getRegistry(request):
    context = {}
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))

    if Patient.objects.filter(username=request.user.username).exists():
        context['Registry'] = currentPatient.registry
        context['Illnesses'] = currentPatient.registry.illness_set.all()
        context['Treatments'] = currentPatient.registry.treatment_set.all()


    return render(request, 'medapp/registry.html', context)

def createNewTreatment(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    context = {}
    treatmentResult = "notSolved"

    specializationsList = str(request.POST.getlist("specialization") )
    specializationsList = specializationsList.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(specializationsList)

     
    print(request.POST['treatmentResult'])
    if request.POST['treatmentResult'] == "Solved":
        treatmentResult = "Solved"
    elif request.POST['treatmentResult'] == "inProcess":  
        treatmentResult = "inProcess" 
    elif request.POST['treatmentResult'] == "notSolved":
        treatmentResult = "notSolved"     

    newTreatment = Treatment(registry = currentPatient.registry, dateT = request.POST['dateOfTreatment'], specialization = specializationsList, describtion = request.POST['describtion'], methodology = request.POST['methodology'], result = treatmentResult )
    newTreatment.save()

    filesSent = request.FILES.getlist('treatmentFiles')

    for f in filesSent:
        newTreatmentFile = TreatmentFile(fileT = f, treatment = newTreatment)
        newTreatmentFile.save()

    context['Registry'] = currentPatient.registry
    context['Illnesses'] = currentPatient.registry.illness_set.all()
    context['Treatments'] = currentPatient.registry.treatment_set.all()

    return render(request, 'medapp/registry.html', context)

def getTreatmentData(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))

    treatmentNeeded= currentPatient.registry.treatment_set.get(id = request.GET['treatmentID'])
    methodology = treatmentNeeded.methodology
    describtion = treatmentNeeded.describtion
    specialization = treatmentNeeded.specialization
    date = treatmentNeeded.dateT
    result = treatmentNeeded.result

    data = {'methodology' : methodology, 'describtion' : describtion, 'specialization' : specialization, 'date' : date, 'result' : result}
    return JsonResponse(data)

def editTreatment(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    neededTreatment = currentPatient.registry.treatment_set.get(id = request.POST['treatmentID'])
    context = {}
    treatmentResult = "notSolved"

    specializationsList = str(request.POST.getlist("specialization") )
    specializationsList = specializationsList.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(specializationsList)

     
    print(request.POST['treatmentResult'])
    if request.POST['treatmentResult'] == "Solved":
        neededTreatment.result = "Solved"
    elif request.POST['treatmentResult'] == "inProcess":  
        neededTreatment.result = "inProcess" 
    elif request.POST['treatmentResult'] == "notSolved":
        neededTreatment.result = "notSolved"     

    neededTreatment.dateT = request.POST['dateOfTreatment']
    neededTreatment.specialization = specializationsList
    neededTreatment.describtion = request.POST['describtion']
    neededTreatment.methodology = request.POST['methodology']
    neededTreatment.save()

    context['Registry'] = currentPatient.registry
    context['Illnesses'] = currentPatient.registry.illness_set.all()
    context['Treatments'] = currentPatient.registry.treatment_set.all()

    return render(request, 'medapp/registry.html', context)


@login_required    
def createNewIllness(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    context = {}
    isActive = False


    specializationsList = str(request.POST.getlist("specialization") )
    specializationsList = specializationsList.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(specializationsList)

    print(request.POST['illnessState'])
    if request.POST['illnessState'] == "active":
        isActive = True
        print("SS")
       # try:
    newIllness = Illness(registry = currentPatient.registry, dateI = request.POST['dateOfIllness'], specialization = specializationsList, describtion = request.POST['describtion'], diagnose = request.POST['diagnose'], active = isActive )
    newIllness.save()
    filesSent = request.FILES.getlist('illnessFiles')    
    for f in filesSent:
        print(f)
        newIllnessFile = IllnessFile(fileI = f, illness = newIllness)
        newIllnessFile.save()

       # except ValidationError:
        #    print(ValidationError)
        #    return HttpResponse("Date Input error")

   
    context['Registry'] = currentPatient.registry
    context['Illnesses'] = currentPatient.registry.illness_set.all()
    context['Treatments'] = currentPatient.registry.treatment_set.all()

    return render(request, 'medapp/registry.html', context)

@login_required    
def getIllnessData(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    
    illnessNeeded= currentPatient.registry.illness_set.get(id = request.GET['illnessID'])
    diagnose = illnessNeeded.diagnose
    describtion = illnessNeeded.describtion
    specialization = illnessNeeded.specialization
    date = illnessNeeded.dateI
    active = illnessNeeded.active
    
    data = {'diagnose' : diagnose, 'describtion' : describtion, 'specialization' : specialization, 'date' : date, 'active' : active}

    return JsonResponse(data)

def editIllness(request):
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
    illnessNeeded = currentPatient.registry.illness_set.get(id = request.POST['illnessID'])

    context = {}
    isActive = False


    specializationsList = str(request.POST.getlist("specialization") )
    specializationsList = specializationsList.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(specializationsList)

    print(request.POST['illnessState'])
    if request.POST['illnessState'] == "active":
        isActive = True
        illnessNeeded.active = isActive
    elif request.POST['illnessState'] == "solved":
        isActive = False
        illnessNeeded.active = isActive
    elif request.POST['illnessState'] == "":
        isActive = False


    illnessNeeded.dateI = request.POST['dateOfIllness']
    illnessNeeded.specialization = specializationsList
    illnessNeeded.describtion = request.POST['describtion']
    illnessNeeded.diagnose = request.POST['diagnose']
    illnessNeeded.save()

    #newIllness = Illness(registry = currentPatient.registry, dateI = request.POST['dateOfIllness'], specialization = specializationsList, describtion = request.POST['describtion'], diagnose = request.POST['diagnose'], active = isActive )
    #newIllness.save()
    context['Registry'] = currentPatient.registry
    context['Illnesses'] = currentPatient.registry.illness_set.all()
    context['Treatments'] = currentPatient.registry.treatment_set.all()

    return render(request, 'medapp/registry.html', context)

def getProfile(request):
    context = {}
    if Patient.objects.filter(username=request.user.username).exists():
        patientToSend = Patient.objects.get(username = request.user.username)
        requests = patientToSend.request_set.all()
        consultancies = patientToSend.consultancy_set.all()
       
        doctorsAgeList = []
        doctorsAgeListС = []

        favouriteDoctorsCount = getFavouriteDocs(patientToSend).count()
        favouriteArticlesCount = patientToSend.favouriteArticle.all().count()
        RequestsListCount = patientToSend.request_set.all().count()
        ConsultancyListCount = patientToSend.consultancy_set.all().count()
        ConsultancyListClosedCount = patientToSend.consultancy_set.filter(status = "Closed").count()

         
        print(ConsultancyListClosedCount)

        for r in requests:
            doctorsAgeList.append(datetime.now().year - r.targetDoctor.dob.year)

        for c in consultancies:
            doctorsAgeListС.append(datetime.now().year - c.consultancyDoctor.dob.year)  
        
        context['ConsultancyListClosed'] = zip(consultancies, doctorsAgeListС)
        context['ConsultancyList'] = zip(consultancies, doctorsAgeListС)
        context['RequestsList'] = zip(requests, doctorsAgeList)
        context['favouriteArticlesList'] = patientToSend.favouriteArticle.all()
        context['favouriteDoctorsList'] = getFavouriteDocs(patientToSend)
        context['Patient'] = patientToSend

        context['favouriteDoctorsCount'] = favouriteDoctorsCount
        context['favouriteArticlesCount'] = favouriteArticlesCount
        context['RequestsListCount'] = RequestsListCount
        context['ConsultancyListCount'] = ConsultancyListCount
        context['ConsultancyListClosedCount'] = ConsultancyListClosedCount




        return render(request, 'medapp/profilePatient.html', context)

    elif Doctor.objects.filter(username=request.user.username).exists():
        doctorToSend = Doctor.objects.get(username = request.user.username)
        patientAgeList = []
        patientAgeListC = []
        articlesForApprove = []
        approvalListForDoc = []
        disapprovalListForDoc = []

        


        requests = doctorToSend.request_set.all()
        consultancies = doctorToSend.consultancy_set.all()

        for r in requests:
            patientAgeList.append(datetime.now().year - r.requestPatient.dob.year)

        for c in consultancies:
            patientAgeListC.append(datetime.now().year - c.consultancyPatient.dob.year)
            print(c.status)  

        for a in Article.objects.all():
            if a.numOfApprovals < 5:
                articlesForApprove.append(a)  
                if Doctor.objects.filter(approvedArticles = a).exists():
                    approvalListForDoc.append(True)
                else:
                    approvalListForDoc.append(False)
                    
                if Doctor.objects.filter(disapprovedArticles = a).exists():
                    disapprovalListForDoc.append(True)
                else:
                    disapprovalListForDoc.append(False)
      
        favouriteArticlesListCount = doctorToSend.favouriteArticle.all().count()
        myArticleListCount = doctorToSend.doctorsArticles.all().count()
        articlesForApproveCount = len(articlesForApprove)
        RequestsListCount = doctorToSend.request_set.all().count()
        ConsultancyListCount = doctorToSend.consultancy_set.all().count()
        ConsultancyListClosedCount = doctorToSend.consultancy_set.filter(status = "Closed").count()

        context['favouriteArticlesList'] = doctorToSend.favouriteArticle.all()
        context['articlesForApprove'] = zip(articlesForApprove, approvalListForDoc, disapprovalListForDoc)
        context['myArticleList'] = doctorToSend.doctorsArticles.all()
        context['ConsultancyListClosed'] = zip(consultancies, patientAgeListC)
        context['ConsultancyList'] = zip(consultancies, patientAgeListC)
        context['RequestsList'] = zip(requests, patientAgeList)
        context['Experience'] = datetime.now().year - doctorToSend.experience.year 
        context['Doctor'] = doctorToSend

        context['articlesForApproveCount'] = articlesForApproveCount
        context['RequestsListCount'] = RequestsListCount
        context['ConsultancyListCount'] = ConsultancyListCount
        context['ConsultancyListClosedCount'] = ConsultancyListClosedCount
        context['favouriteArticlesCount'] = favouriteArticlesListCount
        context['myArticleListCount'] = myArticleListCount

        return render(request, 'medapp/profileDoc.html', context)

    


    return render(request, 'medapp/base.html', context)

def getFavouriteDocs(patientToSend):

    return patientToSend.favouriteDoctors.all()
        

def showDocPage(request, user_name):
    context = {}
    likesDoctorsList = []
    favouriteDoctorsList = []
    reviewsList = []
    isPatient = False


    doctorToSend = Doctor.objects.get(username = user_name)
    specializations = doctorToSend.specialization.split(' ')
    age = datetime.now().year - doctorToSend.dob.year
    experience = datetime.now().year - doctorToSend.experience.year 

   

    if request.user.is_authenticated:
        if Patient.objects.filter(user = User.objects.get(username = request.user.username)).exists():
            isPatient = True
            currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
            for d in Doctor.objects.all():
                print(d)
                if d in currentPatient.likedDoctors.all():
                    likesDoctorsList.append(d.id)
                
                if d in currentPatient.favouriteDoctors.all():
                    favouriteDoctorsList.append(d.id)


            i = 0  

    reviewsList = doctorToSend.reviewdoctor_set.all()    
        
                
                


    context['sendReviewList'] = reviewsList 
    context['doctor'] = doctorToSend
    context['specializations'] = specializations
    context['age'] = age
    context['experience'] = experience
    context["likingList"] = likesDoctorsList
    context["favList"] = favouriteDoctorsList
    context["isPatient"] = isPatient


    return render(request, 'medapp/showDoctorPage.html', context)


def closeConsultancy(request):
    consultancyNeeded = Consultancy.objects.get(id = request.POST['consultancyID'])
    currentDoctor = consultancyNeeded.consultancyDoctor
    currentPatient = consultancyNeeded.consultancyPatient
    awaitData = ""
    context = {}

    if Doctor.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        if currentDoctor.user.username == request.user.username:
            consultancyNeeded.closeStatusDoctor = True
            consultancyNeeded.status = "Awaiting Close"
            consultancyNeeded.save()
            awaitMsg = "Expecting patient to close consultancy!"

            consultancyList = currentPatient.consultancy_set.all()
            consultancyNo = getIndexQuerySet(consultancyList, consultancyNeeded.id)
            mailTitle = "Medapp Consultancy No: " + str(consultancyNo) + " notification."
            mailText = currentPatient.user.first_name + ", Consultancy No: " + str(consultancyNo) + " was closed by doctor " + getFullName(currentDoctor) + ". Expecting you to close as well!"

            send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [currentPatient.user.email])

            currentPatient.rating = (currentPatient.rating + int(request.POST['ratingValueToPass']))/2
            currentPatient.save()
            print("Doc /// Pat")
            print(request.POST['ratingValueToPass'])
            print(currentPatient.rating)
            print(consultancyNeeded.closeStatusPatient)
            print(consultancyNeeded.closeStatusDoctor)


            if consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor:
                consultancyNeeded.status = "Closed"
                consultancyNeeded.consultancyEndDate = datetime.now()
                consultancyNeeded.save()

            
            data = {'await' : awaitMsg}
            return JsonResponse(data)   


    elif Patient.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        if currentPatient.user.username == request.user.username: 
            consultancyNeeded.closeStatusPatient = True
            consultancyNeeded.status = "Awaiting Close"
            consultancyNeeded.save()

            consultancyList = currentDoctor.consultancy_set.all()
            consultancyNo = getIndexQuerySet(consultancyList, consultancyNeeded.id)
            mailTitle = "Medapp Consultancy No: " + str(consultancyNo) + " notification."
            mailText = currentDoctor.user.first_name + ", Consultancy No: " + str(consultancyNo) + " was closed by patient " + getFullName(currentPatient) + ". Expecting you to close as well!"

            send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [currentDoctor.user.email])


            awaitMsg = "Expecting doctor to close consultancy!"

            currentDoctor.rating = (currentDoctor.rating + int(request.POST['ratingValueToPass']))/2
            currentDoctor.save()

            print("Pat /// Doc")
            print(request.POST['ratingValueToPass'])
            print(currentDoctor.rating)


            newReview = reviewDoctor(targetDoctor = currentDoctor, authorPatient = currentPatient, reviewText = request.POST['reviewMSG'], stars = request.POST['ratingValueToPass'])
            newReview.save()
            print(consultancyNeeded.closeStatusPatient)
            print(consultancyNeeded.closeStatusDoctor)
            if consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor:
                consultancyNeeded.status = "Closed"
                consultancyNeeded.consultancyEndDate = datetime.now()
                consultancyNeeded.save()
                
                #Mail to Doctor sent!
                consultancyList = currentDoctor.consultancy_set.all()
                consultancyNo = getIndexQuerySet(consultancyList, consultancyNeeded.id)
                mailTitle = "Medapp Consultancy No: " + str(consultancyNo) + " Closed!."
                mailText = currentDoctor.user.first_name + ", Consultancy No: " + str(consultancyNo) + " is closed!"
                send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [currentDoctor.user.email])

                #Mail to patient
                consultancyList = currentPatient.consultancy_set.all()
                consultancyNo = getIndexQuerySet(consultancyList, consultancyNeeded.id)
                mailTitle = "Medapp Consultancy No: " + str(consultancyNo) + " notification."
                mailText = currentPatient.user.first_name + ", Consultancy No: " + str(consultancyNo) + " is closed!"
                send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [currentPatient.user.email])


            data = {'await' : awaitMsg}
            return JsonResponse(data)    

    return render(request, 'medapp/base.html')            


def getConsultancy(request, consultancyID):

    consultancyNeeded = Consultancy.objects.get(id = consultancyID )
    currentDoctor = consultancyNeeded.consultancyDoctor
    currentPatient = consultancyNeeded.consultancyPatient
    context = {}

    if Doctor.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        if currentDoctor.user.username == request.user.username:

            consultancyList = currentDoctor.consultancy_set.all()
            consultancyNo = getIndexQuerySet(consultancyList, consultancyID)
            context['isDoctor'] = True
            context['consultancy'] = consultancyNeeded
            context['consultancyNo'] = consultancyNo
            context['chat'] = consultancyNeeded.chat


            if consultancyNeeded.closeStatusPatient == False and consultancyNeeded.closeStatusDoctor:
                context['consultancyClosed'] = True
                context['awaitMSG'] = "Expecting patient to close consultancy!"

            elif consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor == False:
                context['consultancyClosed'] = False
                context['awaitMSG'] = "Expecting you to close consultancy!"

            elif consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor:     
                context['consultancyClosed'] = True
                context['awaitMSG'] = "Closed!"
            else:
                context['consultancyClosed'] = False


    elif Patient.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        if currentPatient.user.username == request.user.username: 
            consultancyList = currentPatient.consultancy_set.all()
            consultancyNo = getIndexQuerySet(consultancyList, consultancyID)
            context['isDoctor'] = False
            context['consultancy'] = consultancyNeeded
            context['consultancyNo'] = consultancyNo
            context['chat'] = consultancyNeeded.chat

            if consultancyNeeded.closeStatusPatient == False and consultancyNeeded.closeStatusDoctor:
                context['consultancyClosed'] = False
                context['awaitMSG'] = "Expecting you to close consultancy!"
                
            elif consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor == False:
                context['consultancyClosed'] = True

                context['awaitMSG'] = "Expecting doctor to close consultancy!"

            elif consultancyNeeded.closeStatusPatient and consultancyNeeded.closeStatusDoctor:     
                context['consultancyClosed'] = True
                context['awaitMSG'] = "Closed!"
            else:
                context['consultancyClosed'] = False                

            


    else:

        return render(request, 'medapp/base.html', context)
    

    return render(request, 'medapp/consultancyObj.html', context)


def actionOnRequest(request):

    print('s')
    print(request.POST['requestID'])
    requestNeeded = Request.objects.get(id = request.POST['requestID'])
    status = "inProcess"
    if request.POST['action'] == "Agree":
        requestNeeded.status = "Agreed"
        requestNeeded.save()
        newConsultancy = Consultancy(consultancyPatient = requestNeeded.requestPatient, consultancyDoctor = requestNeeded.targetDoctor, patientMessage = requestNeeded.message, status = "Active", doctorComments = "Area for doctor's comments", doctorConclusion = "Area for doctor's conclusion upon end of consultancy")
        newConsultancy.save()

        newChat = Chat(consultancy = newConsultancy, countMSG = 1)
        newChat.save()
        
        welcomeTextFromDoctor = "Hello, " + newConsultancy.consultancyPatient.user.first_name + ", you are welcome to contact me in this chat!"
        newMessageDoctor = ChatMessage(chat = newChat, author = newConsultancy.consultancyDoctor, authorType = "Doctor", messageText = welcomeTextFromDoctor)
        newMessageDoctor.save()
        print("saved")

        filesSent = requestNeeded.requestfile_set.all()  
        for f in filesSent:
            newConsultancyFile = ConsultancyFile(fileC = f.fileR, consultancy = newConsultancy, author = requestNeeded.requestPatient.user)
            newConsultancyFile.save()
        full_name = newConsultancy.consultancyPatient.user.first_name + " " + newConsultancy.consultancyPatient.user.last_name
        age = datetime.now().year - newConsultancy.consultancyPatient.dob.year
        data = {'action' : requestNeeded.status, 'full_name' : full_name, 'age' : age, 'consultancyID' : newConsultancy.id, 'status' : newConsultancy.status} 

        print("A")
    elif request.POST['action'] == "Reject":
        requestNeeded.status = "Rejected"
        requestNeeded.save()
        data = {'action' : requestNeeded.status} 

        print("R")
    else:
        data = {'action' : requestNeeded.status} 

        print("Read") 

    requestList = requestNeeded.requestPatient.request_set.all()
    requestNo = getIndexQuerySet(requestList, requestNeeded.id)
    mailTitle = "Medapp Request No: " + str(requestNo) + "update!" + str(requestNeeded.status)
    mailText = requestNeeded.requestPatient.user.first_name + ", Dr " + requestNeeded.targetDoctor.user.first_name + " " + requestNeeded.status + " to provide consultancy!"
    send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [requestNeeded.requestPatient.user.email])

     


    return JsonResponse(data)


def getRequestData(request):

    if Doctor.objects.filter(user = User.objects.get(username = request.user.username)).exists():
        doctorToRequest = Doctor.objects.get(user = User.objects.get(username = request.user.username))
        ratingToSend = doctorToRequest.rating
        requestNeeded = doctorToRequest.request_set.get(id = request.GET['requestID'])
        requestNo = getIndexQuerySet(doctorToRequest.request_set.all(), request.GET['requestID'])
        isDoctor = "True"
        full_name = requestNeeded.requestPatient.user.first_name + " " + requestNeeded.requestPatient.user.last_name
        location = requestNeeded.requestPatient.location
        dob = requestNeeded.requestPatient.dob
    else:
        patientToRequest = Patient.objects.get(user = User.objects.get(username = request.user.username))
        ratingToSend = patientToRequest.rating
        requestNeeded = patientToRequest.request_set.get(id = request.GET['requestID'])
        requestNo = getIndexQuerySet(patientToRequest.request_set.all(), request.GET['requestID'])
        isDoctor = "False"

        full_name = requestNeeded.targetDoctor.user.first_name + " " + requestNeeded.targetDoctor.user.last_name
        location = requestNeeded.targetDoctor.location
        dob = requestNeeded.targetDoctor.dob
    

    
    message = requestNeeded.message
    status = requestNeeded.status

    files = requestNeeded.requestfile_set.all()
    files_url=[]
    illnessFileId = []
    for f in files:
        files_url.append("media/"+str(f.fileR))
        illnessFileId.append(f.id)
        #files

    print(requestNo)
    data = {'requestNo' : requestNo, 'full_name' : full_name, 'location' : location, 'dob' : dob.strftime("%B %d %Y"), 'message' : message, 'imageURL' : ("media/" + str(requestNeeded.requestPatient.profileIMG)),  'status' : status, 'filesURL' : files_url, 'illnessFileID' : illnessFileId, 'ratingvalue' : ratingToSend, 'isDoctor' : isDoctor}

    return JsonResponse(data)    

def getIndexQuerySet(searchList, elementID):
    i = 0
    print(searchList)
    for s in searchList:
        print(elementID)
        print(s.id)
        if str(s.id) == str(elementID):
            
            return i+1
        i = i + 1
    return 0        


def requestConsultancy(request):

    requestsList = Request.objects.all()

    doctorToRequest = Doctor.objects.get(user = User.objects.get(username = request.POST['targetDoctor']))
    currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))

    datetimeNow = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    print(doctorToRequest.user.username)
    print(currentPatient.user.username)
    print(request.POST['message'])
    for r in requestsList:
        if r.requestPatient ==  currentPatient and r.targetDoctor == doctorToRequest:
            
            return HttpResponse("requestExists")

        
    newRequest = Request(requestDate = datetimeNow, message = request.POST['message'], targetDoctor = doctorToRequest, requestPatient = currentPatient, status = "Pending" )
    newRequest.save()

    requestList = doctorToRequest.request_set.all()
    requestNo = getIndexQuerySet(requestList, newRequest.id)
    mailTitle = "Medapp: New Request No " + str(requestNo)
    mailText = "Dr" + newRequest.targetDoctor.user.first_name + ", Patient " + newRequest.requestPatient.user.first_name + " " + newRequest.requestPatient.user.last_name + " requested consultancy! \n Patient is from: " +  newRequest.requestPatient.location + " \n Patient tel: " + newRequest.requestPatient.telphone + " Patient email: " + newRequest.requestPatient.user.email + "."
    send_mail(mailTitle , mailText, 'ihuseyn5@gmail.com', [newRequest.targetDoctor.user.email])



    


    
    

    return HttpResponse("OK")


def anamnesis(request):
    currentUser = Patient.objects.get(username = request.user.username)
    currentAnamnesis = Anamnesis.objects.get( id = currentUser.anamnesis_id)
    context = {}
    context['anamnesis'] = currentAnamnesis

    return render(request, 'medapp/anamnesisPage.html', context)
    #anamnesisCreated = Anamnesis(placeOfBirth = request.PSOT['placeOfBirth'], parentsAgeAtBirth = request.POST['parentsAge'], descriptionOfBirth = request.POST['descriptionOfBirth'], aboutEAT = request.POST['aboutEAT'], premorbidState = request.POST['premorbidState'], peculiaritiesInDevelopment = request.POST['peculiaritiesInDevelopment'], lifeConditions = request.POST['lifeConditions'], jobDescription = request.POST['jobDescription'], badHabits = request.POST['badHabits'], lifeStyle = request.POST['lifeStyle'], dietDescription = request.POST['dietDescription'], pastIllnesses = request.POST['pastIllnesses'], surgicalInterventions = request.POST['surgicalInterventions'], hereditaryDiseases = request.POST['hereditaryDiseases'], pastInfections = request.POST['pastInfections'], allergicHistory = request.POST['allergicHistory'] )

def editConsultancyField(request):
    patientUsername = Consultancy.objects.get( id = request.POST['consultancyID']).consultancyPatient.user.username
    doctorUsername = Consultancy.objects.get( id = request.POST['consultancyID']).consultancyDoctor.user.username

    if patientUsername == request.user.username or doctorUsername == request.user.username:

        currentConsultancy = Consultancy.objects.get( id = request.POST['consultancyID'])
        setattr(currentConsultancy, request.POST['fieldToChange'],  request.POST['newData'])
        currentConsultancy.save()

        print(request.POST['fieldToChange'] + request.POST['newData'])

        return HttpResponse("OK")

    else:
        return render(request, 'medapp/base.html') 






def editAnamnesis(request):

    currentUser = Patient.objects.get(username = request.user.username)
    print(currentUser.id)
    print(currentUser.anamnesis_id)

    print(currentUser.username)

    currentAnamnesis = Anamnesis.objects.get( id = currentUser.anamnesis_id)

    fieldToChange = "'" + request.POST['fieldToChange'] + "'" 
    print(currentAnamnesis.id)
    print(fieldToChange)
    print(currentAnamnesis.placeOfBirth)
    print(request.POST['newData'])
    #currentAnamnesis.placeOfBirth = request.POST['newData']

    setattr(currentAnamnesis, request.POST['fieldToChange'],  request.POST['newData'])
    print(currentAnamnesis.placeOfBirth)

    currentAnamnesis.save()

    return HttpResponse("OK")

def anamnesisToDoctor(request, patientID):
    
    currentDoctor = Doctor.objects.get(user = User.objects.get(username = request.user.username))
    currentPatient = Patient.objects.get(id = patientID)
    context = {}

    for c in Consultancy.objects.filter(consultancyDoctor = currentDoctor):

        if c.consultancyPatient.user.username == currentPatient.user.username and c.status == "Active":
            currentAnamnesis = Anamnesis.objects.get( id = c.consultancyPatient.anamnesis.id)
            context['anamnesis'] = currentAnamnesis
            return render(request, 'medapp/viewAnamnesis.html', context)





    return render(request, 'medapp/base.html', context)


def searchDoctor(request):
    context = {}
    doctorList = Doctor.objects.all()
    sendList = []  
    experienceList =[]
    ageList = []
    specializationList = []
    likesDoctorsList = []
    favouriteDoctorsList = []

    isPatient = False

    if request.user.is_authenticated:
        if Patient.objects.filter(user = User.objects.get(username = request.user.username)).exists():
            isPatient = True
            currentPatient = Patient.objects.get(user = User.objects.get(username = request.user.username))
            for d in Doctor.objects.all():
                print(d)
                if d in currentPatient.likedDoctors.all():
                    likesDoctorsList.append(d.id)
                
                if d in currentPatient.favouriteDoctors.all():
                    favouriteDoctorsList.append(d.id)


            

    

    for d in doctorList:
        if request.GET['specializationForSearch'] == "" and request.GET['doctorNameforSearch'] == "":
                sendList.append(d)
                ageList.append(datetime.now().year - d.dob.year)
                experienceList.append(datetime.now().year - d.experience.year )
                specializationList.append(d.specialization.split(' '))


        elif request.GET['specializationForSearch'] == "":

            doctorNameForComparison = d.user.first_name + " " + d.user.last_name
            doctorNameForComparisonReveresed = d.user.last_name + " " + d.user.first_name

            if request.GET['doctorNameforSearch'].lower() in doctorNameForComparison.lower() or request.GET['doctorNameforSearch'].lower() in doctorNameForComparisonReveresed.lower():
                sendList.append(d)
                ageList.append(datetime.now().year - d.dob.year)
                experienceList.append(datetime.now().year - d.experience.year )
                specializationList.append(d.specialization.split(' '))

        elif request.GET['specializationForSearch'] in d.specialization:

            doctorNameForComparison = d.user.first_name + " " + d.user.last_name
            doctorNameForComparisonReveresed = d.user.last_name + " " + d.user.first_name

            if request.GET['doctorNameforSearch'] == "":
                sendList.append(d)
                ageList.append(datetime.now().year - d.dob.year)
                experienceList.append(datetime.now().year - d.experience.year )
                specializationList.append(d.specialization.split(' '))
            
            elif request.GET['doctorNameforSearch'].lower() in doctorNameForComparison.lower() or request.GET['doctorNameforSearch'].lower() in doctorNameForComparisonReveresed.lower():

                sendList.append(d)
                ageList.append(datetime.now().year - d.dob.year)
                experienceList.append(datetime.now().year - d.experience.year )
                specializationList.append(d.specialization.split(' '))


        



    sendList1 = zip(sendList, ageList, experienceList, specializationList)
    context["sendDoctorList"] = sendList1
    context["requestSpec"] = request.GET['specializationForSearch'].lower()
    context["requestDoc"] = request.GET['doctorNameforSearch'].lower()
    context["isPatient"] = isPatient
    print(likesDoctorsList)
    print(favouriteDoctorsList)

    context["likingList"] = likesDoctorsList
    context["favList"] = favouriteDoctorsList


    #context["ageList"] = ageList
    #context["experienceList"] = experienceList

    #context["sendDoctorList"] = Doctor.objects.filter(specialization=request.POST['specializationForSearch'])
    
    

    return render(request, 'medapp/showDoctors.html', context)

def showDoctorPage(request):

    return render (request, 'medapp/showDoctorPage.html')

def goSignUp(request):

    return render (request, 'medapp/signUp.html')

def signUp(request):

    justRegisteredUser = User.objects.create_user(username=request.POST["usernameInput"].lower(), email=request.POST["email"], password=request.POST["password"], first_name=request.POST["firstName"], last_name=request.POST["secondName"] )


    if request.POST["education"] == "":
        anamnesisCreated = Anamnesis()
        anamnesisCreated.save()
        registryCreated = Registry()
        registryCreated.save()
        registeredUser = Patient( user = justRegisteredUser, username = justRegisteredUser.username, dob = request.POST["dob"], location = request.POST["city"] + " , " + request.POST["country"], telphone = request.POST['telphone'], malefemale = request.POST['malefemale'], rating = 5, anamnesis = anamnesisCreated, registry = registryCreated )
        registeredUser.save()
    else:
        print(request.POST.getlist("specialization"))
        specializationsList = str(request.POST.getlist("specialization") )
        specializationsList = specializationsList.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
        registeredUser = Doctor( user = justRegisteredUser, username = justRegisteredUser.username, dob = request.POST["dob"], location = request.POST["city"] + " , " + request.POST["country"], telphone = request.POST['telphone'], work = request.POST['work'], malefemale = request.POST['malefemale'], experience = request.POST["experience"],  rating = 5, achievementStatus = 5, specialization=specializationsList, education = request.POST['education'], aboutMe = request.POST['aboutMe'] )
        registeredUser.save()
        print(registeredUser.specialization)



    return render (request, 'medapp/base.html')

def changePassword(request):
    currentUser = User.objects.get(username = request.user.username)
    print("before check")
    print(request.POST['newPassword'])
    if(check_password(request.POST['oldPassword'], request.user.password)):
        currentUser.set_password(request.POST['newPassword'])
        currentUser.save()
        return HttpResponse("OK")
    
    print("no check")

    return HttpResponse("noMatch")

def goLogIn(request):

    return render (request, 'medapp/logIn.html')

def goLogOut(request):
    logout(request)
    return render (request, 'medapp/base.html')

def logIn(request):
    context={}
    print(User.objects.filter(username=request.POST["usernameInput"].lower()).exists())
    loggedUser = authenticate(username=request.POST["usernameInput"].lower(), password=request.POST['password'])
    if loggedUser is not None:
        login(request, loggedUser)
        print("FF")
        return  render(request, 'medapp/base.html')

    else:
        context['notLoggedMsg'] = "This pair of username/password was not found!"
        return render (request, 'medapp/logIn.html', context)

@login_required
def sendMails(request):
    #data = xlsx_get('/Users/huseynkuliev/Downloads/a.xlsx', column_limit=5)
    data2 = request.FILES['uploadedFile']
    #if (str(data2).split('.')[-1] == "xls"):
        #data = xls_get(data2, column_limit=5)
    #elif (str(data2).split('.')[-1] == "xlsx"):
    data = xlsx_get(data2, column_limit=5)
    i = 0
    userdata = data['sheet']
    print(userdata[0])
    for u in userdata:
        if u[0] == "username":
            print("empty")
        elif u[0] == "":
            print("empty")
        else:
            str2 = "Уважаемый участники Олимпиады! \n Напоминаем вам,что необходимо пройти экзаменационные испытания в срок с 1 июля 00:00 по 4 июля 23:59. \n Платформа для прохождения олимпиады: https://examus.sechenov.ru/login/index.php \n Ваш логин: " + str(u[0]) + " \n Пароль: " + str(u[1]) + " \n Удачи! \n \n Dear Olympiad participants! \n We remind you that you need to pass the examinations from July 1 00:00 to July 4 23:59. \n Platform for passing the Olympiad: https://examus.sechenov.ru/login/index.php \n Your Username: " + str(u[0]) + " \n Password: " + str(u[1]) + " \n Good luck!" 



            print(str2)
            print(str(i))


            #print(str(u[0]) + " " + str(u[1]) + " " + str(u[2]) + " " + str(u[3]) + " " + str(u[4]))
            #try:
            send_mail('Олимпиада(Olympiad)', str2, 'interolymp@staff.sechenov.ru', [u[2]])
            #except Exception as e:
             #   print(str(u[2]))
            #    print("This email is invalid")

            i = i + 1

            #if i == 5:
                #time.sleep(1)
                #send_mail('Olympiad 4', '4 отправлено, ждём ...', 'interolymp@staff.sechenov.ru', ['interolymp@staff.sechenov.ru'])
                #i = 1


    print("Send")
    send_mail('Olympiad', 'Всё отправлено успешно! Письма высланы на почты! \n Всего доброго!', 'interolymp@staff.sechenov.ru', ['interolymp@staff.sechenov.ru'])
    print("Send")   

    return render (request, 'medapp/base.html')
     
