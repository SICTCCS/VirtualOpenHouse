let delimiter = "/ClassroomView/";
    let place = window.location.href;
    let room = place.substring(place.indexOf(delimiter) + delimiter.length);
    room = room.slice(0, room.indexOf("/"));
        document.getElementById("mtt").href = "../../MeetTheTeacher/Teachers/"+room+"/index.html";
        document.getElementById("lm").href = "../../ClassCard/"+room+"/index.html";