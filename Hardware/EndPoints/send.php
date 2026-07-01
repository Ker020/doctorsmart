<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Invalid JSON"]);
    exit;
}

$bpm             = isset($data['bpm']) ? (int)$data['bpm'] : 0;
$spo2            = isset($data['spo2']) ? (int)$data['spo2'] : 0;
$temperature     = isset($data['temperature']) ? round((float)$data['temperature'], 2) : 0.0;
$body_state      = isset($data['body_state']) ? substr(trim($data['body_state']), 0, 20) : 'STABLE';
$finger_detected = isset($data['finger_detected']) ? (int)$data['finger_detected'] : 0;   // مهم: نحوله لـ 0 أو 1

$host = 'localhost';         
$db   = 'health_project';    
$user = 'root';    
$pass = '';    

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $sql = "INSERT INTO health_data 
            (bpm, spo2, temperature, body_state, finger_detected) 
            VALUES (?, ?, ?, ?, ?)";

    $stmt = $pdo->prepare($sql);
    $stmt->execute([$bpm, $spo2, $temperature, $body_state, $finger_detected]);

    echo json_encode([
        "status" => "success",
        "message" => "Data saved successfully",
        "id" => $pdo->lastInsertId()
    ]);

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode([
        "status" => "error",
        "message" => "Database error",
        "debug" => $e->getMessage()
    ]);
}
?>
