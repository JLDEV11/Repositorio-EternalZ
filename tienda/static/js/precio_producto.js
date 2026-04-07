    const precio_producto=document.getElementById('precio_producto')
    

    document.getElementById('variante').addEventListener('change', function() {
           const precio = this.options[this.selectedIndex].dataset.precio;

       

      
        precio_producto.textContent = '$' + Number(precio).toLocaleString('es-CO');

        
    });