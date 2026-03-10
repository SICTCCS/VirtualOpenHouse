let delimiter = "/Teachers/";
    let place = window.location.href;
    let room = place.substring(place.indexOf(delimiter) + delimiter.length);
    room = room.slice(0, room.indexOf("/"));
        document.getElementById("lm").href = "../../../ClassCard/"+room+"/index.html";
        document.getElementById("vc").href = "../../ClassroomView/"+room+"/index.html";