$(document).ready(function(){
   // Get user cookie and updat field with value
   var userId = getUserCookie();
   // Set the userId in the UI if id=userid
   $("#userid").html(userId);
   // Perform GET for user's crawls
   $.ajax({type: "GET",
            url: "/cgi-bin/web-crawler/usergraphs.py",
            data: { user_id: userId},
            dataType:"text",
            success:function(data){
	      data = eval(data);
              list = "<table class='table table-striped table-bordered text-center'><tr><th class='text-center'>Search code</th><th class='text-center'>Website</th><th class='text-center'>Time</th><th class='text-center'>Search type</th><th class='text-center'>Max level</th></tr>"
              for (var i = 0; i < data.length; i++) {
               list += "<tr><td><a href='/graph.html?id=" + data[i]['search_code'] + "'>" + data[i]['search_code'] + "</a></td><td>" + data[i]['start_url'] + "</td><td>" + data[i]['crawled_data_time'] + "</td><td>" + data[i]['search_type'] + "</td><td>" + data[i]['max_level'] + "</td></tr>";
               }
              list += "</table>";
	      $("#pastgraphs").html(list);
            },
           error:function(result)
            {
             console.log(result);
           }
       });

    
});
