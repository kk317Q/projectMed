"""projectMed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
from .views import index, searchDoctor, showDoctorPage, signUp, logIn, goSignUp, goLogIn, goLogOut, checkUsername, showDocPage, requestConsultancy, getRequestData, actionOnRequest, anamnesis, editAnamnesis, anamnesisToDoctor, registryToDoctor, getProfile, editProfilePatient, editProfileDoctor, editProfileField, changePassword, favouriteDoctor, likeDoctor, getRegistry, createNewIllness, getIllnessData, editTreatment, createNewTreatment, getTreatmentData, editIllness, getConsultancy, editConsultancyField, closeConsultancy, sendMails, createArticle, writeArticle, goToEditArticle, editArticleData, viewArticleToApprove, approveArticle, likeArticle, favouriteArticle, articlesSection, searchArticles, showFullArticle, createArticleReview, editReviewField, createResponseOnReview, processPhoto, addIllnessFiles, addRequestFiles, addConsultancyFiles, addTreatmentFiles, deleteIllnessFile, deleteTreatmentFile, deleteConsultancyFile, deleteRequestFile, deleteDoctorFile, addDoctorsFiles, createChatMessage, checkChatMessages, deleteResponseReview, deleteArticleReview, deleteIllness, deleteTreatment, deleteArticle


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('checkChatMessages', checkChatMessages, name = 'checkChatMessages'),
    path('createChatMessage', createChatMessage, name = 'createChatMessage'),
    path('deleteResponseReview/<responseID>/<articleID>/', deleteResponseReview, name = "deleteResponseReview"),
    path('deleteArticleReview/<reviewID>/<articleID>/', deleteArticleReview, name = "deleteArticleReview"),



    path('processPhoto', processPhoto, name = 'processPhoto'),
    path('deleteRequestFile/<requestFileID>/', deleteRequestFile, name = 'deleteRequestFile'),

    path('deleteIllnessFile/<illnessFileID>/', deleteIllnessFile, name = 'deleteIllnessFile'),
    path('deleteTreatmentFile/<treatmentFileID>/', deleteTreatmentFile, name = 'deleteTreatmentFile'),
    path('deleteConsultancyFile/<consultancyFileID>/', deleteConsultancyFile, name = 'deleteConsultancyFile'),

    

    
    path('addDoctorsFiles', addDoctorsFiles, name = 'addDoctorsFiles'),
    path('deleteDoctorFile/<doctorFileID>/', deleteDoctorFile, name = 'deleteDoctorFile'),

    path('addConsultancyFiles', addConsultancyFiles, name = 'addConsultancyFiles'),
    path('addRequestFiles', addRequestFiles, name = 'addRequestFiles'),
    path('addIllnessFiles', addIllnessFiles, name = 'addIllnessFiles'),
    path('addTreatmentFiles', addTreatmentFiles, name = 'addTreatmentFiles'),

    path('createArticleReview', createArticleReview, name = 'createArticleReview'),
    path('createResponseOnReview', createResponseOnReview, name = 'createResponseOnReview'),
    path('editReviewField', editReviewField, name = 'editReviewField'),
    path('createArticle', createArticle, name = 'createArticle'),
    path('writeArticle', writeArticle, name = 'writeArticle'),
    path('likeArticle', likeArticle, name = 'likeArticle'),
    path('favouriteArticle', favouriteArticle, name = 'favouriteArticle'),
    path('articlesSection', articlesSection, name = 'articlesSection'),
    path('browseAsearchArticlesrticles', searchArticles, name = 'searchArticles'),
    path('showFullArticle/<articleID>/', showFullArticle, name = 'showFullArticle'),

    path('goToEditArticle/<articleID>/', goToEditArticle, name = 'goToEditArticle'),
    path('editArticleData', editArticleData, name = 'editArticleData'),
    path('viewArticleToApprove/<articleID>/', viewArticleToApprove, name = 'viewArticleToApprove'),
    path('approveArticle', approveArticle, name = 'approveArticle'),
    path('deleteArticle/<articleID>/', deleteArticle, name = 'deleteArticle'),


    path('sendMails', sendMails, name = 'sendMails'),
    path('searchDoctor', searchDoctor, name='searchDoctor'),
    path('showDoctorPage', showDoctorPage, name='showDoctorPage'),
    path('favouriteDoctor', favouriteDoctor, name = 'favouriteDoctor'),
    path('likeDoctor', likeDoctor, name = 'likeDoctor'),
    path('showDocPage/(?P<user_name>\w+)$', showDocPage, name = 'showDocPage'),
    path('getConsultancy/<consultancyID>/', getConsultancy, name = 'getConsultancy'),
    path('actionOnRequest', actionOnRequest, name = 'actionOnRequest'),
    path('getRequestData', getRequestData, name = 'getRequestData'),
    path('closeConsultancy', closeConsultancy, name = 'closeConsultancy'),
    path('editConsultancyField', editConsultancyField, name = 'editConsultancyField'),
    path('requestConsultancy', requestConsultancy, name = 'requestConsultancy'),

    path('deleteTreatment/<treatmentID>/', deleteTreatment, name = 'deleteTreatment'),
    path('createNewTreatment', createNewTreatment, name = 'createNewTreatment'),
    path('getTreatmentData', getTreatmentData, name = 'getTreatmentData'),
    path('editTreatment', editTreatment, name = 'editTreatment'),
    path('deleteIllness/<illnessID>/', deleteIllness, name = 'deleteIllness'),
    path('createNewIllness', createNewIllness, name = 'createNewIllness'),
    path('getIllnessData', getIllnessData, name = 'getIllnessData'),
    path('editIllness', editIllness, name = 'editIllness'),
    path('registryToDoctor/<patientID>/', registryToDoctor, name = 'registryToDoctor'),
    path('getRegistry', getRegistry, name = 'getRegistry'),
    path('anamnesis', anamnesis, name = 'anamnesis' ),
    path('editAnamnesis', editAnamnesis, name = 'editAnamnesis' ),
    path('anamnesisToDoctor/<patientID>/', anamnesisToDoctor, name = 'anamnesisToDoctor'),
    path('checkUsername', checkUsername, name = 'checkUsername'),
    path('editProfileField', editProfileField, name = 'editProfileField'),
    path('editProfilePatient', editProfilePatient, name = 'editProfilePatient'),
    path('editProfileDoctor', editProfileDoctor, name = 'editProfileDoctor'),
    path('changePassword', changePassword, name = 'changePassword'),
    path('getProfile', getProfile, name = 'getProfile'),
    path('goSignUp', goSignUp, name='goSignUp'),
    path('goLogIn', goLogIn, name='goLogIn'),
    path('goLogOut', goLogOut, name='goLogOut'),
    path('signUp', signUp, name='signUp'),
    path('logIn', logIn, name='logIn'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
