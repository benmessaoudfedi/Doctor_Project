        $(document).ready( function() {

          $('#use_zoom').change(function() {
                if ($('#use_zoom').is(':checked')) {

                    wheelzoom(document.querySelector("#img_upload"), {zoom: 0.1, maxZoom: 10});
                }else{
                    document.querySelector('#img_upload').dispatchEvent(new CustomEvent('wheelzoom.destroy'));
                }});


    });
