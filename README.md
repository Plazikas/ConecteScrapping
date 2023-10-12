# ConecteScrapping
The progam excracts files from "https://www.conecte.es/index.php/es/plantas/mapa" and export them into an excel by a monitorized way
# Requirements
- Python 3.8.10
- selenium 4.10.0
- pandas 2.0.3
# Use
1. **Selecting province**<br>
	1.1. Select the province we want, in this example Almería ~ Andalucía <br>
   1.2. Press 'Aplicar filtros' <br>
![Image](img/1_SeleccionarProvincia_edited.jpg)<br>
2. **Take municipalities one by one**<br>
   2.1. Save municipality and comarca info <br>
   2.2. Click into the municipality link<br>
![Image](img/2_Seleccionar_Municipio_edited.png)<br>
3. **Extract files info**<br>
	3.1. Take Fecha, Usuario, Ficha, Tipo and Contenido for each file<br>
![Image](img/3_ObtenerDatosFichas_edited.png)<br>
4. **Export info for each file into an excel**<br>
   4.1. Each row content Municipality, Comarca, Date, User, File, Type and Content<br>
![Image](img/4_ExcelResultado_edited.png)<br>
