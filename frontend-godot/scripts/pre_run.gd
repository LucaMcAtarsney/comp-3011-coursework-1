extends CanvasLayer

# --- UI Node References ---
# Make sure your nodes in the scene are named "PlayerNameEdit", "PasswordEdit", etc.
@onready var player_name_edit: LineEdit = $Username
@onready var password_edit: LineEdit = $Password
@onready var error_label: Label = $"Doesnt Exist"
@onready var start_button: Button = $"Start Button"

func _ready() -> void:
	# Connect to the signals from the Network singleton
	Network.game_session_started.connect(_on_game_session_started)
	Network.authentication_failed.connect(_on_authentication_failed)
	
	# Hide the error label initially
	error_label.visible = false
	
	# Set focus to the name input field for a better user experience
	player_name_edit.grab_focus()

# --- Signal Handlers ---

# Called when the user clicks the "Start" button
func _on_start_button_button_up() -> void:
	var player_name: String = player_name_edit.text
	var password: String = password_edit.text
	
	# Basic validation to ensure fields are not empty
	if player_name.is_empty() or password.is_empty():
		show_error("Player name and password cannot be empty.")
		return
		
	# Disable the button to prevent multiple clicks while waiting for the server
	start_button.disabled = true
	error_label.visible = false # Hide previous errors
	
	# Call the network function to log in the existing player
	Network.start_game_session(player_name, password, false)

# Called by the Network singleton on successful login
func _on_game_session_started(player_id: int, run_id: int) -> void:
	# The server has confirmed the login, so we can proceed to the game
	get_tree().change_scene_to_file("res://scenes/arena.tscn")

# Called by the Network singleton if authentication fails
func _on_authentication_failed(error_message: String) -> void:
	# Show the error message and re-enable the button so the user can try again
	show_error(error_message)
	start_button.disabled = false

# --- Helper Functions ---

func show_error(message: String) -> void:
	error_label.text = message
	error_label.visible = true


func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/second_screen.tscn")
