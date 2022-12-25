$(document).ready(function () {
  $("#addLinkForm")
    .bootstrapValidator({
      message: "Este valor no es valido",
      feedbackIcons: {
        valid: "fa-solid fa-check",
        invalid: "fa-solid fa-times",
        validating: "fas fa-spinner fa-pulse",
      },
      submitHandler: function (validator, form, submitButton) {
        document.querySelector("#btnFetch").innerHTML =
          '<i class="fas fa-spinner fa-pulse" style="padding: 0; margin-right: 10px;"></i> Guardando...';
        $.post(
          form.attr("action"),
          form.serialize(),
          function (result) {
            if (result.status == false || result.status == "false") {
              var Toast = Swal.mixin({
                toast: true,
                orientation: "auto",
                showConfirmButton: false,
                timer: 4000,
              });
              document.querySelector("#btnFetch").innerHTML =
                '<i class="fa-solid fa-check"></i> Guardar';
              Toast.fire({
                icon: "error",
                title: result.msg,
              });
            } else if (result.status == true || result.status == "true") {
              $("#addLink").modal("toggle");
              $("form input[type=text]").each(function () {
                this.value = "";
              });
              var Toast = Swal.mixin({
                toast: true,
                orientation: "auto",
                showConfirmButton: false,
                timer: 4000,
              });
              Toast.fire({
                icon: "success",
                title: result.msg,
              });
              window.setTimeout(function () {
                window.location = "";
              }, 2000);
              document.querySelector("#btnFetch").innerHTML =
                '<i class="fa-solid fa-check"></i> Guardar';
            } else {
              $("#addLinkForm").bootstrapValidator(
                "disableSubmitButtons",
                false
              );
            }
          },
          "json"
        )
          .done(function (msg) {})
          .fail(function (xhr, status, error) {
            document.querySelector("#btnFetch").innerHTML =
              '<i class="fa-solid fa-check"></i> Guardar';
            Swal.fire({
              icon: "error",
              title: error,
              showConfirmButton: false,
            });
          });
      },
      fields: {
        name: {
          validators: {
            notEmpty: {
              message: "Este campo no puede estar vacio",
            },
          },
        },
        url: {
          validators: {
            notEmpty: {
              message: "Este campo no puede estar vacio",
            },
            uri: {
              message: "URL no válida",
            },
          },
        },
      },
    })

    $("#editLinkForm")
    .bootstrapValidator({
      message: "Este valor no es valido",
      feedbackIcons: {
        valid: "fa-solid fa-check",
        invalid: "fa-solid fa-times",
        validating: "fas fa-spinner fa-pulse",
      },
      submitHandler: function (validator, form, submitButton) {
        document.querySelector("#btnFetchEditLink").innerHTML =
          '<i class="fas fa-spinner fa-pulse" style="padding: 0; margin-right: 10px;"></i> Guardando...';
        $.post(
          form.attr("action"),
          form.serialize(),
          function (result) {
            if (result.status == false || result.status == "false") {
              var Toast = Swal.mixin({
                toast: true,
                orientation: "auto",
                showConfirmButton: false,
                timer: 4000,
              });
              document.querySelector("#btnFetchEditLink").innerHTML =
                '<i class="fa-solid fa-check"></i> Guardar';
              Toast.fire({
                icon: "error",
                title: result.msg,
              });
            } else if (result.status == true || result.status == "true") {
              var Toast = Swal.mixin({
                toast: true,
                orientation: "auto",
                showConfirmButton: false,
                timer: 4000,
              });
              Toast.fire({
                icon: "success",
                title: result.msg,
              });
              window.setTimeout(function () {
                window.location = "/";
              }, 2000);
              document.querySelector("#btnFetchEditLink").innerHTML =
                '<i class="fa-solid fa-check"></i> Guardar';
            } else {
              $("#editLinkForm").bootstrapValidator(
                "disableSubmitButtons",
                false
              );
            }
          },
          "json"
        )
          .done(function (msg) {})
          .fail(function (xhr, status, error) {
            document.querySelector("#btnFetchEditLink").innerHTML =
              '<i class="fa-solid fa-check"></i> Guardar';
            Swal.fire({
              icon: "error",
              title: error,
              showConfirmButton: false,
            });
          });
      },
      fields: {
        name: {
          validators: {
            notEmpty: {
              message: "Este campo no puede estar vacio",
            },
          },
        },
        url: {
          validators: {
            notEmpty: {
              message: "Este campo no puede estar vacio",
            },
            uri: {
              message: "URL no válida",
            },
          },
        },
      },
    })


    .on("success.field.fv", function (e, data) {
      if (data.fv.getInvalidFields().length > 0) {
        // There is invalid field
        data.fv.disableSubmitButtons(true);
      }
    });
});

$(function () {
  $("#form-login").submit(function () {
    var usuario = $("#username").val();
    var clave = $("#password").val();
    var dataString = $("#form-login").serialize();

    document.querySelector("#btnLogin").innerHTML =
      '<i class="fas fa-spinner fa-pulse" style="padding: 0; margin-right: 10px;"></i> Comprobando...';

    if (usuario == "" || clave == "") {
      var Toast = Swal.mixin({
        toast: true,
        orientation: "auto",
        showConfirmButton: false,
        timer: 3000,
      });
      document.querySelector("#btnLogin").innerHTML =
        '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
      Toast.fire({
        icon: "info",
        title: "Debe especificar un usuario y una contraseña",
      });
    } else {
      $.ajax({
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
              orientation: "auto",
              showConfirmButton: false,
              timer: 3000,
            });
            document.querySelector("#btnLogin").innerHTML =
              '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
            Toast.fire({
              icon: "error",
              title: "usuario y/o contraseña incorrecta.",
            });
          }
          if (msg == 3) {
            var Toast = Swal.mixin({
              toast: true,
              orientation: "auto",
              showConfirmButton: false,
              timer: 3000,
            });
            document.querySelector("#btnLogin").innerHTML =
              '<i class="fa-solid fa-right-to-bracket"></i> Entrar';
            Toast.fire({
              icon: "error",
              title: "Formulario no valido",
            });
          }
        },
      });
    }
    return false;
  });
});

function delete_link(i) {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta acción es irreversible",
    icon: "warning",
    showCancelButton: true,
    cancelButtonText: "No, cancelar",
    confirmButtonText: "Si, eliminar",
    reverseButtons: true,
    confirmButtonColor: "darkred",
  }).then(function (result) {
    if (result.isConfirmed) {
      var dataString = "id=" + i;
      $('#spinner').html(`
      <div class="preloader">
      <div class="loader">
        <div class="spinner">
          <div class="spinner-container">
            <div class="spinner-rotator">
              <div class="spinner-left">
                <div class="spinner-circle"></div>
              </div>
              <div class="spinner-right">
                <div class="spinner-circle"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      `);
      $.ajax({
        type: "POST",
        url: "/link/delete/",
        data: dataString,
        dataType: "json",
        success: function (result) {
          if (result.status == true || result.status == "true") {
            $('#spinner').empty()
            var Toast = Swal.mixin({
              toast: true,
              orientation: "auto",
              showConfirmButton: false,
              timer: 4000,
            });
            Toast.fire({
              icon: "success",
              title: result.msg,
            });
            window.setTimeout(function () {
              window.location = "";
            }, 2000);
          }
          if (result.status == false || result.status == "false") {
            $('#spinner').empty()
            Swal.fire({
              icon: "error",
              title: result.msg,
              showConfirmButton: false,
            });
          }
        },
        error: function (jqXHR, status, error) {
          $('#spinner').empty()
          Swal.fire({
            icon: "error",
            title: error,
            showConfirmButton: false,
          });
        },
      });
    }
  });
}

const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput  = document.getElementById('search-input')
const resultBox  = document.getElementById('result-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (link) => {
  $.ajax({
    type: 'POST',
    url: '/link/search/',
    data: {
      'csrfmiddlewaretoken': csrf,
      'link': link,
    },
    success: (res)=> {      
      const data = res.data
      if (Array.isArray(data)) {
        resultBox.innerHTML = ""
        resultBox.classList.add('show')
        data.forEach(link=> {
          resultBox.innerHTML += `
          <li><a class="dropdown-item" href="/${link.slug}/" target="_blank">${link.name} <p class="text-muted">${link.description}</p></a></li>
          `
        })
      } else {
        if (searchInput.value.length > 0) {
          resultBox.classList.add('show')
          resultBox.innerHTML = `<b>${data}</b>`
        } else {
          resultBox.classList.remove('show')
        }
      }
    },
    error: (err)=> {
      console.log(err)
    }
  })
}

searchInput.addEventListener('keyup', e=>{
  sendSearchData(e.target.value)
})

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})