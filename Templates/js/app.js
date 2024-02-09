function toggleTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("nav-link");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

$( document ).ready(function() {
    console.log("App Running");
});

function loadFile(event){
    console.log("Input Image Selected");
    document.getElementById('inputImageCard').style.display = "flex";
    var output = document.getElementById('inputImage');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
}

function fetchData(tableName, fieldId) {
    let url = '/fetchData/' + tableName
    fetch(url)
    .then((response) => {
        console.log(response.status);
        return response.json();
    })
    .then(function(data) {
        console.log(data.results);
        let dropdown = $(fieldId);
        dropdown.empty();
        for (var i = 0; i < data.results.length; i++) {
            dropdown.append($('<option></option>').attr('value', data.results[i].id).text( data.results[i].field_name));
        }
    });
}