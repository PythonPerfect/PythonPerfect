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

$(document).ready(function() {
  $('#submit').click(function() {
    var question = getElementsByClassName('question');
    $.post("/submit_answer"), 
      {
        question: question,
      },
      function () {
        console.log("success")
      };
  });

});