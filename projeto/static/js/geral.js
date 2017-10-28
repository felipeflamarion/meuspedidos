$(document).ready(function () {
    // Ativar elementos dropdown
    $('.ui.dropdown').dropdown();
    // Fechar elementos "message"
    $('.message .close').on('click', function() {$(this).closest('.message').transition('fade');});
});