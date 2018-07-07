/*
 * jQuery File Upload Plugin JS Example 8.9.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/* global $, window */

/*
THIS FILE WAS CHANGED BY LEO

Upload-url here, needs to point to "file-panel/upload for now"
*/



$(function () {
    

      'use strict';
      // Change this to the location of your server-side upload handler:
     
      //var url = 'file-panel/upload';
      var url = 'server/php';
      
      
      $('#fileupload').fileupload({
            url: 'file-panel/upload',
          dataType: 'json',
          done: function (e, data) {
              alert("ok");
              $.each(data.result.files, function (index, file) {
                  $('<p/>').text(file.name).appendTo('#files');
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


/* 
$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: 'file-panel/upload'
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );


});
 */