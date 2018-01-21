function analyze() {
  var url = "";
  var score = getScore(url);
  var outputStringTemp = "The Objectivity Score Of This Webpage is " + score; 
  document.getElementById('outputString').innerHTML = outputStringTemp;
  //display(score);
}

function getScore(url) {
  return 1;
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

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('button').addEventListener('click', clickHandler);
  main();
});