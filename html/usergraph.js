$(document).ready(function(){
  // Get user cookie and updat field with value
   var userId = getUserCookie();
   // Set the userId in the UI if id=userid
   $("#userid").html(userId);
   var searchCode = location.search.split('id=')[1];
   // Perform GET for user's crawls
   $.ajax({type: "GET",
            url: "/cgi-bin/web-crawler/usergraphs.py",
            data: { user_id: userId,search_code: searchCode},
            dataType:"text",// json value is useless due to CGI bin mangling double quotes for single quotes with Python print()
            success:function(data){
		console.log(data);
		//This funky/additional parsing necessary Python end point with print() mangles " to ' , dataType:json in AJAX doesn't help
		json = JSON.parse(data.replace(/'/g, '"'));
		//console.log(json);
		// NOTE: data has 'd3' data strcuture for graph
		//       and also high-level crawl fields ('search_code','crawled_data_time',etc) in case these need to be displayed also.
 		// Create D3 tree graph with data.d3 response
		// NOTE: vertical or horizontal tree displays available 
                //       display quality varies depending on tree structure
		//vertical_tree(json['d3'][0],'d3graph');
		horizontal_tree(json['d3'][0],'d3graph');
           },
           error:function (xhr, ajaxOptions, thrownError) {
               console.log(xhr.status);
               console.log(thrownError);
           }
       });

    
});
