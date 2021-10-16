function information(){
    var num = document.forms["form-information"]["num"].value;
    var text = document.getElementById("inputText").value;

    if (num == 1)
        alert(text)
    else if (num == 2)
        alert('Hello!')
    
    else if (num == 3)
        alert('안녕!')
    
    }