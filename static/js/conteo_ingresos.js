function updateCounts() {
    // Hacer una petición AJAX a la vista que devuelve el conteo de ingresos en cada estado
    $.ajax({
      url: '{% url "ingresos_counts" %}',
      method: 'GET',
      success: function(data) {
        // Actualizar el texto de los elementos HTML correspondientes
        $('#no_reparados_card .card-text').text(data.no_reparados_count);
        $('#en_reparacion_card .card-text').text(data.en_reparacion_count);
        $('#reparados_card .card-text').text(data.reparados_count);
      },
      error: function() {
        console.log('Error al obtener el conteo de ingresos');
      }
    });
  }

  // Actualizar el conteo cada 10 segundos
  setInterval(updateCounts, 10000);

  // Actualizar el conteo al cargar la página
  updateCounts();

  

