import { Injectable } from '@angular/core';
import Swal from 'sweetalert2/dist/sweetalert2.js';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  private loading = Swal.mixin({
    showConfirmButton: false,
    onBeforeOpen: () => {
      Swal.showLoading()
    }
  })

  private toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  constructor() { }

  mostrarLoading(){
    this.loading.fire()
  }

  ocultarLoading(){
    this.loading.close()
  }

  mostrarError(mensaje){
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: mensaje,
    })
  }

  mostrarToast(mensaje){
    this.toast.fire({
      icon: 'success',
      title: mensaje
    })
  }
}
