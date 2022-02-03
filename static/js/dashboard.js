var greeting = document.getElementsByTagName("h1")[0];

function updateTime() {
    hour = new Date().getHours();

    var text = null;

    if (hour < 11)
        text = "Morning";

    else if (hour > 17)
        text = "Evening";

    greeting.innerHTML.replace("Afternoon", text);
}

updateTime();
setInterval(updateTime, 1000 * 60);