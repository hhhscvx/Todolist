document.addEventListener("DOMContentLoaded", (event) => {
  // variabes
  let edit = document.querySelectorAll(".fa-pen-to-square");
  let cancel = document.querySelector(".fa-rectangle-xmark");

  // mouseenter backgrounds
  cancel.addEventListener("mouseenter", (event) => {
    cancel.style.background = "#555555";
    cancel.addEventListener("mouseleave", (event) => {
      cancel.style.background = "";
    });
  });

  cancel.addEventListener("mousedown", (event) => {
    cancel.style.background = "#333333";
    cancel.addEventListener("mouseup", (event) => {
      cancel.style.background = "";
    });
  });

  Array.from(edit).forEach((el) => {
    el.addEventListener("mouseenter", (event) => {
      el.style.background = "#20c997"; // green
      el.addEventListener("mouseleave", (event) => {
        el.style.background = "";
      });
    });
  });

  // main func
  Array.from(edit).forEach((el) => {
    el.addEventListener("click", (event) => {
      showPrompt(
        el.dataset.noteTitle,
        el.dataset.noteDatetodo,
        el.dataset.noteDescription,
        // function on click to edit
        function (noteTitle, noteDatetodo, noteDescription) {
          console.log(
            `Вы ввели: ${noteTitle} и ${noteDatetodo} и ${noteDescription}`
          );
          console.log(`typeof noteTitle: ${typeof noteTitle}`);
          const data = {
            new_title: noteTitle,
            new_datetodo: noteDatetodo,
            new_description: noteDescription,
          };
          let currEl =
            el.previousElementSibling.lastElementChild.lastElementChild
              .firstElementChild;
          currEl.textContent = noteTitle;
          fetch(`edit/${el.dataset.noteId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken"), // добавляем CSRF токен
              "Content-Type": "application/json", // Тип содержимого (JSON)
            },
            body: JSON.stringify(data),
          })
            .then((response) => {
              if (response.ok) {
                console.log("Запрос успешно выполнен");
                currEl.nextElementSibling.firstElementChild.textContent = `Сделать до ${noteDatetodo}`;
              } else {
                alert("Введена некорректная дата, попробуйте еще раз");
              }
            })
            .catch((error) => {
              console.error("Ошибка при выполнении запроса:", error);
            });
        }
      );
    });
  });
  function showCover() {
    let coverDiv = document.createElement("div");
    coverDiv.id = "cover-div";

    // убираем возможность прокрутки страницы во время показа модального окна с формой
    document.body.style.overflowY = "hidden";

    document.body.append(coverDiv);
  }

  function hideCover() {
    document.getElementById("cover-div").remove();
    document.body.style.overflowY = "";
  }

  function showPrompt(title, datetodo, description, callback) {
    showCover();
    var form = document.getElementById("prompt-form");
    let container = document.getElementById("prompt-form-container");
    document.getElementById("prompt-title").innerHTML = "Изменить название:";
    document.getElementById("prompt-datetodo").innerHTML = "Изменить дату:";
    document.getElementById("prompt-description").innerHTML =
      "Изменить описание:";

    form.text.value = title;
    form.text2.value = datetodo;
    form.text3.value = description;

    function complete(value, value2, value3) {
      hideCover();
      container.style.display = "none";
      document.onkeydown = null;
      if (value != null) callback(value, value2, value3);
    }

    form.onsubmit = function (event) {
      event.preventDefault();
      let value = form.text.value;
      let value2 = form.text2.value;
      let value3 = form.text3.value;
      if (value == "") return false; // игнорируем отправку пустой формы

      complete(value, value2, value3);
      return false;
    };

    cancel.onclick = function () {
      complete(null);
    };

    document.onkeydown = function (e) {
      if (e.key == "Escape") {
        complete(null);
      }
    };

    let lastElem = form.elements[form.elements.length - 1];
    let firstElem = form.elements[0];

    lastElem.onkeydown = function (e) {
      if (e.key == "Tab" && !e.shiftKey) {
        firstElem.focus();
        return false;
      }
    };

    firstElem.onkeydown = function (e) {
      if (e.key == "Tab" && e.shiftKey) {
        lastElem.focus();
        return false;
      }
    };

    container.style.display = "block";
    form.elements.text.focus();
  }

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
