// Global variables
var drawing_id = -1;
var other_drawings = [];

function DataURIToBlob(dataURI) {
  const splitDataURI = dataURI.split(',')
  const byteString = splitDataURI[0].indexOf('base64') >= 0 ? atob(splitDataURI[1]) : decodeURI(splitDataURI[1])
  const mimeString = splitDataURI[0].split(':')[1].split(';')[0]
  const ia = new Uint8Array(byteString.length)
  for(let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i)
  }
  return new Blob([ia], {
    type: mimeString
  });
}

function readURL(input) {
  if(input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('.image-upload-wrap').hide();
      $('#instructions').hide();
      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();
      $("#loader").css('visibility', 'visible');
      $('.image-title').html("Image"); // input.files[0].name
      var data = new FormData();
      const img_data = DataURIToBlob(e.target.result)
      data.append('drawing', img_data);

      jQuery.ajax({
        url: '/upload',
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type: 'POST', // For jQuery < 1.9
        success: function(data) {
          // Set the Drawing
          data = JSON.parse(data);

          if(data['error'] !== ''){
            console.error(data['error'])
            if(data['error'] == 'No contours'){
              // alert("Photo is niet goed. Probeer op nieuw alsjeblieft.");
              alert("Error:" + data['error']);
              history.go(0);
            }
          }

          $("#loader").css('visibility', 'hidden');

          $("#rocket").attr('src', data['drawing']);
          drawing_id = data['drawing_id'];
          other_drawings = data['other_drawings'];
          astronaut = data['astronaut'];
          
          window.setSceneData(drawing_id, other_drawings, astronaut);
        }
      });
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function() {
  $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function() {
  $('.image-upload-wrap').removeClass('image-dropping');
});