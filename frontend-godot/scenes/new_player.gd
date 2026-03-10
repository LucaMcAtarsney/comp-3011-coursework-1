extends CanvasLayer

# --- UI Node References ---
@onready var player_name_label: Label = $Name
@onready var password_edit: LineEdit = $Password
@onready var error_label: Label = $ErrorLabel
@onready var start_button: Button = $"Start Button"

var generated_player_name: String = ""
# --- New variable to track session state ---
var is_session_started: bool = false

func _ready() -> void:
	# --- Connect Signals ---
	Network.random_name_received.connect(_on_random_name_received)
	Network.game_session_started.connect(_on_game_session_started)
	Network.authentication_failed.connect(_on_authentication_failed)
	
	# --- Initial UI State ---
	error_label.visible = false
	start_button.disabled = true
	player_name_label.text = "..........................."
	password_edit.editable = false
	
	# --- Start the Process ---
	Network.generate_random_name()

# --- Signal Handlers ---

func _on_random_name_received(player_name: String) -> void:
	generated_player_name = player_name
	player_name_label.text = player_name
	
	password_edit.editable = true
	password_edit.grab_focus()
	start_button.disabled = false

func _on_start_button_button_up() -> void:
	var password := password_edit.text
	
	if password.is_empty():
		show_error("Password cannot be empty.")
		return
		
	if generated_player_name.is_empty():
		show_error("Could not retrieve a player name. Please try again.")
		return
	
	start_button.disabled = true
	error_label.visible = false
	
	Network.start_game_session(generated_player_name, password, true)

func _on_game_session_started(player_id: int, run_id: int) -> void:
	# --- The player and session are now created on the server ---
	is_session_started = true
	
	# Store credentials in global state
	global.player_name = generated_player_name
	global.player_password = password_edit.text
	
	# Proceed to the game
	get_tree().change_scene_to_file("res://scenes/arena.tscn")

func _on_authentication_failed(error_message: String) -> void:
	show_error(error_message)
	start_button.disabled = false

# --- Helper Functions ---

func show_error(message: String) -> void:
	error_label.text = message
	error_label.visible = true

# --- Back Button Logic ---
func _on_go_back_button_up() -> void:	
	# Go back to the previous screen
	get_tree().change_scene_to_file("res://scenes/second_screen.tscn")
