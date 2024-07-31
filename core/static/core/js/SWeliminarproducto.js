
const btnsEliminacion = document.querySelectorAll('.btnEliminacion');   

(function (){
    /*
    btnsEliminacion.forEach(btn => {
        btn.addEventListener('click', function(e){
            let confirmacion = confirm("Confirma la eliminacion ??");
            if(!confirmacion){
                e.preventDefault();
            }
        })
        
    })
    */
    btnsEliminacion.forEach((btn) => {
        btn.addEventListener("click", function(e){
            e.preventDefault();
            //console.log(e.target.href);
            swal.fire({
                icon: "question",
                title: "¿Confirma la eliminacion del producto?",
                showCancelButton:true,
                confirmButtonText:"Eliminar",
                confirmButtonColor:"#d33",
                backdrop:true,
                showLoaderOnConfirm:true,
                preConfirm: () => {
                    //console.log("Confirmado!!")
                    swal.fire({
                        icon: "success",
                        title: "Producto Eliminado",
                        timer: 5000,
                        showConfirmButton: false,
                    })
                    setTimeout(() => {    
                        location.href = e.target.href;
                    }, 1000)
                    
                },
                allowOutsideClick:()=>false,
                allowEscapeKey:()=>false,
            })
        })
    })

})();


