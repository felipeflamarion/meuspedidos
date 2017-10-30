$(document).ready(function () {

    input_quantidade = $('input[id="id_quantidade"]');
    mensagem = $('.error.quantidade.message');
    multiplo_de_venda = parseInt($('#multiplo_de_venda').val());

    input_quantidade.change(function () {
        controle_multiplo();
    });

    input_quantidade.keyup(function () {
        controle_multiplo();
    });

    $('.item.form').submit(function () {
        if (!controle_multiplo()) {
            mensagem.removeClass("hidden");
            return false;
        }
    });

    function controle_multiplo() {
        quantidade = parseInt(input_quantidade.val());
        if (quantidade % multiplo_de_venda == 0) {
            $('.quantidade.field').removeClass("error");
            return true;
        }
        else {
            $('.quantidade.field').addClass("error");
            return false;
        }
    }
});