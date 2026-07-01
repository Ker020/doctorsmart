<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');


$host = 'localhost';
$db   = 'health_project';    
$user = 'root';    
$pass = ''; 

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


    $sql = "SELECT 
                id, 
                bpm, 
                spo2, 
                temperature, 
                body_state, 
                finger_detected, 
                timestamp 
            FROM health_data 
            ORDER BY id DESC 
            LIMIT 10";

    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);


    echo json_encode([
        "status" => "success",
        "count" => count($data),
        "data" => $data
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
