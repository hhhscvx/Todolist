document.addEventListener("DOMContentLoaded", (event) => {
  let daily = document.getElementById("daily");
  let weekly = document.getElementById("weekly");

  document.body.addEventListener("click", (event) => {
    if (event.target === daily || event.target === weekly) {
      let currentDate = new Date();

      let currYear = currentDate.getFullYear();
      let currMonth = currentDate.getMonth(); // Месяцы в JavaScript начинаются с 0
      let currDay = currentDate.getDate();

      currentDate = new Date(currYear, currMonth, currDay);

      // Получаем дату через неделю
      let oneWeekLater = new Date();
      if (event.target === weekly) {
        oneWeekLater.setDate(currentDate.getDate() + 7);
      }

      let notes = document.querySelectorAll(".note");
      const months = {
        января: "01",
        февраля: "02",
        марта: "03",
        апреля: "04",
        мая: "05",
        июня: "06",
        июля: "07",
        августа: "08",
        сентября: "09",
        октября: "10",
        ноября: "11",
        декабря: "12",
      };
      Array.from(notes).forEach(function (note) {
        let datetodoStr =
          note.firstElementChild.nextElementSibling.dataset.noteDatetodo.split(
            " "
          );
        let year = datetodoStr[2];
        let month = months[datetodoStr[1]];
        let day = datetodoStr[0];
        let datetodo = new Date(
          `${year}-${month >= 10 ? month : "0" + month}-${
            day >= 10 ? day : "0" + day
          }`
        );
        console.log(`datetodo: ${datetodo}, currentDate: ${currentDate}`);
        if (datetodo < currentDate || datetodo > oneWeekLater) {
          note.style.display = "none";
        } else {
          note.style.display = "block";
        }
      });
    }
  });
});
