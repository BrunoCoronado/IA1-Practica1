import { Component, OnInit, ViewChild } from '@angular/core';
import { UtilsService } from './utils.service';
import { WebService } from './web.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app';

  criterioFinalizacion: number = 1;
  seleccionPadres: number = 1;

  @ViewChild('csvReader') csvReader: any; 

  data: any = []

  solucion: any = []

  notas: any = {
    proyecto1: undefined,
    proyecto2: undefined,
    proyecto3: undefined,
    proyecto4: undefined,
  };

  nc: any

  nombreArchivo: string;

  bitacora: any = [];

  constructor(private service: WebService, private utils: UtilsService) { }

  async ngOnInit(): Promise<void> {

  }

  uploadListener($event: any): void {  
    this.nombreArchivo = this.csvReader.nativeElement.value;
    this.data = []
    try {
      if(!$event.srcElement.files[0].name.endsWith(".csv")){
        this.csvReader.nativeElement.value = "";
        this.utils.mostrarError('Archivo invalido. Debe ser .csv!')
        return
      }
  
      this.utils.mostrarLoading()

      let reader = new FileReader();  
      reader.readAsText($event.target.files[0]);  
  
      reader.onload = () => {  
        let filas = (<string>reader.result).split(/\r\n|\n/);  
        filas.forEach((f, i) => {
          let columnas = f.split(/,/)
          if(columnas[0] && i > 0)
            this.data.push(columnas.map(v => parseFloat(v)))
        });

        this.utils.ocultarLoading()
        this.csvReader.nativeElement.value = "";
        this.utils.mostrarToast('Datos cargados correctamente!')
      };  
  
      reader.onerror = () => {
        this.utils.ocultarLoading()
        this.csvReader.nativeElement.value = "";
        this.utils.mostrarError('Archivo invalido. Debe ser .csv!')
        return
      }
    } catch (error) {
      console.log(error)
      this.utils.ocultarLoading()
      this.csvReader.nativeElement.value = "";
      this.utils.mostrarError('Ocurrio un error al cargar datos')
    }
  }

  async generarModelo(){
    this.bitacora = []
    if(this.data.length == 0){
      this.utils.mostrarError('Sin datos!')
      return
    }

    const data = {
      criterio: this.criterioFinalizacion,
      seleccion: this.seleccionPadres,
      data: this.data,
      nombre: this.nombreArchivo
    }

    this.utils.mostrarLoading()

    const response: any = await this.service.generarModelo(data);

    this.utils.ocultarLoading()

    if(response.status == 200){
      this.solucion = response.solucion
      this.utils.mostrarToast(response.mensaje)
    }else
      this.utils.mostrarError(response.mensaje)
  }

  async calcularNota(){
    if(!this.notas.proyecto1){
      this.utils.mostrarError('Sin nota del proyecto 1!')
      return
    }
    if(!this.notas.proyecto2){
      this.utils.mostrarError('Sin nota del proyecto 2!')
      return
    }
    if(!this.notas.proyecto3){
      this.utils.mostrarError('Sin nota del proyecto 3!')
      return
    }
    if(!this.notas.proyecto4){
      this.utils.mostrarError('Sin nota del proyecto 4!')
      return
    }
    
    this.nc = (this.solucion[0]*this.notas.proyecto1) + (this.solucion[1]*this.notas.proyecto2) + (this.solucion[2]*this.notas.proyecto3) + (this.solucion[3]*this.notas.proyecto4)
  }

  async verBitacora(){
    this.bitacora = []
    this.utils.mostrarLoading()

    const response: any = await this.service.obtenerBitacora();

    this.utils.ocultarLoading()

    if(response.status == 200){
      this.data = []
      this.utils.mostrarToast(response.mensaje)
      let filas = response.bitacora.split(/\r\n|\n/)
      filas.forEach(f => {
        let columnas = f.split(/;/)
        if(columnas[0])
          this.bitacora.push(columnas)
      });
    }else{
      this.utils.mostrarError(response.mensaje)
    }
  }
}
