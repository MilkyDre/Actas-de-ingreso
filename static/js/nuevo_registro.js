  $(function() {
    // Manejar el evento de clic en el botón "agregar ingreso"
    $('#agregar-ingreso-btn').click(function(event) {
      event.preventDefault();
      // Mostrar la ventana emergente con el formulario
      $('#agregar-ingreso-form').show();
    });

    // Manejar el evento de envío del formulario
    $('#ingreso-form').submit(function(event) {
      event.preventDefault();
      // Enviar el formulario a través de AJAX
      $.ajax({
        url: '/agregar_ingreso/',
        method: 'POST',
        data: $(this).serialize(),
        success: function(response) {
          // Ocultar la ventana emergente y volver a la plantilla anterior con el resultado del registro
          $('#agregar-ingreso-form').hide();
          $('#contenido').html(response);
        },
        error: function(xhr, status, error) {
          // Manejar errores de AJAX aquí
        }
      });
    });
  });
