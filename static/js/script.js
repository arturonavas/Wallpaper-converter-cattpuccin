var canvas = document.getElementById('image-canvas');
var ctx = canvas.getContext('2d');
var ogimage;

// Handle image upload
document.getElementById('image-loader').addEventListener('change', function(e) {
    handleImage(e.target.files[0]);
});

function handleImage(file) {
    var reader = new FileReader();

    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            ogimage = canvas.toDataURL();
        }
        img.src = event.target.result;
    }

    reader.readAsDataURL(file);
    document.getElementById('download-button').style.display = 'none';
}

// Function to convert image
function convertImage() {
    var fileInput = document.getElementById('image-loader');
    var formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('theme', 'Rosewater'); // Choose your theme here

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        var img = new Image();
        img.onload = function() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            document.getElementById('download-button').style.display = 'inline';
        }
        img.src = URL.createObjectURL(blob);
    });
}

// Download the converted image
function downloadImage() {
    var link = document.createElement('a');
    link.download = 'converted-image.png';
    link.href = canvas.toDataURL();
    link.click();
}
