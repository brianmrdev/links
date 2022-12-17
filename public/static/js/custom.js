$(function () {
    $("#form-login").submit(function () {
        var usuario = $("#username").val();
        var clave = $("#password").val();
        var dataString = $('#form-login').serialize();

        document.querySelector('#btnLogin').innerHTML = '<i class="fas fa-spinner fa-pulse" style="padding: 0; margin-right: 10px;"></i> Comprobando...';

        if (usuario == '' || clave == '') {
            var Toast = Swal.mixin({
                toast: true,
                orientation: 'auto',
                showConfirmButton: false,
                timer: 3000
            });
            document.querySelector('#btnLogin').innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
            Toast.fire({
                icon: 'info',
                title: 'Debe especificar un usuario y una contraseña'
            });
        }
        else {
            $.ajax
                ({
                    type: "POST",
                    url: "/accounts/login/",
                    data: dataString,
                    success: function (msg) {
                        if (msg == 1) {
                            window.location = "";
                        }
                        if (msg == 2) {
                            var Toast = Swal.mixin({
                                toast: true,
                                orientation: 'auto',
                                showConfirmButton: false,
                                timer: 3000
                            });
                            document.querySelector('#btnLogin').innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
                            Toast.fire({
                                icon: 'error',
                                title: 'usuario y/o contraseña incorrecta.'
                            });
                        }
                        if (msg == 3) {
                            var Toast = Swal.mixin({
                                toast: true,
                                orientation: 'auto',
                                showConfirmButton: false,
                                timer: 3000
                            });
                            document.querySelector('#btnLogin').innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
                            Toast.fire({
                                icon: 'error',
                                title: 'Formulario no valido'
                            });
                        }
                    }
                });
        }
        return false;
    });
});