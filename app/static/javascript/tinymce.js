/* 
  source: https://www.tiny.cloud/
  modified by: Dhruv Jobanputra
*/
tinymce.init({
  selector: "#Content-Editor",
  plugins:
    "a11ychecker advcode casechange formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker",
  resize: false,

  toolbar:
    "undo redo | styleselect | code | bold italic | alignleft aligncenter alignright alignjustify | outdent indent",
  toolbar_mode: "floating",
  tinycomments_mode: "embedded",
  tinycomments_author: "Author name",
  setup: function (ed) {
    ed.on("keydown", function (event) {
      if (event.keyCode == 9) {
        // tab pressed
        if (event.shiftKey) {
          ed.execCommand("Outdent");
        } else {
          ed.execCommand("Indent");
        }

        event.preventDefault();
        return false;
      }
    });
  },
});
