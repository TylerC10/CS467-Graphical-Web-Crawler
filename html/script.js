$(document).ready(function(){


  $("#submitButton").click(function(e){
      e.preventDefault();
      var searchString = "";
      var selected = $("input[type='radio'][name='searchType']:checked");
      var starting = "";
      var startingValue = $("input[type='text'][name='startingURL']");
      var stopWords = "";
      var stopValue = $("input[type='text'][name='search']");
      var userId = getUserCookie();
      starting = startingValue.val();
      searchString = selected.val();
      stopWords = stopValue.val();
        $.ajax({type: "POST",
            url: "/cgi-bin/web-crawler/crawlcgi.py",
            data: { search_type: searchString, start_url: starting, stop_words: stopWords, user_id: userId},
            dataType:"text",
            success:function(data){
	      $("#crawlstatus").html(data);
            },
           error:function(result)
            {
             console.log(result);
           }
       });
    });
});
