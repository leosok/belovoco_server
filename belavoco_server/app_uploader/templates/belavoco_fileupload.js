$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    
    console.log("I was fired once...");
    var url = 'http://'+window.location.host + '{{ upload_url }}';
    var formData;
    console.log(url);
  
    $('.upload_button').prop('disabled', true);



    $('#fileupload1').fileupload({  
        
        url: url,
        dataType: 'json',
        autoUpload: false,

        add: function (e, data) {       
               

          $.each(data.files, function (index, file) {

              console.log('Selected file: ' + file.name);
              $('.upload_button').prop('disabled', false);
              
                       

              data.context = $('.upload_button')
                .click(function () {
                    data.formData = $('form').serializeArray(); 
                    console.log(data);

                    data.context.text('Uploading...');
                    data.submit();
                });
          })
        },  
        drop: function (e, data) {
            $.each(data.files, function (index, file) {
                console.log('Dropped file: ' + file.name);
                data.formData = $('form').serializeArray();
            });
        },      
        done: function (e, data) {

            $('.upload_button').text("Done!").prop("disabled",true);
            $('.filename_text').toggleClass('bg-info bg-success');
            $('.filename_text').prepend("✔ ");
          //console.log("Upload finished!"); 
          //console.log($('form').serializeArray())
            /*
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#files');
                alert(file.name + ' erfolgreich hochgeladen!');
            }); */
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    })
    .on('fileuploadadd', function (e, data) {
        data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<p/>')
                    .append($('<span class="filename_text bg-info" style="padding: 5px"/>').text(file.name));
            if (!index) {
                node
                    .append('<br>')
            }
            node.appendTo(data.context);
        });
    })    
    .prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
  });




  