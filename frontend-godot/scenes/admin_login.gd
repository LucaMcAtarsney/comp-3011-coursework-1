extends CanvasLayer

@onready var username_edit: LineEdit = $Username
@onready var password_edit: LineEdit = $Password
@onready var start_button: Button = $"Start Button"
@onready var error_label: Label = $"Doesnt Exist"

func _ready() -> void:
	# Connect to the new admin signals from the Network singleton
	Network.admin_login_successful.connect(_on_admin_login_successful)
	Network.admin_login_failed.connect(_on_admin_login_failed)
	
	# Initial UI state
	error_label.visible = false
	username_edit.grab_focus()

func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/analytics.tscn")

func _on_start_button_button_up() -> void:
	var user := username_edit.text
	var password := password_edit.text
	
	if user.is_empty() or password.is_empty():
		show_error("Username and password cannot be empty.")
		return
	
	# Disable UI while we wait for the server
	start_button.disabled = true
	error_label.visible = false
	
	# Call the network function to check credentials
	Network.check_admin_login(user, password)

# --- Signal Handlers ---

func _on_admin_login_successful() -> void:
	# Credentials were correct, proceed to the dev mode scene
	get_tree().change_scene_to_file("res://scenes/devmode.tscn")

func _on_admin_login_failed(error_message: String) -> void:
	# Show the error and re-enable the UI
	show_error(error_message)
	start_button.disabled = false

# --- Helper Function ---

func show_error(message: String) -> void:
	error_label.text = message
	error_label.visible = true
