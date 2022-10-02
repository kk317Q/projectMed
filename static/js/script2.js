

function  displayInput(elementClicked) {

  document.getElementById(elementClicked.getAttribute('for')).style.display = "inline";
  document.getElementById(elementClicked.getAttribute('for')+'Btn').style.display = "inline";

}

function respondOnReview(elementClicked) {
  csrfT = getCookie('csrftoken')
  neededInputElements = document.getElementsByTagName('input')
  inputValue = " ";
  for(n in neededInputElements){
    



    if(neededInputElements[n].dataset.targetid == elementClicked.dataset.neededid){
      console.log('imstu')
      inputValue = neededInputElements[n].value
      break
    }
  }
  $.ajax({
    url: $('#' + elementClicked.id).data('url'),
    method: 'POST',
    data: {
      responseText : inputValue,
      reviewArticleID: $('#' + elementClicked.id).data('reviewid'),
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data) {
      neededId = $('#' + elementClicked.id).data('reviewid')
      document.getElementById('commentResult'+neededId).innerHTML = "Successfully sent!"
      document.getElementById('commentResult'+neededId).style.color = "green"


      setTimeout(function(){
        elementClicked.innerHTML = "Save"
        document.getElementById('commentResult'+neededId).innerHTML = ""
        document.getElementById('commentResult'+neededId).style.color = ""
        document.getElementById('reviewResponseInput' +  $('#' + elementClicked.id).data('reviewid')).style.display = "none";
        elementClicked.style.display = "none";
        location.reload()

        


      }, 1000);


    }
  })

  
}

function changeReviewArticleField(elementClicked) {
  csrfT = getCookie('csrftoken')
  neededElement = document.getElementById($('#' + elementClicked.id).data('textneededid'))
  inputValue = neededElement.value
  console.log(inputValue + $('#' + elementClicked.id).data('fieldtosave'))

  $.ajax({
    url: $('#' + elementClicked.id).data('url'),
    method: 'POST',
    data: {
      fieldToChange : $('#' + elementClicked.id).data('fieldtosave'),
      newData: inputValue,
      objectType: $('#' + elementClicked.id).data('commenttype'),
      reviewArticleID: $('#' + elementClicked.id).data('reviewid'),
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data){
      elementClicked.innerHTML = "New data is saved!"
      setTimeout(function(){
        elementClicked.innerHTML = "Save"

      }, 3000);

    }
  })
  
}


function sendArticleReview(elementClicked){
  csrfT = getCookie('csrftoken')
  rating = $('#ratingValueToPass').val()
  reviewText = $('#reviewAboutArticle').val()
  articleIDD = $('#articleID').val()


  $.ajax({
    url: elementClicked.dataset.url,
    method: 'POST',
    data: {
      articleID: articleIDD,
      reviewAboutArticle: reviewText,
      ratingToArticle: rating,
      csrfmiddlewaretoken:  csrfT,

    },
    success: function (data) {

      if(data.exists == "True"){
        document.getElementsByClassName('modal-title')[0].innerHTML = 'You can send only 1 review!'
        document.getElementsByClassName('modal-title')[0].style.backgroundColor = 'red'
        document.getElementsByClassName('modal-title')[0].style.transitionDuration = '400ms'
        document.getElementsByClassName('modal-header')[0].style.backgroundColor = 'red'
        document.getElementsByClassName('modal-header')[0].style.transitionDuration = '400ms'
        
        
      }
      else{
        document.getElementsByClassName('modal-title')[0].innerHTML = 'Review is successfully sent!'
        document.getElementsByClassName('modal-title')[0].style.backgroundColor = 'green'
        document.getElementsByClassName('modal-title')[0].style.transitionDuration = '400ms'
        document.getElementsByClassName('modal-header')[0].style.backgroundColor = 'green'
        document.getElementsByClassName('modal-header')[0].style.transitionDuration = '400ms'
        

      }

     
      setTimeout(function(){
        $('.modal').modal('hide')
        location.reload()


      }, 1000);
      

      
    }
})
}

function sendApproval(elementClicked){
  csrfT = getCookie('csrftoken')
  $.ajax({
    url: elementClicked.dataset.url,
    method: 'POST',
    data: {
      articleID: elementClicked.dataset.articleid,
      action: elementClicked.dataset.action,
      csrfmiddlewaretoken:  csrfT,

    },
    success: function (data) {
      console.log(elementClicked.dataset.action)
      document.getElementsByClassName('approvedByNum')[0].innerHTML = data.numOfApprovals + " Approvals"
      
      if(elementClicked.dataset.action == "Approve"){
        elementClicked.innerHTML = "Unapprove Article"
        elementClicked.setAttribute('data-action', 'Unapprove')
        elementClicked.style.backgroundColor = '#62686b';
        elementClicked.style.borderColor = '#62686b';
        elementToModify = document.getElementsByClassName('btnDisapprove')[0]

        if(elementToModify.dataset.action == "Undisapprove"){
          elementToModify.innerHTML = "Disapprove Article"
          elementToModify.setAttribute('data-action', 'Disapprove')
          elementToModify.style.backgroundColor = '';
          elementToModify.style.borderColor = '';
        }

      }
      else if(elementClicked.dataset.action == "Unapprove"){
        elementClicked.innerHTML = "Approve Article"
        elementClicked.setAttribute('data-action', 'Approve')
        elementClicked.style.backgroundColor = '';
        elementClicked.style.borderColor = '';
      }
      else if(elementClicked.dataset.action == "Disapprove")
      {
        elementClicked.innerHTML = "Undisapprove Article"
        elementClicked.setAttribute('data-action', 'Undisapprove')
        elementClicked.style.backgroundColor = '#62686b';
        elementClicked.style.borderColor = '#62686b';

        elementToModify = document.getElementsByClassName('btnApprove')[0]

        if(elementToModify.dataset.action == "Unapprove"){
          console.log("gosleep")
          elementToModify.innerHTML = "Approve Article"
          elementToModify.setAttribute('data-action', 'Approve')
          elementToModify.style.backgroundColor = '';
          elementToModify.style.borderColor = '';
        }
      }
      else if(elementClicked.dataset.action == "Undisapprove")
      {
        elementClicked.innerHTML = "Disapprove Article"
        elementClicked.setAttribute('data-action', 'Disapprove')
        elementClicked.style.backgroundColor = '';
        elementClicked.style.borderColor = '';
      }
      console.log("Success")

    }
  })
}

function endConsultancy(elementClicked){
  csrfT = getCookie('csrftoken')

  $.ajax({
    url: elementClicked.dataset.url,
    method: 'POST',
    data: {
      consultancyID: elementClicked.dataset.consultancyid,
      ratingValueToPass: $("#ratingValueToPass").val(),
      reviewMSG: $("#reviewAboutPatient").val(),
      csrfmiddlewaretoken:  csrfT,

    },
    success: function (data) {

      document.querySelector(' .btnApprove').style.display = "none";
      document.querySelector(' .btnDisapprove').style.display = "none";

      smallBtns = document.getElementsByClassName('smallBtn')
      for(s in smallBtns){
        console.log(smallBtns[s])
        //smallBtns[s].style.display = "none";
      }


      console.log(data.action)
      document.getElementById('statusOfClose').innerHTML = data.await;

      setTimeout(function(){
        $('.modal').modal('hide')
       


      }, 500);
    }
  })
}

function colorStarsFinal(elementClicked){
  starsParent = document.getElementById("ratingBlock")
  stars = starsParent.getElementsByClassName("fa")
  
  for(var i = 0; i<5; i++){

    if(i==0){
      stars[i].className = "fa fa-star "
      stars[i].style.transitionDuration = '500ms';
      stars[i].setAttribute('data-clicked', "false")

      
    }
    else{
      stars[i].className = "fa fa-star "
      stars[i].style.transitionDuration = '500ms';
      stars[i].setAttribute('data-clicked', "false")



    }
    
  
}

  for(var i = 0; i<parseInt(elementClicked.dataset.ratingvalue, 10); i++){

    if(i==0){
      stars[i].className = "fa fa-star checked "
      stars[i].style.transitionDuration = '500ms';
      stars[i].setAttribute('data-clicked', "true")


      
    }
    else{
      stars[i].className = "fa fa-star checked "
      stars[i].style.transitionDuration = '500ms';
      stars[i].setAttribute('data-clicked', "true")


    }


    
  
}
document.getElementById("ratingValueToPass").value = parseInt(elementClicked.dataset.ratingvalue, 10)
}

function colorStars(elementClicked){
  starsParent = document.getElementById("ratingBlock")
  stars = starsParent.getElementsByClassName("fa")
  for(var i = 0; i<parseInt(elementClicked.dataset.ratingvalue, 10); i++){

    if(i==0){
        stars[i].className = "fa fa-star checked "
        stars[i].style.transitionDuration = '500ms';
      
      

      
    }
    else{
        stars[i].className = "fa fa-star checked "
        stars[i].style.transitionDuration = '500ms';
      
      

    }
    
  
}
}

function colorStarsOpposite(elementClicked){

    starsParent = document.getElementById("ratingBlock")
    stars = starsParent.getElementsByClassName("fa")
    for(var i = 0; i<parseInt(elementClicked.dataset.ratingvalue, 10); i++){
  
      if(i==0){
        if(stars[i].dataset.clicked == "false"){

        stars[i].className = "fa fa-star"
        stars[i].style.transitionDuration = '5000ms';
        }
        
      }
      else{
        if(stars[i].dataset.clicked == "false"){

        stars[i].className = "fa fa-star"
        stars[i].style.transitionDuration = '5000ms';
        }
      }
      
    
  }
}


function consultancyInput(elementClicked) {
  csrfT = getCookie('csrftoken')
  neededElement = document.getElementById($('#' + elementClicked.id).data('textneededid'))
  inputValue = neededElement.value
  /*inputValue = inputValue.replace(/<br>/g, "");
  inputValue = inputValue.replace(/<div>/g, "");
  inputValue = inputValue.replace(/<\/div>/g, "");*/


  console.log(inputValue + $('#' + elementClicked.id).data('fieldtosave'))

  $.ajax({
    url: $('#' + elementClicked.id).data('url'),
    method: 'POST',
    data: {
      fieldToChange : $('#' + elementClicked.id).data('fieldtosave'),
      newData: inputValue,
      consultancyID: $('#' + elementClicked.id).data('consultancyid'),
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data){
      elementClicked.innerHTML = "New data is saved!"
      setTimeout(function(){
        elementClicked.innerHTML = "Save"

       

        


      }, 3000);

    }
  })
  
}

function respondRequest(elementClicked, actionToRequest){
  csrfT = getCookie('csrftoken')
  neededID = elementClicked.dataset.requestid;

  $.ajax({
    url: elementClicked.dataset.url,
    method: 'POST',
    data: {
      requestID: elementClicked.dataset.requestid,
      action: actionToRequest,
      csrfmiddlewaretoken:  csrfT,

    },
    success: function (data) {

      document.querySelector('#viewRequest .btnApprove').style.display = "none";
      document.querySelector('#viewRequest .btnDisapprove').style.display = "none";
      //document.querySelector('#viewRequest .btnReaddress').style.display = "none";
      console.log(data.action)
      document.getElementById('actionResult').innerHTML = "Request was " + data.action + "!";
      
      console.log(document.getElementById('actionResult'))



      requestList = document.getElementsByClassName('RequestBlock');
      requestList2 = requestList[0].getElementsByTagName('a');
      for (a in  requestList2){
        console.log(requestList2[a].dataset.requestid)
        console.log(neededID)
        if(requestList2[a].dataset.requestid == neededID){
          statusElement = requestList2[a].getElementsByTagName('span')[0];
          if(data.action == "Agreed"){
              statusElement.innerHTML = "Agreed"
              statusElement.className = "solved";
              document.getElementById('actionResult').style.color = 'green'
              a = document.createElement("a");
              a.className = "-"
              a.innerHTML ="~&nbsp;&nbsp;" + data.full_name + "&nbsp;&nbsp;" + data.age + " | Status: "
              urlToSet = 'getConsultancy/' + data.consultancyID + '/'
              a.setAttribute('href', urlToSet)    

              s = document.createElement("span");
              s.innerHTML = data.status

              if(data.status == "Active"){
                s.className = "requestStatus inProcess" 
              }
              else if(data.status == "Closed"){
                s.className = "requestStatus solved" 
              }
              else if(data.status == "Dispute"){
                s.className = "requestStatus notSolved" 

              }

              a.appendChild(s)
              document.querySelector(".CurrentConsultancy").appendChild(a);
          }
          else if(data.action == "Rejected"){
            statusElement.innerHTML = "Rejected"
            statusElement.className = "notSolved";
            document.getElementById('actionResult').style.color = 'red'


          }
          else{
            statusElement.className = "notSolved";

          }

          break;

        }

      }
      

      setTimeout(function(){
        $('.modal').modal('hide')
        document.getElementById('actionResult').style.color = 'black'
        document.getElementById('actionResult').innerHTML = ''


      }, 1000);

      
      document.querySelector('#viewRequest .btnApprove').style.display = "display";
      document.querySelector('#viewRequest .btnDisapprove').style.display = "display";
      //document.querySelector('#viewRequest .btnReaddress').style.display = "display";




      

      
    },
    error: function() {
    
    console.log("Error")   ;   
    }

  })
}


function getRequestData(elementClicked){
  csrfT = getCookie('csrftoken')
  console.log(elementClicked)

  $.ajax({
    url: elementClicked.dataset.url,
    method: 'GET',
    data: {
      requestID: elementClicked.dataset.requestid,
    },
    success: function(data){
      console.log(data.filesURL[0])
      document.querySelector('#viewRequest #hiddenID').value = elementClicked.dataset.requestid;

      neededElement = document.getElementsByClassName('filesBlock')[0]
      console.log(neededElement)

      for(f in data.filesURL){
        console.log("here")

      
  
        e1 = document.createElement('embed')
        e1.setAttribute('src', data.filesURL[f])
        e1.setAttribute('width',"300px")
        e1.setAttribute('height',"200px")
        

        neededElement.appendChild(document.createElement('br'))
        neededElement.appendChild(e1)
        console.log(neededElement)

        neededElement.appendChild(document.createElement('br'))

        if(data.isDoctor == "False"){
        
        a2 = document.createElement('a')
        a2.setAttribute('href', '/deleteRequestFile/' + data.illnessFileID[f] + '/')
        a2.className = "label"
        b2 = document.createElement('button')
        b2.innerHTML = "Delete"
        b2.className = "smallBtn"
        a2.appendChild(b2)  
        neededElement.appendChild(a2)

      

        }
        a1 = document.createElement('a')
        a1.setAttribute('href', data.filesURL[f])
        a1.className = "documents"
        b1 = document.createElement('button')
        b1.innerHTML = "Download"
        b1.className = "smallBtn"
        a1.appendChild(b1)  

       
        neededElement.appendChild(a1)

       
        


       





      }

      starsParent = document.getElementById("profileDetailBlockID")
      stars = starsParent.getElementsByClassName("fa")
      
      for(var i = 0; i<parseInt(data.ratingvalue, 10); i++){

        if(i==0){
          stars[i].className = "fa first fa-star checked "
          stars[i].style.transitionDuration = '500ms';
          stars[i].setAttribute('data-clicked', "true")
    
    
          
        }
        else{
          stars[i].className = "fa fa-star checked "
          stars[i].style.transitionDuration = '500ms';
          stars[i].setAttribute('data-clicked', "true")
    
    
        }
    
    
        
      
    }
     
      document.querySelector('#requestIMG').setAttribute('src', data.imageURL);
      document.querySelector('#viewRequest #staticBackdropLabel').innerHTML = "Pending Request No: " + data.requestNo;
      document.querySelector('#viewRequest #patientFullName').innerHTML = data.full_name;
      document.querySelector('#viewRequest #patientLocation').innerHTML = data.location;
      document.querySelector('#viewRequest #patientDOB').innerHTML = data.dob; 
      document.querySelector('#viewRequest #requestMessage').innerHTML = data.message;
      

      //<a href="{{illnesfile.fileI.url}}"   class="documents"  download="patient_nameFileName"><embed src="{{illnesfile.fileI.url}}" width="300px" height="200px" /> </a>


      


      if(data.status != "Pending"){
        document.querySelector('#viewRequest .btnApprove').style.display = "none";
        document.querySelector('#viewRequest .btnDisapprove').style.display = "none";
        //document.querySelector('#viewRequest .btnReaddress').style.display = "none";

        
      }
      else{
        document.querySelector('#viewRequest #btnApprove').setAttribute('data-requestid', elementClicked.dataset.requestid); 
        document.querySelector('#viewRequest #btnDisapprove').setAttribute('data-requestid', elementClicked.dataset.requestid); 
        //document.querySelector('#viewRequest #btnReaddress').setAttribute('data-requestid', elementClicked.dataset.requestid); 
        document.querySelector('#viewRequest .btnApprove').style.display = "inline";
        document.querySelector('#viewRequest .btnDisapprove').style.display = "inline";
       // document.querySelector('#viewRequest .btnReaddress').style.display = "inline";
      }
        
     
    }
  })

}


function getIllnessData(elementClicked){
  csrfT = getCookie('csrftoken')
  

  $.ajax({
    url: $(elementClicked).data('url'),
    method: 'GET',
    data: {
      illnessID: elementClicked.id,
    },
    success: function(data){
      alert(data.specialization)
      document.querySelector('#editIllnessWindow #InputDiagnose').value = data.diagnose;
      document.querySelector('#editIllnessWindow #InputDescribtion').value = data.describtion;
      document.querySelector('#editIllnessWindow #InputDateOfIllness').value = data.date; 
      document.querySelector('#editIllnessWindow #InputIllnessID').value = elementClicked.id; 
      specializations = data.specialization.split(" ");
      listOfElements = document.getElementsByClassName('specializationOption')
      console.log(listOfElements[0].children[0].value)
      for(var r = 0; r<listOfElements.length; r++) {
          listOfElements[r].children[0].checked = false;
        
        
        
      }

      for(var i = 0; i<specializations.length; i++){
        for(var r = 0; r<listOfElements.length; r++) {
          if(listOfElements[r].children[0].value == specializations[i]){

            listOfElements[r].children[0].checked = true;
          
          }
          
        }
      }

      if(data.active == true){
        document.querySelector('#editIllnessWindow #illnessStateActiveE').checked = true;
        document.querySelector('#editIllnessWindow #illnessStateSolvedE').checked = false;
        
      }
      else if(data.active == false){
        document.querySelector('#editIllnessWindow #illnessStateActiveE').checked = false;
        document.querySelector('#editIllnessWindow #illnessStateSolvedE').checked = true;
      }
    }
  })

}

function getTreatmentData(elementClicked){
  csrfT = getCookie('csrftoken')
  

  $.ajax({
    url: $(elementClicked).data('url'),
    method: 'GET',
    data: {
      treatmentID: elementClicked.id,
    },
    success: function(data){
      alert(data.specialization)
      document.querySelector('#editTreatmentWindow #InputMethodology').value = data.methodology;
      document.querySelector('#editTreatmentWindow #InputDescribtion').value = data.describtion;
      document.querySelector('#editTreatmentWindow #InputDateOfTreatment').value = data.date; 
      document.querySelector('#editTreatmentWindow #InputTreatmentID').value = elementClicked.id; 
      
      specializations = data.specialization.split(" ");
      listOfElements = document.getElementsByClassName('specializationOption')
      console.log(listOfElements[0].children[0].value)
      for(var r = 0; r<listOfElements.length; r++) {
          listOfElements[r].children[0].checked = false;
        
        
        
      }

      for(var i = 0; i<specializations.length; i++){
        for(var r = 0; r<listOfElements.length; r++) {
          if(listOfElements[r].children[0].value == specializations[i]){

            listOfElements[r].children[0].checked = true;
          
          }
          
        }
      }

      if(data.result == 'Solved'){
        document.querySelector('#editTreatmentWindow #treatmentResultSolvedE').checked = true;
        document.querySelector('#editTreatmentWindow #treatmentResultInProcessE').checked = false;
        document.querySelector('#editTreatmentWindow #treatmentResultNotSolvedE').checked = false;

        
      }
      else if(data.result == "inProcess"){
        document.querySelector('#editTreatmentWindow #treatmentResultSolvedE').checked = false;
        document.querySelector('#editTreatmentWindow #treatmentResultInProcessE').checked = true;
        document.querySelector('#editTreatmentWindow #treatmentResultNotSolvedE').checked = false;
      }
      else if(data.result == "notSolved"){
        document.querySelector('#editTreatmentWindow #treatmentResultSolvedE').checked = false;
        document.querySelector('#editTreatmentWindow #treatmentResultInProcessE').checked = false;
        document.querySelector('#editTreatmentWindow #treatmentResultNotSolvedE').checked = true;
      }
    }
  })

}

function showIllnesses(elementClicked, neededClass){
  ourIllnesses = document.getElementsByClassName(neededClass);
  if(elementClicked.className == "showBtn"){
    for(var i = 0; i<ourIllnesses.length; i++){

      ourIllnesses[i].style.display = 'block';


      
    }

    elementClicked.setAttribute('src', '/static/images/closeMenu.png');
    elementClicked.className = "hideBtn";

  }
  else{
    for(var i = 0; i<ourIllnesses.length; i++){

      ourIllnesses[i].style.display = 'none';


    }

    elementClicked.setAttribute('src', '/static/images/openMenu.png');
    elementClicked.className = "showBtn";

  } 

  
}

function likeFavDoctor(elementClicked){
  targetDocId = elementClicked.id;

  console.log(elementClicked.id)
  console.log(elementClicked.className)
  console.log($(elementClicked).data('url'))


  csrfT = getCookie('csrftoken')

  $.ajax({
    url: $(elementClicked).data('url'),
    method: 'POST',
    data: {
      targetDoctor: targetDocId,
      csrfmiddlewaretoken:  csrfT,
    },
    success: function(data){
      if(data == "Like"){
        console.log(data)
        //$(elementClicked).attr('class', 'likeBtn likedBtn');
        elementClicked.className = "likeBtn likedBtn";

      }
      else if(data == "Dislike"){
        console.log(data)

        elementClicked.className = "likeBtn";
      }
      else if(data == "Favourite"){
        console.log(data)

        elementClicked.className = "favBtn favedBtn";
      }
      else if(data == "Unfavourite"){
        console.log(data)

        elementClicked.className = "favBtn";
      }
    }
  })
}

$(document).on('click', '#InputAccountType', (function(){

    if ($("#InputAccountType").prop("checked") == true)
    {
        $(".forDoctorSignUp").show()

        document.getElementById("InputEducation").required = true;
        document.getElementById("InputExperience").required = true;
    }
    else
    {
        $(".forDoctorSignUp").hide()
        document.getElementById("InputEducation").required = false;
        document.getElementById("InputExperience").required = false;

    }

}))



$(document).on('click', '.saveChange', (function(){
    saveElement = this;

    sendAnamnesisChange(saveElement);
    

}))

//url: '{% url "anamnesis" %}',

function sendAnamnesisChange(saveElement){
  csrfT = getCookie('csrftoken')
  inputValue = getInputElement(saveElement.id)

  if(saveElement.id == "malefemale"){
    if(document.getElementsByClassName('malefemale')[0].checked)
    {
      inputValue = document.getElementsByClassName('malefemale')[0].value;
    }
    else{
      inputValue = document.getElementsByClassName('malefemale')[1].value;
    }
  }

  $.ajax({
    url: $('#' + saveElement.id).data('url'),
    method: 'POST',
    data: {
      fieldToChange : saveElement.id,
      newData: inputValue,
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data){
      if(saveElement.id == "dob"){
        for(l in document.getElementsByTagName('label')){
          if (document.getElementsByTagName('label')[l].htmlFor == 'InputDOB'){
            document.getElementsByTagName('label')[l].innerHTML = "Date of Birth ff: " + data;
  
  
          }
        }
      }

  
      saveElement.innerHTML = "New value was saved!"
      saveElement.style.color = "white"
      saveElement.style.backgroundColor = "#0e3854"
      saveElement.style.borderColor = "#0e3854"


      setTimeout(function(){
        saveElement.innerHTML = "Save"
        saveElement.style.backgroundColor = ""
        saveElement.style.borderColor = ""
        saveElement.style.color = ""





      }, 3000);

    }
  })
}

function getInputElement(idToSearch){
  if(idToSearch == 'specialization'){
    newSpecializations = ''
    allInputs = document.getElementsByClassName('specializationOption');
    for(a in allInputs){
      if(allInputs[a].checked){
        newSpecializations = newSpecializations + " " + allInputs[a].value;
      }
    }
    if(newSpecializations.charAt(0) == " "){
      newSpecializations = newSpecializations.substring(1);
    }
    alert(newSpecializations);
    return newSpecializations
  }
  else{
    allInputs = document.getElementsByTagName('input');

    for(a in allInputs){
      //console.log(allInputs[a]);
      //console.log(allInputs[a].id);
      //console.log(allInputs[a].value);
      
      if(allInputs[a].getAttribute('name') === idToSearch){
        
        return allInputs[a].value;
  
      }
    }

  }

}


function sendRequestToServer(elementClicked){
  csrfT = getCookie('csrftoken')
  messageID = "messageToSend" + elementClicked.id;
  messageToSend = $("#" + messageID).val();
  $.ajax({
    url: $(elementClicked).data('url'),
    method: 'POST',
    data: {
      targetDoctor: elementClicked.id,
      message: messageToSend,
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data){
      neededID = "modal" + elementClicked.id
      initialTitle = document.getElementById(neededID).innerHTML;

      
      if(data == "OK"){
        document.getElementById(neededID).style.backgroundColor = 'green';
        document.getElementById(neededID).style.transitionDuration = '400ms';
        document.getElementById(neededID).innerHTML = "Request is sucessfully sent!";
      }
      else{
        document.getElementById(neededID).style.backgroundColor = 'red';
        document.getElementById(neededID).style.transitionDuration = '400ms';
        document.getElementById(neededID).innerHTML = "Request was already sent! Do not repeat it!";
        
      }
     
      setTimeout(function(){
        $('.modal').modal('hide')
        document.getElementById(neededID).style.backgroundColor = '';
        document.getElementById(neededID).innerHTML = initialTitle;


      }, 1000);
      

    }
  });
}

function changePassword(){
  
 

  alert(  $("#InputPasswordOld").val())
  idForURL = this.id;
  csrfT = getCookie('csrftoken');


  $.ajax({

    url: $("#passwordConfirmChange").data('url'),
    method: 'POST',
    data: {
      oldPassword: $("#InputPasswordOld").val(),
      newPassword: $("#InputConfirmPassword").val(),
      csrfmiddlewaretoken:  csrfT,


    },
    success: function(data){

      if(data == "noMatch"){
        document.getElementById('passwordValidation').innerHTML = 'Old password is not correct!';
        document.getElementById('passwordValidation').style.color = 'red';


      }
      else{
        document.getElementById('passwordValidation').innerHTML = 'Password is changed!';
        document.getElementById('passwordValidation').style.color = 'green';


      }
   
    }
  })

}

  function checkPasswords() {

    if (document.getElementById('InputConfirmPassword').value == document.getElementById('InputPassword').value) {
      document.getElementById('InputPassword').style.borderColor = 'green';
      document.getElementById('InputConfirmPassword').style.borderColor = 'green';
      document.getElementById('passwordValidation').innerHTML = 'Passwords match';
      document.getElementById('passwordValidation').style.color = 'green';

      if(document.body.contains(document.getElementById('submitSignUp'))){
        document.getElementById('submitSignUp').disabled = false;
      }
      else{
        document.getElementById('passwordConfirmChange').style.visibility = ''; 
        document.getElementById('passwordConfirmChange').disabled = false; 
      }



    } else {
        document.getElementById('InputPassword').style.borderColor = 'red';
        document.getElementById('InputConfirmPassword').style.borderColor = 'red';
        document.getElementById('passwordValidation').innerHTML = 'Passwords do not match! Submit is not availalbe until passwords match';
        document.getElementById('passwordValidation').style.color = 'red';

        if(document.body.contains(document.getElementById('submitSignUp'))){
          document.getElementById('submitSignUp').disabled = true;
        }
        else{
          document.getElementById('passwordConfirmChange').style.visibility = 'hidden'; 
          document.getElementById('passwordConfirmChange').disabled = true; 



        }



    }
  }

  function checkUsername(elementClicked){
    usernameToCheck = document.getElementById('InputUsername');
      if (usernameToCheck.value.includes('+') || usernameToCheck.value.includes('-') || usernameToCheck.value.includes('/') || usernameToCheck.value.includes('*') || usernameToCheck.value.includes('=') || usernameToCheck.value.includes('^') || usernameToCheck.value.includes(';')){
        document.getElementById('usernameValidation').innerHTML = "Username must not contain: +/-;*^=, submit is disabled!";
        document.getElementById('usernameValidation').style.color='red';
        document.getElementById('submitSignUp').disabled = true;

      }
      else{
        document.getElementById('usernameValidation').innerHTML = "";
        document.getElementById('submitSignUp').disabled = false;
        $.ajax({
          url: elementClicked.dataset.url,
          method: 'GET',
          data: {
            usernameToCheck: elementClicked.value,      
      
          },
          success: function(data){
  
            if(data.checkResult == "Exists"){
              document.getElementById('usernameValidation').innerHTML = "Username " + elementClicked.value + " already exists. Submit disabled!";
              document.getElementById('usernameValidation').style.color='red';
              document.getElementById('submitSignUp').disabled = true;

              
            }
            else{
              document.getElementById('usernameValidation').innerHTML = "Username " + elementClicked.value + " is free!";
              document.getElementById('usernameValidation').style.color='green';
              document.getElementById('submitSignUp').disabled = false;
            }
          }
        })

      }
  }
 

  lastdateInputedValue = "";

  /*function inputDOB(){

    dateInputedValue = document.getElementById('InputDOB').value;
    dateInputedElement = document.getElementById('InputDOB');
    checkDateStart("dob", dateInputedValue);
    formatingInputDate(dateInputedValue, lastdateInputedValue);

      lastdateInputedValue = dateInputedValue;

    
  }

  lastexperienceInputedValue = "";

  function inputExperience(){

    dateInputedValue = document.getElementById('InputExperience').value;
    dateInputedElement = document.getElementById('InputExperience');
    checkDateStart("experience", dateInputedValue);
    formatingInputDate(dateInputedValue, lastexperienceInputedValue);

      lastexperienceInputedValue = dateInputedValue;

    
  }*/


  function sendMessageChat(elementClicked) {

    csrfT = getCookie('csrftoken')
    messageToSend = document.getElementById('chatMessageInput').value
    document.getElementById('chatMessageInput').value = ""
    chatIDtoSend = $('#' + elementClicked.id).data('chatid')

    $.ajax({
      url: $('#' + elementClicked.id).data('url'),
      method: 'POST',
      data: {
        newMessage : messageToSend,
        chatID: chatIDtoSend,
        csrfmiddlewaretoken:  csrfT,
  
  
      },
      success: function(data){
        /*
        
        chatNeeded = document.getElementsByClassName('chatBody')[0]
        
        divForChat = document.createElement('div')
        divForChat.className = "chatElement2"
        spanMessage = document.createElement('span')
        spanMessage.className = "chatMessageText"
        spanMessage.innerHTML = data.newMessage
        spanMessageDate = document.createElement('span')
        spanMessageDate.className = "chatMessageDate"
        spanMessageDate.innerHTML = data.messageDate
        divForChat.appendChild(spanMessage)
        divForChat.appendChild(spanMessageDate)
        chatNeeded.appendChild(divForChat)
        document.getElementById('chatBox').scrollTop = 5000


    
        
        setTimeout(function(){
          chatNeeded.removeChild(divForChat)

  
        }, 100);
        */
      }
    })

    
  }

  function formatingInputDate(dateInputedValue, lastdateInputedValue){
    
    firstInputValue = ""
    secondInputValue = "";

    if(dateInputedValue.length<lastdateInputedValue.length){
        
    }   
 
    else if(dateInputedValue.length>3 && dateInputedValue.length<5 && dateInputedValue.substring(3, 4) != "-"){

      dateInputedElement.value = dateInputedValue + '-';

    

    }
    
    else if(dateInputedValue.length>6 && dateInputedValue.length<8 ){

      dateInputedElement.value = dateInputedValue + "-";
    }
    else if(dateInputedValue.length>9){


      dateInputedValue = dateInputedValue.substring(0, 10);
      dateInputedElement.value = dateInputedValue;
        
    }
    else if(dateInputedValue.length == 5 && dateInputedValue.substring(4) != "-"){
      dateInputedElement.value = dateInputedValue.substring(0,4) + "-" + dateInputedValue.substring(4);

    }

    else if(dateInputedValue.length == 6 && dateInputedValue.substring(5, 6) == "-"){

      dateInputedElement.value = dateInputedValue.substring(0,4) + "-" + dateInputedValue.substring(4,5);

    }

    else if(dateInputedValue.length == 6 && dateInputedValue.substring(4, 5) != "-"){

      dateInputedElement.value = dateInputedValue.substring(0,4) + "-" + dateInputedValue.substring(4);


    }

    else if(dateInputedValue.length == 8 && dateInputedValue.substring(7) == "-"){
      dateInputedElement.value = dateInputedValue.substring(0,7) + "-" + dateInputedValue.substring(7,8);
    }

    else if(dateInputedValue.length == 8 && dateInputedValue.substring(7) != "-"){
      dateInputedElement.value = dateInputedValue.substring(0,7) + "-" + dateInputedValue.substring(7);
    }


    else if(dateInputedValue.length == 9 && dateInputedValue.substring(7, 8) != "-"){
      dateInputedElement.value = dateInputedValue.substring(0,7) + "-" + dateInputedValue.substring(7);

    }
   

  }

  function checkDateStart(typeOfInput, dateInputedValue ){

    if(typeOfInput == "dob")
    {

      document.getElementById('dobValidation').innerHTML = "";
      document.getElementById('submitSignUp').disabled = false;


      if( dateInputedValue.substring(0,1) != "1" && dateInputedValue.substring(0,1) != "2"){

        document.getElementById('dobValidation').innerHTML = "No way you were born that time...";
        document.getElementById('dobValidation').style.color = "red";
        document.getElementById('submitSignUp').disabled = true;


      }
      else if(dateInputedValue.substring(0,1) == "1" && dateInputedValue.substring(1,2) != "9"){

        document.getElementById('dobValidation').innerHTML = "No way you were born that time...";
        document.getElementById('dobValidation').style.color = "red";
        document.getElementById('submitSignUp').disabled = true;


      }

        else if(dateInputedValue.substring(0,1) == "2" && dateInputedValue.substring(1,2) != "0")
        {
          document.getElementById('dobValidation').innerHTML = "No way you were born that time...";
          document.getElementById('dobValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;

        }

         if(dateInputedValue.substring(5,6) == "1" && dateInputedValue.substring(6,7) != "2" && dateInputedValue.substring(6,7) != "1" && dateInputedValue.substring(6,7) != "0" ){

          document.getElementById('dobValidation').innerHTML = "No way you were born that time...";
          document.getElementById('dobValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;
        }

        else if(dateInputedValue.length>5 && dateInputedValue.substring(5,6) != "1" && dateInputedValue.substring(6,7) != "0")
        {


          document.getElementById('dobValidation').innerHTML = "No way you were born that time...";
          document.getElementById('dobValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;

        }
        
        
         

    }
    else{

      document.getElementById('experienceValidation').innerHTML = "";
      document.getElementById('submitSignUp').disabled = false;


      if( dateInputedValue.substring(0,1) != "1" && dateInputedValue.substring(0,1) != "2"){

        document.getElementById('experienceValidation').innerHTML = "No way you were born that time...";
        document.getElementById('experienceValidation').style.color = "red";
        document.getElementById('submitSignUp').disabled = true;


      }
      else if(dateInputedValue.substring(0,1) == "1" && dateInputedValue.substring(1,2) != "9"){

        document.getElementById('experienceValidation').innerHTML = "No way you were born that time...";
        document.getElementById('experienceValidation').style.color = "red";
        document.getElementById('submitSignUp').disabled = true;


      }

        else if(dateInputedValue.substring(0,1) == "2" && dateInputedValue.substring(1,2) != "0")
        {
          document.getElementById('experienceValidation').innerHTML = "No way you were born that time...";
          document.getElementById('experienceValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;

        }

         if(dateInputedValue.substring(5,6) == "1" && dateInputedValue.substring(6,7) != "2" && dateInputedValue.substring(6,7) != "1" && dateInputedValue.substring(6,7) != "0" ){

          document.getElementById('experienceValidation').innerHTML = "No way you were born that time...";
          document.getElementById('experienceValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;
        }

        else if(dateInputedValue.length>5 && dateInputedValue.substring(5,6) != "1" && dateInputedValue.substring(6,7) != "0")
        {


          document.getElementById('experienceValidation').innerHTML = "No way you were born that time...";
          document.getElementById('experienceValidation').style.color = "red";
          document.getElementById('submitSignUp').disabled = true;

        }
        
        
    }
    
  }

  //getCookie function referencing
  //Author: Django Org
  //URL: https://docs.djangoproject.com/en/3.1/ref/csrf/
  // Downloaded 04.05.2021
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



$(document).ready(function () {


  if($('#chatBox').length > 0){
    document.getElementById('chatBox').scrollTop = 5000

  setInterval(function() {
    checkMessage()
 
  }, 1000); // 60 * 1000 milsec

  }
  
})

function checkMessage() {

  chatCountMsg = document.getElementById('checkMessage').getAttribute('data-chatcount')
  chatIDtoSend = $('#checkMessage').data('chatid')


$.ajax({
  url: $('#checkMessage').data('url'),
  method: 'GET',
  data: {
    chatID: chatIDtoSend,
    chatCount: chatCountMsg,


  },
  success: function(data){

    console.log('DONEEE')
    console.log('Count in  html')
    console.log(chatCountMsg)
    console.log(data.newCountValue)
    console.log(data.updateInfo)
    chatCountMsg = data.newCountValue
    document.getElementById('checkMessage').setAttribute('data-chatcount', data.newCountValue)
    




    if(data.updateInfo == "newMessageExists"){

      console.log(data.newMessagesList)
      console.log("im here")

      chatNeeded = document.getElementsByClassName('chatBody')[0]

      for(m in data.newMessagesList){
        //Remove below if: if you agree not to display just sent msg immediately!
        
        

        if(data.authorList[m] == $('#checkMessage').data('username')){
          console.log(data.authorList[m])
          console.log($('#checkMessage').data('username'))

          divForChat = document.createElement('div')
          divForChat.className = "chatElement2"
          

        }
        else{
          divForChat = document.createElement('div')
          divForChat.className = "chatElement"
        }

          spanMessage = document.createElement('span')
          spanMessage.className = "chatMessageText"
          spanMessage.innerHTML = data.newMessagesList[m]
          spanMessageDate = document.createElement('span')
          spanMessageDate.className = "chatMessageDate"
          spanMessageDate.innerHTML = data.messageDatesList[m]
          divForChat.appendChild(spanMessage)
          divForChat.appendChild(spanMessageDate)
          chatNeeded.appendChild(divForChat)
        
      
      }

      document.getElementById('chatBox').scrollTop = 5000

    }
    
    
    
    



  }
})


console.log('i work')
  
}

function checkEnterBtn(event) {
   // Number 13 is the "Enter" key on the keyboard
   if (event.key === "Enter") {
    // Cancel the default action, if needed
    
    // Trigger the button element with a click
    document.getElementById("sendMessageInput").click();
  }

  
}


function showAdviceLabel(elementClicked) {

  labelID = $(elementClicked).data('labelid')

  document.getElementById(labelID).style.visibility = "visible"
  document.getElementById(labelID).style.transitionDuration = "1000ms"

  
}

function hideAdviceLabel(elementClicked) {

  labelID = $(elementClicked).data('labelid')

  document.getElementById(labelID).style.visibility = "hidden"
  document.getElementById(labelID).style.transitionDuration = "2000ms"


  
}