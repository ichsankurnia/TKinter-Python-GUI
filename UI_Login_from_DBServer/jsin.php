<?php
	$conn = mysqli_connect('localhost', 'goesnobe_cam', 'sureTrea53', 'goesnobe_security');
	// Check connection
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 

	$sql = "SELECT * FROM user";
	$result = mysqli_query($conn, $sql);

	$data = array();

	while ($row = mysqli_fetch_array($result))
	{
		array_push($data, array(
			"id" 	        =>	$row[0],
			"name"	        =>	$row[1],
			"email"	        =>	$row[2],
			"number"	    =>	$row[3],
			"password"	    =>	$row[4]
		));
	}

echo json_encode(array("user"=>$data));

?>