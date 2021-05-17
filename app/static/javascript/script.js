function openSection(evt, sectionNames) {
  let i, tabcontent, tablinks;
  console.log(sectionNames);
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  for (i = 0; i < sectionNames.length; i++) {
    document.getElementById(sectionNames[i]).style.display = "block";
  }
  evt.currentTarget.className += " active";
}

/*function saveQuestion() {
  console.log("started")
}

function submitAnswer = () => {
    sessionStorage.setItem("isSubmitted", true);
    const userId = sessionStorage.getItem("userId");
    const questionId = sessionStorage.getItem("questionId");
    const answer = document.querySelector("#question-answer").value;
  };


function selectAnswer() {

}

$(document).ready(function() {


  function saveQuestion() {
    console.log("started")
  }

  function getResponses() {
    
  }

  $.post("submit_answer/"+questionId, {
    submitAnswer();
  });

  $('#save-btn').click(function() {
    saveQuestion();
  });


});*/