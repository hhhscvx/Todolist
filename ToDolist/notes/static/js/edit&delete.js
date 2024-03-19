document.addEventListener("DOMContentLoaded", (event) => {
  let edit = document.querySelectorAll(".fa-pen-to-square"); // также реализовать подсвечивание при наведении и cursor: pointer
  let del = document.querySelectorAll(".fa-trash-can");
  let listItems = document.querySelectorAll(".ul-notes li");
  

  Array.from(del).forEach((el) => {
    el.addEventListener("click", (event) => {
      let noteId = el.dataset.noteId;
      let note = document.querySelector(`[data-note-id="${noteId}"]`);
      fetch(`delete/${noteId}`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => {
          if (response.ok) {
            console.log("Заметка успешно удалена");
            console.log(`note: ${note}`);
            note.closest('li').hidden = true;
          } else {
            console.log("Произошла ошибка, заметка не удалена");
          }
        })
        .catch((error) => {
          console.error("Error deleting note:", error);
        });
    });
  });

  Array.from(edit).forEach((el) => {
    el.addEventListener("click", (event) => {
      console.log(el.dataset.noteId);
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

});
