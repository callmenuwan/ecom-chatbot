<?php

header('Content-Type: application/json');
$conn = new mysqli("localhost:3307", "root", "", "eshop_db");

if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed"]));
}

$sql = "SELECT * FROM products";
$result = $conn->query($sql);

$products = [];
while($row = $result->fetch_assoc()) {
    $products[] = $row;
}

echo json_encode($products);

?>
