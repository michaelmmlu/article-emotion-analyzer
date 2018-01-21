var activeTabId;
var data;

chrome.tabs.query({active: true, currentWindow: true}, function(arrayOfTabs) {

     // since only one tab should be active and in the current window at once
     // the return variable should only have one entry
     var activeTab = arrayOfTabs[0];
     activeTabId = activeTab.url; // or do whatever you need
  });

$(function() {
  $('button').click(function() {
    var link = activeTabId;
    $.ajax({
        url: 'https://hackdavis2018-1516486944179.appspot.com/run_analysis',
        data: {form_url: link},
        type: 'POST',
        success: function(response) {
          data = JSON.parse(response);
          populate_fields(data);
        },
        error: function(error) {
          window.alert("Error");
        }
    });
  });
});

function populate_fields(stringlist) {
  var data = stringlist.split(',');

  list = document.getElementById('list');
  var entry = document.createElement('li');
  entry.appendChild(document.createTextNode("bias level: " + data[0]));
  list.appendChild(entry);
  entry = document.createElement('li');
  entry.appendChild(document.createTextNode("1. " + data[1] + ": " + data[2]));
  list.appendChild(entry);
  entry = document.createElement('li');
  entry.appendChild(document.createTextNode("2. " + data[3] + ": " + data[4]));
  list.appendChild(entry);
  entry = document.createElement('li');
  entry.appendChild(document.createTextNode("3. " + data[5] + ": " + data[6]));
  list.appendChild(entry);
  entry = document.createElement('li');
  entry.appendChild(document.createTextNode("4. " + data[7] + ": " + data[8]));
  list.appendChild(entry);
  entry = document.createElement('li');
  entry.appendChild(document.createTextNode("5. " + data[9] + ": " + data[10]));
  list.appendChild(entry);
}
