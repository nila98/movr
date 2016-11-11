<?php

$servername = "127.0.0.1";
$username = "root";
$password = "root";
$dbname = "IMDB0";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

echo "Demo Query<br><br>";

//$sql = "INSERT INTO Peoplee (firstname, lastname, age) VALUES ('John', 'Doe', '23')";
/*
if ($conn->query($sql) === TRUE) {
	echo "added new data<br>";
} else {
	echo "Errorrr " . $conn->error;
}
*/

/*
$sql = "SELECT title FROM title WHERE id IN (
		SELECT movie_id FROM cast_info WHERE person_id = (
			SELECT id FROM name WHERE name = 'Page, Ellen'))";
*/
$sql = "SELECT info FROM movie_info WHERE movie_id = (
SELECT id FROM `title` WHERE title = 'Inception' AND kind_id = '1')
AND
info_type_id = (
SELECT id FROM info_type WHERE info = 'plot')";


echo "Ellen Page Movies:<br>";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
	while ($row = $result->fetch_assoc()) {
		echo "info: " . $row["info"] . "<br>";
	}
}



/*
if ($conn->query($sql) === TRUE) {
	echo "added new data<br>";
} else {
	echo "Errorrr " . $conn->error;
}
*/
$conn->close();

?>


