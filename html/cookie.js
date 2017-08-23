  // Set cookie 
  function setUserCookie() {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));// Set cookie with 1 year expiration
    var expires = "expires="+d.toUTCString();
    randomId = Math.random().toString().slice(2,11); // Up to 9 digits
    document.cookie = "userid=" + randomId + ";" + expires + ";path=/";
    return randomId;
  }

  // Get cookie
  function getUserCookie() {
    var name = "userid=";
    var decodedCookie = decodeURIComponent(document.cookie);
    // Cookies are lumped together by domain so need to search for given name
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        } else { 
	    // No user cookie set it up 
	    return setUserCookie();
        }
    }
}
