var xxx = document.getElementById('text1');
var qu = document.getElementById('q');
var jsMessage = document.getElementById('js-message')
var noRes = document.getElementById('no-res')
var temEr = document.getElementById('template-errors')

var cheBox = document.getElementById('checkbox1');
function formValid() {
	var err = false;
	if ( noRes ) {
		noRes.style.display = "none";
	};
	if ( temEr ) {
		temEr.style.display = "none";
	};
	jsMessage.innerHTML = "";
	if ( q.value.includes(' ') ) {
		jsMessage.innerHTML += "No spaces allowed (one-word check only)<br/>";
			err = true;
	}
	if ( xxx.required == true) {
		if ( xxx.value.length != qu.value.length) {
			jsMessage.innerHTML += "Word and mask should be of equal length<br/>";
			err = true;
		}
	}
	if ( err == true ) {
		return false;
	}
}

function checkBox() {
	if ( cheBox.checked ) {
		xxx.disabled = false;
		xxx.required = true;
	} else {
		xxx.disabled = true;
		xxx.required = false;
	}
}

function onLoad() {
	if ( cheBox.checked ) {
		xxx.disabled = false;
		xxx.required = true;
	} else {
		xxx.disabled = true;
		xxx.requires = false;
	}
}
document.onload = onLoad();
