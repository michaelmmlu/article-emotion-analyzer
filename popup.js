function analyze() {
  var url = "";
  var score = getScore(url);
  var outputStringTemp = "The Objectivity Score Of This Webpage is " + score; 
  document.getElementById('outputString').innerHTML = outputStringTemp;
  //display(score);
}

function getScore(url) {
  return doQuery();
}

/**
 * test method to output score as a popup box.
 * @param score 
 */
function display(score) {
  alert("" + score);
}

function main() {
  // init stuff
}

function clickHandler(e) {
  analyze()
  //setTimeout(analyze, 10);
}

function doQuery() {
  $(function() {
    $('button').click(function() {
        $.ajax({
            url: 'http://secret-heaven-192806.appspot.com/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                return response;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('button').addEventListener('click', clickHandler);
  main();
});