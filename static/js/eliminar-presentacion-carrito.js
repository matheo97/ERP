// Autor: @jqcaper
// Configuraciones Generales
var nombre_tabla1 = "#tabla_toppings"; // id
var nombre_boton_eliminar1 = $('.desactivar'); // Clase
var nombre_formulario_modal1 = "#frmDesactivarUsuario"; //id
var nombre_ventana_modal1 = "#myModal"; // id
// Fin de configuraciones


    $('document').ready(function() {
        
        //Eliminar Elementos de la lista del carrito
        $('.desactivar').on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#modal_codigoContacto').val(Pid);
            $('#modal_name').text(name);
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
                        location.reload();
                        document.getElementById('data-table').deleteRow(Number(response.row))
                        location.reload();
                        location.href=location.href;
                        window.location.reload(true);
                        window.location.href=window.location.href;
                        
                    }else{
                        alert("Hubo un error al eliminar!");
                        $(nombre_ventana_modal1).modal('hide');
                    };
                }
            });
            return false;
        });
        
        
        //Recalculo de los valores
        $("div.tabla-facturacion").on('change', function(){
                    
    		var cantidades = document.getElementsByName("cantidad");
    		var valores_unidad = document.getElementsByName("precio_unidad");
    		var valores_totales = document.getElementsByName("precio_total");
    		var precio_total_group = $('input[name="precio_total"]');
			var subtotal = 0;
			
			for(var i = 0; i < cantidades.length ; i++)
			{
				cantidad = Number(cantidades[i].value);
				costo = Number(valores_unidad[i].value);
				
				var total = cantidad * costo;
				
				subtotal += total;
				
				valores_totales[i].innerHTML = total;
				
			}
			
			var iva = subtotal * 19/100;
			var total = subtotal + iva;
			
			
			var sub_total = document.getElementsByName("sub_total");
			sub_total[0].innerHTML = subtotal;
			$('#subtotalinput').val(subtotal);
			console.log('1');
			
			var iva_total = document.getElementsByName("iva_total");
			iva_total[0].innerHTML = iva;
            $('#iva2').val(iva);
            console.log('2');
			
			var total1 = document.getElementsByName("total");
			total1[0].innerHTML = total;
            $('#total2').val(total);
            console.log('3');
 
    	 }); 
    	 
    	
        // 	Validar Consecutivo de la Dian
        $( "#consecutivo" ).keypress(function() {
            setTimeout(validarConsecutivo, 100);
        });
        
        function validarConsecutivo(){
            
            var consecutivo = $('#consecutivo').val();
            var dicc = { 'consecutivo' : consecutivo };
            
            $.ajax({ 
                
                data: dicc,
                type: 'POST',
                url: 'validar_consecutivo/',
                
                success: function(response) { 
                
                    if(response.status=="False")
                    {
                        //Cambio de Positivo a Negativo
                        $( "#consecutivo_id" ).removeClass('has-success');
                        $( "#span_id" ).removeClass('fa-check');
                        $( "#consecutivo_id" ).addClass('has-error');
                        $( "#span_id" ).addClass('fa-times');
                        
                        
                    }
                    else
                    {
                        //Cambio de Negativo a Positivo
                        $( "#consecutivo_id" ).removeClass('has-error');
                        $( "#span_id" ).removeClass('fa-times');
                        $( "#consecutivo_id" ).addClass('has-success');
                        $( "#span_id" ).addClass('fa-check');
                        
                    };
                }
            });
        
        }
        
    });