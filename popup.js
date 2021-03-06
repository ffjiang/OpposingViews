/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    console.assert(typeof url == 'string', 'tab.url should be a string');
    callback(url);
  });
}

function visitURL(link) {
  chrome.tabs.create({ "url": link });
}

function getOpposingViewURLs(url) {
  var encoded_current_uri = encodeURI(url);
  var xhttp = new XMLHttpRequest();
  xhttp.open('GET', 'http://ec2-35-160-7-63.us-west-2.compute.amazonaws.com:8080/?article=' 
    + encoded_current_uri, true);
  xhttp.onreadystatechange = function() {
    var resp = JSON.parse(xhttp.responseText);
    news_snippets = '';
    for (i = 0; i < resp.length; i++) {
      news_snippets += '<div class="media"><div class="media-left"><img class="media-object" src="' + resp[i].topImage + '" style="width: 64px; height: 64px;"></div>'
        + '<div class="media-body"><a href="#" onclick="visitURL(&quot;' + resp[i].url + '&quot;)"><h4 class="media-heading">'
        + resp[i].title
        + '</h4></a><h4 class="source">' + resp[i].source + '</h4>'
        + '<p>' + resp[i].content
        + '</div></div>';
    }
    document.getElementById("news-content").innerHTML = news_snippets;
  }
  xhttp.send();
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
    getOpposingViewURLs(url);
  });
});