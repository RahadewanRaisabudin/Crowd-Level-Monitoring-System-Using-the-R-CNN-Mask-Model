<?php
$nama = $alamat = $nomor_handphone = $jenis_kelamin = $agama = $keahlian= $posisi = $ttl= "";
if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["nama"]) && isset($_POST["alamat"]) && isset($_POST["nomor_handphone"])&& isset($_POST["jenis_kelamin"])&& isset($_POST["agama"])&& isset($_POST["keahlian"])&& isset($_POST["posisi"])&& isset($_POST["ttl"])) {
$nama = $_POST["nama"];
$alamat = $_POST["alamat"];
$nomor_handphone = $_POST["nomor_handphone"];
$jenis_kelamin = $_POST["jenis_kelamin"];
$agama = $_POST["agama"];
$ttl = $_POST["ttl"];
$posisi = $_POST["posisi"];
$keahlian = $_POST["keahlian"];
 $namafile = "file.txt"; 
 $a = "NAMA = ";  
 $b = "ALAMAT = "; 
 $c = "JENIS KELAMIN = "; 
 $d = "AGAMA = "; 
 $e = "NOMOR HANDPHONE = "; 
 $f = "POSISI = "; 
 $g = "KEAHLIAN = ";  
 $h = " , ";



}
?>
<?php
echo "<h2>data validasi</h2>";
if(!empty($nama) && !empty($alamat) && !empty($nomor_handphone) && !empty($jenis_kelamin) && !empty($agama)&& !empty($ttl)&& !empty($posisi) && !empty($keahlian)) {
  
   if (!preg_match("/[a-zA-Z ]/",$nama)) {
      
       echo "NAMA HARUS HURUF" . "<br>";
    }
    else {
       echo "NAMA : " .  $nama . "<br>"; 
    }
    echo "ALAMAT : " . $alamat . "<br>";
    echo "JENIS KELAMIN : " . $jenis_kelamin. "<br>" ;
     if (!preg_match("/[0-9]/",$ttl)) {
      
       echo "TANGGAL LAHIR HARUS ANGKA" . "<br>";
    }
    else {
      echo " TANGGAL LAHIR : " . $ttl . "<br>";
    }

     if (!preg_match("/[0-9]/",$nomor_handphone)) {
      
       echo "NOMOR HARUS ANGKA" . "<br>";
    }
    else {
      echo " NOMOR HANDPHONE : " . $nomor_handphone . "<br>";
    }

    echo "AGAMA : " . $agama . "<br>" . "POSISI : " . $posisi. "<br>" . "KEAHLIAN : " . $keahlian;

}
else{
  echo "data kurang lengkap";
}
 $file = fopen($namafile,"w");  
 fwrite($file,$nama."\n");
 fwrite($file,$alamat."\n"); 
  fwrite($file,$jenis_kelamin."\n");
 fwrite($file,$ttl."\n");

  fwrite($file,$agama."\n");

  fwrite($file,$nomor_handphone."\n");

  fwrite($file,$posisi."\n");
 
  fwrite($file,$keahlian."\n");
 fclose($file);  
 echo "<h2>Hasil Penyimpanan Data</h2>";  
 echo "<hr>";  
 echo "Hasil : <a href='$namafile'> $namafile </a>";  
 echo "<h2>Hasil Tampilan</h2>";
  echo "<hr>"; 
  echo "<a href='table.php'>tamplian</a>";

?>
