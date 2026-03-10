# devmode.gd
extends CanvasLayer

@onready var container = $ScrollContainer/VBoxContainer
@onready var toggle_button: Button = $ToggleViewButton # Make sure you have a button named ToggleViewButton

# --- Add references to your header labels ---
@onready var header_col1: Label = $Headers/RunID
@onready var header_col2: Label = $Headers/Player
@onready var header_col3: Label = $Headers/Time
@onready var header_col4: Label = $Headers/Level
@onready var header_col5: Label = $"Headers/Monsters Slain"

@onready var Player_Headers = $"Player Headers"
@onready var Run_Headers = $"Run Headers"


@export var record_scene: PackedScene = preload("res://scenes/db_record.tscn")

enum ViewMode { PLAYERS, RUNS }
var current_view: ViewMode = ViewMode.RUNS

# --- New function to update header text ---
func update_headers():
	if current_view == ViewMode.RUNS:
		Run_Headers.visible = true
		Player_Headers.visible = false
		
	else: # current_view is PLAYERS
		Player_Headers.visible = true
		Run_Headers.visible = false

func _ready() -> void:
	Network.all_runs_received.connect(_on_runs_received)
	Network.players_received.connect(_on_players_received)
	
	# Set initial button text
	toggle_button.text = "Viewing Runs Data"
	Run_Headers.visible = true
	
	# Fetch the initial data
	fetch_data_for_current_view()

# --- Data Fetching ---

func fetch_data_for_current_view():
	
	update_headers()
	
	for child in container.get_children():
		child.queue_free()
		
	if current_view == ViewMode.RUNS:
		Network.get_runs()
	else:
		Network.get_players()

# --- Signal Handlers for Receiving Data ---

func _on_runs_received(runs_data: Array) -> void:
	if current_view != ViewMode.RUNS:
		return

	for run_data in runs_data:
		var record = record_scene.instantiate()
		container.add_child(record)
		record.setup_as_run(run_data)
		record.delete_requested.connect(_on_delete_run_requested)

func _on_players_received(players_data: Array) -> void:
	if current_view != ViewMode.PLAYERS:
		return

	for player_data in players_data:
		var record = record_scene.instantiate()
		container.add_child(record)
		record.setup_as_player(player_data)
		record.delete_requested.connect(_on_delete_player_requested)
		record.edit_requested.connect(_on_edit_player_requested)

func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/analytics.tscn")

# --- Action Handlers from Records ---

func _on_delete_run_requested(run_id: int):
	print("Requesting to delete run: ", run_id)
	Network.admin_delete_run(run_id)
	await get_tree().create_timer(0.5).timeout
	fetch_data_for_current_view()

func _on_delete_player_requested(player_id: int):
	print("Requesting to delete player: ", player_id)
	Network.admin_delete_player(player_id)
	await get_tree().create_timer(0.5).timeout
	fetch_data_for_current_view()

func _on_edit_player_requested(player_id: int, new_name: String):
	print("Requesting to edit player %s with new name: %s" % [player_id, new_name])
	Network.admin_update_player_name(player_id, new_name)
	await get_tree().create_timer(0.5).timeout
	fetch_data_for_current_view()




func _on_toggle_view_button_button_up() -> void:
	if current_view == ViewMode.RUNS:
		current_view = ViewMode.PLAYERS
		toggle_button.text = "Viewing Player Data"
	else:
		current_view = ViewMode.RUNS
		toggle_button.text = "Viewing Runs Data"
	
	fetch_data_for_current_view()
