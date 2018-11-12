$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    
    console.log("I was fired once...");
    var url = 'http://'+window.location.host + '{{ upload_url }}';
    var formData;
    console.log(url);
  
    $('.upload_button').prop('disabled', true);

    $('.upload_button').click( function() {$('#ModalEmail').modal() });


    $('#fileupload1').bind('fileuploadaddfileerror', function (e, data){
        console.log('Custom Error Event Fired');
    });


    $('#fileupload1').fileupload({  
        
        url: url,
        dataType: 'json',
        autoUpload: false,

        add: function (e, data) {       
               

          $.each(data.files, function (index, file) {

              console.log('Selected file: ' + file.name);
              $('.upload_button').prop('disabled', false);
              
                       

              //data.context = $('.upload_button')
              data.context = $('#modal_submit_button')
                .click(function () {
                    
                    var upload_creator_mail = $("#input_upload_email").val();
                    $("#form_creator_email").val(upload_creator_mail);

                    console.log("Usermail: "+ $("#form_creator_email").val());

                    $('#ModalEmail').modal('hide');
                    $('.upload_button').text('Uploading...');
                    
                    data.formData = $('form').serializeArray(); 
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
            //alert('Dankeschön ✔')
        },

        // This will trigger an ALERT with a Server Message
        fail: function(e, data){
            $('.upload_button').text("Upload");
            $('.filename_text').toggleClass('bg-info bg-danger');
            $('.filename_text').prepend("✘");
            alert('Fehler. Servermeldung: '+ data.jqXHR.responseJSON.msg);
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




  