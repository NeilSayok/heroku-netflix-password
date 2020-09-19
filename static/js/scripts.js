function copyPassword(){
    var copyText = document.getElementById("pass");
    console.log(copyText.innerHTML);
    copyText.select();
    document.execCommand("copy");
    alert("Password Copied to clipboard. \nPassword: " + copyText.value);

}


document.getElementById("change_password_btn").onclick = function () {
    $("body").append('<div style="width: 100%;height: 100%;position: absolute;background: rgba(255,255,255,0.9);display: flex;'+
        '                    flex-direction: column;justify-content: center;align-items: center;">' +
        '    <div class="loader"></div> ' +
        '    <p style="color: black">Changing Password...</p>' +
        '</div>');
    console.log("change_password_Called");
    //location.href = "/change_password";
    location.href = "https://colab.research.google.com/drive/1GHrevM4gXymdzQq6zJP64kET-kEKiJ44?usp=sharing"

    };

