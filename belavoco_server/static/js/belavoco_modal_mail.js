


function modal_upload_button_click(){

    $('#ModalEmail').modal('hide');
//TODO: add actual Upload Capability
    alert ( $("#input_upload_email").val() );
    //#creator_email
}

/* 
$( "#input_upload_email" ).change(function(){

   

    $.get( AJAX_USERMAIL_URL, function( data ) {
        console.log(data.exists);
      });

}); */

//TODO: Validation which tries to find Email in Database...

$('#input_upload_email').validator({
    custom: {
        emailexist: function ($el) {
            var result = checkUserEmail($el.val())
                .done(function (r) {
                    if (!r.success) {
                        // email already in use
                        return r;
                    } 
                })
            return result.responseText;
        }
    }
});



function checkUserEmail(mail) {
    
    console.log("checking...");

    var r = false;
    var AJAX_USERMAIL_URL = 'https://bvtest.free.beeceptor.com/' + mail;

    $.ajax({
        url:AJAX_USERMAIL_URL,
        //data: { ChapterPOCEmail: name },
        //type: 'POST',
        dataType: 'json',
        async: false // wait for the call, dont treat as an async call
    }).done(function(result) {
        r = result === "OK";
        console.log(result)
    }).fail(function (err) {
        console.log(err, "something went awire");
    }).always(function () {
        console.log("all done");
    });

    return r;
}



//

$( "input[type='checkbox']" ).change(function(){
    // Anonymer Upload wird de-/aktiviert


    if (this.checked){
        $("#input_upload_email").attr('disabled', 'disabled');
    }
    else {
        $("#input_upload_email").removeAttr('disabled');
    }

});



