<!DOCTYPE html>
<html>
<head>
	<?php include("src/header.php"); ?>
</head>

<body class="blue lighten-5">

	<?php include("src/navbar.php"); ?>

	<?php
	$datasetJSON = file_get_contents("http://192.168.1.20:1111/dataset/");
	$dataset = json_decode($datasetJSON);
	?>

	<section>
		<?php include("src/sections/presentationDatas.php"); ?>
	</section>

	<section>
		<?php include("src/sections/cardDatas.php"); ?>
	</section>



	<?php include("src/footer.php"); ?>

</body>
</html>

