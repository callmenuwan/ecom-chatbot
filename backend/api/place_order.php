<?php
// backend/api/place_order.php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");
header("Access-Control-Allow-Methods: POST");

$conn = new mysqli("localhost:3307", "root", "", "eshop_db");

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["success" => false, "message" => "DB connection failed"]);
    exit;
}

$data = json_decode(file_get_contents("php://input"), true);

if (!isset($data["name"], $data["email"], $data["phone"], $data["items"])) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Missing input"]);
    exit;
}

$name = $conn->real_escape_string($data["name"]);
$email = $conn->real_escape_string($data["email"]);
$phone = $conn->real_escape_string($data["phone"]);
$items = $data["items"];

$conn->begin_transaction();

try {
    // Insert into users table
    $query = "INSERT INTO users (user_fname, user_email, user_phone) VALUES ('$name', '$email', '$phone')";
    if (!$conn->query($query)) {
        throw new Exception("User insert failed: " . $conn->error);
    }
    $user_id = $conn->insert_id;

    // Insert into orders table
    $sql = "INSERT INTO orders (user_id) VALUES ($user_id)";
    if (!$conn->query($sql)) {
        throw new Exception("Order insert failed: " . $conn->error);
    }
    $order_id = $conn->insert_id;

    // Insert into order_items table
    foreach ($items as $item) {
        $product = $conn->real_escape_string($item["product_id"]);
        $price = floatval($item["product_price"]);
        $qty = floatval($item["quantity"]);
        $order_prodcuct_price = $price*$qty;

        $item_sql = "INSERT INTO order_items (order_id, product_id, qty, order_prodcuct_price)
                     VALUES ($order_id, '$product', '$qty', '$order_prodcuct_price')";
        if (!$conn->query($item_sql)) {
            throw new Exception("Order item insert failed: " . $conn->error);
        }
    }

    $conn->commit();
    echo json_encode([
        "success" => true,
        "user_id" => $user_id,
        "order_id" => $order_id
    ]);
} catch (Exception $e) {
    $conn->rollback();
    http_response_code(500);
    echo json_encode([
        "success" => false,
        "message" => "Order placement failed",
        "error" => $e->getMessage()
    ]);
}

$conn->close();
?>
