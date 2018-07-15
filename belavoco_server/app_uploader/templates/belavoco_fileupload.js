$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    
    console.log("I was fired once...");
    var url = 'http://'+window.location.host + '{{ upload_url }}';
    var formData;
    console.log(url);
  

    $('#fileupload1').fileupload({  
        
        url: url,
        dataType: 'json',
        change: function (e, data) {
          $.each(data.files, function (index, file) {
              //alert('Selected file: ' + file.name);
              data.formData = $('form').serializeArray();
          })
        },  
        drop: function (e, data) {
            $.each(data.files, function (index, file) {
                console.log('Dropped file: ' + file.name);
                data.formData = $('form').serializeArray();
            });
        },      
        done: function (e, data) {
          //console.log("Upload finished!"); 
          //console.log($('form').serializeArray())
  
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#files');
                alert(file.name + ' erfolgreich hochgeladen!');
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
  });