/*
	Author: Brock Erwin
	Description:  Scripts to set email notification preferences for MyEMSL uploads
 */
function checkBoxClicked() {
	var proposalData = new Object;
	proposalData[this.id] = this.checked;
	$.post('../notification', proposalData);
}
function enableAll() {
	setAllBoxes(true);
}
function disableAll() {
	setAllBoxes(false);
}
function setAllBoxes(value) {
	var proposals = document.getElementsByName("checkBoxProposal");
	for(var i = 0; i < proposals.length; i++)
		if(proposals[i].checked != value)
			proposals[i].click();
}
var callback = {
	on_success: function (r) {
		var proposals = document.getElementsByName("checkBoxProposal");
		for(var i = 0; i < proposals.length; i++)
			proposals[i].onclick = checkBoxClicked;
		/* Set onclick properties for buttons */
		document.getElementById("pref-enable-all").onclick = enableAll;
		document.getElementById("pref-disable-all").onclick = disableAll;
	}
}

$(document).ready(function() {
	// Show the main area
	maindiv = document.getElementById("Main");
	maindiv.style.display = "block";
	// Hide the no-javascript error message
	nojavascript = document.getElementById("error-NoJavascript");
	nojavascript.style.display = "none";

	// Process the template with our callback
	$("#Items").setTemplateElement("Template-Items").processTemplateURL("../notification", null, callback);
});
