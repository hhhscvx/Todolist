document.addEventListener("DOMContentLoaded", (event) => {
  let notes = document.querySelector(".notes");
  notes.style.left =
    document.body.offsetWidth / 2 - notes.offsetWidth / 2 + "px";

  let ul = document.querySelector(".ul-notes");
  let listItems = Array.from(document.querySelectorAll(".ul-notes li"));
  let checkboxes = document.querySelectorAll("[data-note-id]");
  Array.from(checkboxes).forEach((cbox) => {
    if (cbox.checked) ul.append(cbox.closest("li"));
  });

  document.body.addEventListener("mousedown", (event) => {
    let target = event.target;
    console.log(target);
  });

  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function (event) {
      let noteId = checkbox.dataset.noteId;
      let status = checkbox.checked ? "Completed" : "ToDo";
      fetch(`/notes/status/${noteId}/${status}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"), // добавляем CSRF-токен
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // пустое тело запроса, так как данные передаются в URL
      })
        .then((response) => {
          if (response.ok) {
            console.log("Статус заметки успешно изменен");
          } else {
            console.error("Ошибка при изменении статуса заметки");
          }
        })
        .catch((error) => {
          console.error("Произошла ошибка:", error);
        });
      let noteTitle = event.currentTarget.nextElementSibling.lastElementChild;
      noteTitle.classList.toggle("complete");
    });
  });

  // Функция для получения CSRF-токена из куки
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

  for (let checkbox of checkboxes) {
    checkbox.addEventListener("click", (event) => {
      let target = event.target;
      let checkboxesChecked = 0;
      Array.from(checkboxes).forEach((cbox) => {
        if (cbox.checked) checkboxesChecked++;
      });

      let li = target.closest("li");
      if (!li) {
        alert("li не найдено, break");
      }

      let curr_li_position = listItems.indexOf(li);
      console.log(`curr_li_position: ${curr_li_position}`);
      if (checkbox.checked) {
        ul.append(li);
      } else {
        if (curr_li_position == 0) {
          ul.prepend(li);
        } else {
          console.log(`checkboxesChecked: ${checkboxesChecked}`);
          console.log(`curr_li_postition: ${curr_li_position}`);
          listItems[curr_li_position - 1].insertAdjacentElement("afterend", li);
          Array.from(checkboxes).forEach((cbox) => {
            if (cbox.checked) ul.append(cbox.closest("li"));
          });
        }
      }
    });
  }
});
