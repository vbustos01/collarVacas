
<html> 
   <head>
      <title>Datos Vaca nº1</title>
      <meta http-equiv="refresh" content="5">
   </head> 
    <body background="87397.jpg">

<?php
    include("datos.php");
    $conexion = mysqli_connect($host,$usuario,$clave);
    $consulta = "SELECT * FROM Vaca1;";
    mysqli_select_db($conexion,$base);
    $data=mysqli_query($conexion,$consulta);
?>
<table id="example" class="display" style="width:100%">
<tr>
    <!--<td>ID</td>-->
    <td>Fecha de recoleción</td>
    <td>Nivel Bateria (v)</td>
    <td>Datos GPS</td>
	<td>Datos IMU</td>
	<td>Estado SD</td>
	<td>Datos Microfono</td>
	<td>Collar Abierto</td>
	<td>Latitud</td>
	<td>Longitud</td>
	<td>Guardado el:</td>
</tr>
<?php
    while($fila=mysqli_fetch_array($data)){
        echo "<tr>";
        //echo "<td>".$fila ["ID"]."</td>";
        echo "<td>".$fila["Fecha"]."</td>";
        echo "<td>".$fila ["Nivel_Bateria"]."</td>";
        echo "<td>".$fila["Datos_GPS"]."</td>";
        echo "<td>".$fila["Datos_IMU"]."</td>";
        echo "<td>".$fila["Estado_SD"]."</td>";
        echo "<td>".$fila["Datos_Microfono"]."</td>";
        echo "<td>".$fila["Collar_Abierto"]."</td>";
        echo "<td>".$fila["Latitud"]."</td>";
        echo "<td>".$fila["Longitud"]."</td>";
        echo "<td>".$fila["time"]."</td>";
        echo "</tr>";}
?>
</table>  
</body> 
</html>
