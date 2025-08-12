<?php

header('Content-Type: application/json');
$conn = new mysqli("localhost:3307", "root", "", "eshop_db");

if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed"]));
}

// Input parameters
$category = isset($_GET['category']) ? $conn->real_escape_string($_GET['category']) : '';
$max_price = isset($_GET['max_price']) ? floatval($_GET['max_price']) : 0;
$tags = isset($_GET['tags']) ? $conn->real_escape_string($_GET['tags']) : '';

// Build one compact SQL query
$sql = "
    SELECT * FROM products
    WHERE 
        ('$category' = '' OR product_category LIKE '%$category%')
        AND ($max_price = 0 OR product_price <= $max_price)
        AND ('$tags' = '' OR product_tags LIKE '%$tags%' OR product_description LIKE '%$tags%')
";

// Run query
$result = $conn->query($sql);
$products = [];

if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $products[] = $row;
    }
}

echo json_encode($products);
$conn->close();

// $sql = "SELECT * FROM products";
// $result = $conn->query($sql);

// $products = [];
// while($row = $result->fetch_assoc()) {
//     $products[] = $row;
// }

// echo json_encode($products);

?>
