extends Node2D

@export var enemy_types: Array[PackedScene] =[
	preload("res://scenes/enemy1.tscn"),
	preload("res://scenes/enemy2.tscn"),
	preload("res://scenes/enemy3.tscn")
	]
	
@export var spawn_area = Rect2(Vector2(0, 0), Vector2(300, 300))  # Set this to your desired area

@onready var spawn_timer = $SpawnTimer
@onready var incrementer = $Incrementer
@onready var player = $"../player"
@export var min_spawn_distance = 200
@export var max_spawn_distance = 400



func _ready():
	spawn_timer.timeout.connect(_on_spawn_timer_timeout)
	spawn_timer.start()

func _on_spawn_timer_timeout():
	var enemy_scene: PackedScene = enemy_types.pick_random()
	var enemy = enemy_scene.instantiate()

	var angle := randf() * TAU
	var distance := randf_range(min_spawn_distance, max_spawn_distance)
	
	var offset := Vector2(cos(angle), sin(angle)) * distance
	
	enemy.global_position = player.global_position + offset
	enemy.attacked.connect(player._on_player_attacked)
	get_tree().root.add_child(enemy)


func _on_incrementer_timeout() -> void:
	
	spawn_timer.wait_time = spawn_timer.wait_time * 0.95
	print(spawn_timer.wait_time)
