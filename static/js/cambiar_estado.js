$('.cambiar-estado').click(function(e) {
    e.preventDefault();
  
    var $button = $(this);
    var ingresoId = $button.data('id_ingreso');
    var nuevoEstado = $button.data('estado');
  
    $.ajax({
      url: '/cambiar_estado/' + ingresoId + '/' + nuevoEstado + '/',
      type: 'POST',
      success: function(response) {
        // Actualizar el conteo de ingresos
        $.get('/ingresos_counts/', function(data) {
          $('#en-espera-count').text(data.en_esp_count);
          $('#en-reparacion-count').text(data.en_reparacion_count);
          $('#reparados-count').text(data.reparados_count);
        });
      }
    });
  });