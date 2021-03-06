// Autor: @jqcaper
// Configuraciones Generales
var nombre_tabla1 = "#tabla_toppings"; // id
var nombre_boton_eliminar1 = $('.desactivar'); // Clase
var nombre_formulario_modal1 = "#frmDesactivarUsuario"; //id
var nombre_ventana_modal1 = "#myModal"; // id
// Fin de configuraciones


    $('document').ready(function() {
        
        
        $('.desactivar').on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#modal_codigoContacto').val(Pid);
            $('#modal_name').text(name);
        });
    
        $('.activar').on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#id_industria').val(Pid);
            $('#nombre_industria').text(name);
        });

        $('#frmDesactivarUsuario').submit(function(e) { // catch the form's submit event
                e.preventDefault();
                $.ajax({ // create an AJAX call...
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) { // on success..
                    if(response.status=="True"){
                        $(nombre_ventana_modal1).modal('hide');
                        alert("Se desactivo la industria!");
                        location.reload();
                        
                    }else{
                        alert("Hubo un error al desactivar!");
                        $(nombre_ventana_modal1).modal('hide');
                    };
                }
            });
            return false;
        });
        
        $('#frmActivarUsuario').submit(function(e) { // catch the form's submit event
                e.preventDefault();
                $.ajax({ // create an AJAX call...
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) { // on success..
                    if(response.status=="True"){
                        $(nombre_ventana_modal1).modal('hide');
                        alert("Se activo la industria!");
                        location.reload();
                        
                    }else{
                        alert("Hubo un error al activar!");
                        $(nombre_ventana_modal1).modal('hide');
                    };
                }
            });
            return false;
        });
    });