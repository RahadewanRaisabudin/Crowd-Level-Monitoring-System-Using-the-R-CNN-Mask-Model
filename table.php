<!DOCTYPE html>
<html>
  <head>
    <title>tabel</title>
  </head>
  <style type="text/css">
    .kertas       
 .sheet { width: 210mm; height: 296mm }
.sheet.padding-20mm { padding: 20mm }
  .sheet {
    background: lavender;
    box-shadow: 0 .5mm 2mm rgba(0,0,0,.3);
    margin: 5mm auto;
  }
  .foot
  .sheet2 { width: 190mm; height: 10mm }
.sheet2.padding-10mm { padding: 10mm }
  .sheet2{
    background: silver;
    margin: 175mm auto;
    position: absolute;
    bottom: 250;
  }
  </style>
  <body bgcolor="yellow">

           <div class="kertas">
    <section class="sheet padding-20mm">
        <br></br>
        <table class="table">
                  <table border ="1" style="width:100%; border-collapse: collapse">
        <td colspan = "5" bgcolor="yellow"> 
        <h1 align="center">DATA PENDAFTAR LOWONGAN PEKERJAAN PERUSAHAAN</h1></td>
   <aside>
    <tr>
        <td bgcolor="yellow" width="3%" ><br>
        <td colspan="3" >
    <?php
      echo "<br>";
      echo "NAMA :" . "<br>";
      echo "ALAMAT :" . "<br>";
      echo "JENIS KELAMIN :" . "<br>";
      echo "TANGGAL LAHIR :" . "<br>";
      echo "AGAMA :" . "<br>";
      echo "NOMOR HANDPHONE :" . "<br>";
      echo "KEAHLIAN :" . "<br>";
      echo "POSISI :" . "<br>";
    ?>

          
        </td>
      </aside>
    <aside>
      <td bgcolor="silver" width="50%"><h3 align="center"></h3>
   <?php 
$lines = file('file.txt'); 
foreach ($lines as $line_num => $line){
  print  $line . "<br />\n"; 
}
?>
      </td>
    </aside>
    </tr>

    <footer>
        <td colspan = "5" bgcolor="yellow"> 
       <p align="center">@PTPERUSAHAAN</p>
        </footer>
    </table>
  	
     

</body>
</html>
