<?php

header('Content-Type: application/json');
$conn = new mysqli("localhost:3307", "root", "", "eshop_db");

if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed"]));
}

// Input parameters
$category = $_GET['category'] ?? '';
$tags = $_GET['tags'] ?? '';
$price = $_GET['price'] ?? 0;
$price_condition = $_GET['price_condition'] ?? '';

// Escape to prevent SQL injection
$category = $conn->real_escape_string($category);
$tags = $conn->real_escape_string($tags);

// Start the SQL query
$sql = "SELECT * FROM products WHERE 1=1";

// Filter by category
if (!empty($category)) {
    $sql .= " AND product_category LIKE '%$category%'";
}

// Filter by tags or description
if (!empty($tags)) {
    $sql .= " AND (product_tags LIKE '%$tags%' OR product_description LIKE '%$tags%')";
}

// Filter by price condition
if ($price > 0) {
    if ($price_condition == 'under') {
        $sql .= " AND product_price <= $price";
    } elseif ($price_condition == 'above') {
        $sql .= " AND product_price >= $price";
    } elseif ($price_condition == 'around') {
        $low = $price - 2000;
        $high = $price + 2000;
        $sql .= " AND product_price BETWEEN $low AND $high";
    } else {
        $sql .= " AND product_price = $price";
    }
}

// Run the query
$result = $conn->query($sql);

// Show results
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
