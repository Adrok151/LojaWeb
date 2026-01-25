function abrirPopup() {
  document.getElementById("meuPopup").style.display = "block";
};

function fecharPopup() {
  document.getElementById("meuPopup").style.display = "none";
};

window.onclick = function(event) {
  var popup = document.getElementById("meuPopup");
  if (event.target == popup) {
    popup.style.display = "none";
  }
};