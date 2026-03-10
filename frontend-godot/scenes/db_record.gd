# db_record.gd
extends HBoxContainer

# Signals to notify the dev panel (the parent) that a button was clicked.
# We pass the ID so the parent knows which record to act on.
signal delete_requested(id: int)
signal edit_requested(id: int, new_name: String)

# --- UI Node References ---
# Make sure to wire these up in the Inspector tab in Godot.
@onready var id_label: Label = $Row/IDLabel
@onready var name_label: Label = $Row/NameLabel
@onready var name_edit: LineEdit = $Row/NameEdit
@onready var details_label: Label = $Row/DetailsLabel
@onready var edit_button: Button = $Row/Actions/EditButton
@onready var delete_button: Button = $Row/Actions/DeleteButton

var record_id: int # To store the ID of the player or run.

func _ready() -> void:
	# Connect the button signals to functions within this script.
	delete_button.pressed.connect(_on_delete_pressed)
	edit_button.pressed.connect(_on_edit_pressed)
	name_edit.text_submitted.connect(_on_name_submitted)

# --- Public Configuration Functions ---
# These will be called by devmode.gd to set up the record.

func setup_as_run(data: Dictionary):
	record_id = data["id"]
	
	id_label.text = str(record_id)
	name_label.text = data["player"]["name"]
	
	# Format the duration time
	var minutes = int(data["duration_seconds"]) / 60
	var seconds = int(data["duration_seconds"]) % 60
	details_label.text = "%02d:%02d" % [minutes, seconds]
	
	# For runs, we only allow deleting.
	edit_button.visible = false
	name_edit.visible = false

func setup_as_player(data: Dictionary):
	record_id = data["id"]
	
	id_label.text = str(record_id)
	name_label.text = data["name"]
	details_label.text = str(int(data["total_runs"]))
	
	# For players, we allow editing and deleting.
	edit_button.visible = true
	name_edit.visible = false # The edit field is hidden until "Edit" is clicked.

# --- Internal Button Handlers ---

func _on_delete_pressed():
	# When the delete button is clicked, emit a signal to the parent.
	delete_requested.emit(record_id)

func _on_edit_pressed():
	# When the edit button is clicked, show the LineEdit and hide the Label.
	name_label.visible = false
	name_edit.visible = true
	name_edit.text = name_label.text # Pre-fill with the current name.
	name_edit.grab_focus()

func _on_name_submitted(new_text: String):
	# When the user presses Enter in the LineEdit...
	if not new_text.is_empty():
		# Emit a signal to the parent with the ID and the new name.
		edit_requested.emit(record_id, new_text)
	
	# Hide the edit field and show the label again.
	name_label.visible = true
	name_edit.visible = false
