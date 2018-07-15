$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
   
    
     
  
    $(".js-video-button").modalVideo({
        channel: 'youtube',
        youtube: {
          autoplay: 1,
          cc_load_policy: 0,
          color: null,
          controls: 1,
          disablekb: 0,
          enablejsapi: 0,
          end: null,
          fs: 1,
          h1: null,
          iv_load_policy: 1,
          list: "PL_R95CAufNZ_YOg6czP415_1YLn2J5HQo",
          listType: "playlist",
          loop: 0,
          modestbranding: null,
          origin: null,
          playlist: null,
          playsinline: null,
          rel: 0,
          showinfo: 1,
          start: 0,
          wmode: 'transparent',
          theme: 'dark'
        },
        ratio: '16:9',
      });


  });