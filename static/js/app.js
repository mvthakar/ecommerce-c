function triggerImage1Select()
{
    document.getElementById("image1").click();
}

function triggerImage2Select()
{
    document.getElementById("image2").click();
}

function image1Selected(event)
{
    let output = document.getElementById('image1-preview');

    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src);
    }
}

function image2Selected(event)
{
    let output = document.getElementById('image2-preview');
        
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src);
    }
}

function clearImage1()
{
    let output = document.getElementById('image1-preview');
    output.src = "/static/images/border.png";

    document.getElementById("image1").value = '';
}

function clearImage2()
{
    let output = document.getElementById('image2-preview');
    output.src = "/static/images/border.png";

    document.getElementById("image2").value = '';
}