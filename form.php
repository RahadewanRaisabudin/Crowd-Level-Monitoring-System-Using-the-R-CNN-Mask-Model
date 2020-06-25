<html>
<body>
<?php
$nama = $alamat = $nomor_handphone = $jenis_kelamin = $agama = $prestasi= "";
if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["nama"]) && isset($_POST["alamat"]) && isset($_POST["nomor_handphone"])&& isset($_POST["jenis_kelamin"])&& isset($_POST["agama"])&& isset($_POST["prestasi"])) {
$nama = $_POST["nama"];
$alamat = $_POST["alamat"];
$nomor_handphone = $_POST["nomor_handphone"];
$jenis_kelamin = $_POST["jenis_kelamin"];
$agama = $_POST["agama"];
$prestasi = $_POST["prestasi"];


}
?>
<?php
echo "<h2>data validasi</h2>";
if(!empty($nama) && !empty($alamat) && !empty($nomor_handphone) && !empty($jenis_kelamin) && !empty($agama) && !empty($prestasi)) {
	
	 if (!preg_match("/[a-zA-Z ]/",$nama)) {
     	
       echo "NAMA HARUS HURUF" . "<br>";
    }
    else {
    	 echo "NAMA : " .  $nama . "<br>"; 
    }
    echo "ALAMAT : " . $alamat . "<br>";
     if (!preg_match("/[0-9]/",$nomor_handphone)) {
     	
       echo "NOMOR HARUS ANGKA" . "<br>";
    }
    else {
    	echo " NOMOR HANDPHONE : " . $nomor_handphone . "<br>";
    }

    echo "JENIS KELAMIN : " . $jenis_kelamin. "<br>" . "AGAMA : " . $agama . "<br>" . "PRESTASI : " . $prestasi;

}
else{
  echo "data kurang lengkap";
}
?>
</body>
</html>
