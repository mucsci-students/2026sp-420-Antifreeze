// ---------------------------------------------------------------------------
// CONTROLLER
//    Orchestrates between Model and View
// ---------------------------------------------------------------------------

import * as Model from "./navigation_model.js";
import { NavigationOriginator, command_history } from "./navigation_model.js";
import * as View from "./navigation_view.js";

// ---------------------------------------------------------------------------
// Validation functions
// ---------------------------------------------------------------------------

// Validates all inputs for the Faculty Add/Modify form.
// Returns true if all fields are valid, false if any errors were shown.
// Parameters: is_add - boolean, true when adding (all fields required)
function validate_faculty_form(is_add) {
  View.clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("faculty-name");
  const max_credits_input = document.getElementById("faculty-max-credits");
  const min_credits_input = document.getElementById("faculty-min-credits");
  const unique_limit_input = document.getElementById("faculty-unique-course-limit");
  const max_days_input = document.getElementById("faculty-max-days");

  const name = name_input ? name_input.value.trim() : "";
  const max_credits = max_credits_input ? max_credits_input.value.trim() : "";
  const min_credits = min_credits_input ? min_credits_input.value.trim() : "";
  const unique_limit = unique_limit_input ? unique_limit_input.value.trim() : "";
  const max_days = max_days_input ? max_days_input.value.trim() : "";

  // Faculty name: required always; letters/spaces/hyphens/apostrophes only
  if (!name) {
    View.show_field_error(name_input, "Faculty name is required.");
    valid = false;
  } else if (!/^[A-Za-z\s'\-]+$/.test(name)) {
    View.show_field_error(name_input, "Faculty name must contain only letters, spaces, hyphens, or apostrophes.");
    valid = false;
  }

  // Max credits: required on add; must be a non-negative integer if provided
  if (is_add || max_credits !== "") {
    if (max_credits === "") {
      View.show_field_error(max_credits_input, "Max credits is required.");
      valid = false;
    } else if (isNaN(max_credits) || !Number.isInteger(parseFloat(max_credits)) || parseInt(max_credits) < 0) {
      View.show_field_error(max_credits_input, "Max credits must be a non-negative whole number.");
      valid = false;
    }
  }

  // Min credits: required on add; must be a non-negative integer if provided
  if (is_add || min_credits !== "") {
    if (min_credits === "") {
      View.show_field_error(min_credits_input, "Min credits is required.");
      valid = false;
    } else if (isNaN(min_credits) || !Number.isInteger(parseFloat(min_credits)) || parseInt(min_credits) < 0) {
      View.show_field_error(min_credits_input, "Min credits must be a non-negative whole number.");
      valid = false;
    }
  }

  // Cross-field check: min credits must not exceed max credits
  if (
    valid &&
    max_credits !== "" && min_credits !== "" &&
    !isNaN(max_credits) && !isNaN(min_credits) &&
    parseInt(min_credits) > parseInt(max_credits)
  ) {
    View.show_field_error(min_credits_input, "Min credits must be less than or equal to max credits.");
    valid = false;
  }

  // Unique course limit: required on add; must be a positive integer if provided
  if (is_add || unique_limit !== "") {
    if (unique_limit === "") {
      View.show_field_error(unique_limit_input, "Unique course limit is required.");
      valid = false;
    } else if (isNaN(unique_limit) || !Number.isInteger(parseFloat(unique_limit)) || parseInt(unique_limit) < 1) {
      View.show_field_error(unique_limit_input, "Unique course limit must be a whole number of at least 1.");
      valid = false;
    }
  }

  // Max days: required on add; must be 1-5 if provided
  if (is_add || max_days !== "") {
    if (max_days === "") {
      View.show_field_error(max_days_input, "Max days is required.");
      valid = false;
    } else if (isNaN(max_days) || !Number.isInteger(parseFloat(max_days)) || parseInt(max_days) < 1 || parseInt(max_days) > 5) {
      View.show_field_error(max_days_input, "Max days must be a whole number between 1 and 5.");
      valid = false;
    }
  }

  // Time slots: optional, but if filled must match "DAY HH:MM-HH:MM"
  const time_slot_pattern = /^(MON|TUE|WED|THU|FRI)\s+([01]\d|2[0-3]):[0-5]\d-([01]\d|2[0-3]):[0-5]\d$/;
  document.querySelectorAll('input[name="faculty-time-slot"]').forEach(input => {
    const val = input.value.trim();
    if (val !== "" && !time_slot_pattern.test(val)) {
      View.show_field_error(input, "Time slot must be in the format: MON 09:00-12:00");
      valid = false;
    }
  });

  // Mandatory days are now dropdowns — no free-text validation needed

  return valid;
}

// Validates the Faculty Delete form (name only).
// Returns true if valid, false otherwise.
function validate_faculty_delete_form() {
  View.clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("faculty-name");
  const name = name_input ? name_input.value.trim() : "";

  if (!name) {
    View.show_field_error(name_input, "Faculty name is required.");
    valid = false;
  } else if (!/^[A-Za-z\s'\-]+$/.test(name)) {
    View.show_field_error(name_input, "Faculty name must contain only letters, spaces, hyphens, or apostrophes.");
    valid = false;
  }

  return valid;
}

// Validates all inputs for the Courses Add/Modify form.
// Returns true if all fields are valid, false if any errors were shown.
// Parameters: is_add - boolean, true when adding (stricter required checks)
function validate_courses_form(is_add) {
  View.clear_all_errors();
  let valid = true;

  const id_input = document.getElementById("courses-id");
  const credits_input = document.getElementById("courses-credits");

  const course_id = id_input ? id_input.value.trim() : "";
  const credits = credits_input ? credits_input.value.trim() : "";

  // Course ID: required always; must match format like "CMSC 420"
  const course_id_pattern = /^[A-Z]{2,6}\s+\d{3,4}$/;
  if (!course_id) {
    View.show_field_error(id_input, "Course ID is required.");
    valid = false;
  } else if (!course_id_pattern.test(course_id)) {
    View.show_field_error(id_input, "Course ID must be in the format: CMSC 420 (uppercase letters, space, then 3-4 digits).");
    valid = false;
  }

  // Credits: required on add; must be a positive integer if provided
  if (is_add || credits !== "") {
    if (credits === "") {
      View.show_field_error(credits_input, "Credits is required.");
      valid = false;
    } else if (isNaN(credits) || !Number.isInteger(parseFloat(credits)) || parseInt(credits) < 1) {
      View.show_field_error(credits_input, "Credits must be a whole number greater than 0.");
      valid = false;
    }
  }

  // Rooms: at least one non-empty entry required when adding
  if (is_add) {
    const room_inputs = [...document.querySelectorAll('[name="courses-room"]')];
    const filled_rooms = room_inputs.filter(i => i.value.trim() !== "");
    if (room_inputs.length > 0 && filled_rooms.length === 0) {
      View.show_field_error(room_inputs[0], "At least one room is required.");
      valid = false;
    }
  }

  return valid;
}

// Validates the Courses Delete form (course ID only).
// Returns true if valid, false otherwise.
function validate_courses_delete_form() {
  View.clear_all_errors();
  let valid = true;

  const id_input = document.getElementById("courses-id");
  const course_id = id_input ? id_input.value.trim() : "";

  const course_id_pattern = /^[A-Z]{2,6}\s+\d{3,4}$/;
  if (!course_id) {
    View.show_field_error(id_input, "Course ID is required.");
    valid = false;
  } else if (!course_id_pattern.test(course_id)) {
    View.show_field_error(id_input, "Course ID must be in the format: CMSC 420 (uppercase letters, space, then 3-4 digits).");
    valid = false;
  }

  return valid;
}

// Validates the Labs Add/Modify/Delete form (name only).
// Returns true if valid, false otherwise.
function validate_labs_form() {
  View.clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("labs-name");
  const name = name_input ? name_input.value.trim() : "";

  if (!name) {
    View.show_field_error(name_input, "Lab name is required.");
    valid = false;
  } else if (name.length > 64) {
    View.show_field_error(name_input, "Lab name must be 64 characters or fewer.");
    valid = false;
  }

  return valid;
}

// Validates the time-range sub-form fields.
// Returns true if all fields are valid, false if errors were shown.
function validate_time_range_form() {
  View.clear_all_errors();
  let valid = true;
  const time_pattern = /^([01]\d|2[0-3]):[0-5]\d$/;

  const start_input = document.getElementById("ts-start");
  const spacing_input = document.getElementById("ts-spacing");
  const end_input = document.getElementById("ts-end");

  if (start_input) {
    const v = start_input.value.trim();
    if (!v) { View.show_field_error(start_input, "Start time is required."); valid = false; }
    else if (!time_pattern.test(v)) { View.show_field_error(start_input, "Start time must be HH:MM (e.g. 08:00)."); valid = false; }
  }
  if (spacing_input) {
    const v = spacing_input.value.trim();
    if (!v || parseInt(v) <= 0 || !Number.isInteger(parseFloat(v))) {
      View.show_field_error(spacing_input, "Spacing must be a positive whole number of minutes."); valid = false;
    }
  }
  if (end_input) {
    const v = end_input.value.trim();
    if (!v) { View.show_field_error(end_input, "End time is required."); valid = false; }
    else if (!time_pattern.test(v)) { View.show_field_error(end_input, "End time must be HH:MM (e.g. 17:00)."); valid = false; }
  }
  return valid;
}

// Validates the class-pattern sub-form fields.
// Returns true if all fields are valid, false if errors were shown.
function validate_class_pattern_form() {
  View.clear_all_errors();
  let valid = true;

  const credits_input = document.getElementById("ts-credits");
  if (credits_input) {
    const v = credits_input.value.trim();
    if (!v || parseInt(v) < 1 || !Number.isInteger(parseFloat(v))) {
      View.show_field_error(credits_input, "Credits must be a positive whole number."); valid = false;
    }
  }

  const day_sels = [...document.querySelectorAll('[name="ts-meeting-day"]')];
  const dur_inputs = [...document.querySelectorAll('[name="ts-meeting-duration"]')];

  if (day_sels.length === 0) {
    if (credits_input) View.show_field_error(credits_input, "At least one meeting is required.");
    valid = false;
  }

  day_sels.forEach((sel, i) => {
    if (!sel.value) { View.show_field_error(sel, "Day is required."); valid = false; }
    const dur = dur_inputs[i];
    if (dur) {
      const v = dur.value.trim();
      if (!v || parseInt(v) <= 0 || !Number.isInteger(parseFloat(v))) {
        View.show_field_error(dur, "Duration must be a positive whole number of minutes."); valid = false;
      }
    }
  });

  return valid;
}

// Validates the Rooms Add/Modify/Delete form (name only).
// Returns true if valid, false otherwise.
function validate_rooms_form() {
  View.clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("rooms-name");
  const name = name_input ? name_input.value.trim() : "";
  const room_pattern = /^[A-Za-z][\w\s\-]*$/;

  if (!name) {
    View.show_field_error(name_input, "Room name is required.");
    valid = false;
  } else if (!room_pattern.test(name)) {
    View.show_field_error(name_input, "Room name must start with a letter and contain only letters, numbers, spaces, or hyphens.");
    valid = false;
  }

  return valid;
}

// ---------------------------------------------------------------------------
// Response error helper
// ---------------------------------------------------------------------------

// Returns the identifying input element for the current field (used for error display).
function get_current_id_input() {
  if (Model.current_field === "Faculty") return document.getElementById("faculty-name");
  if (Model.current_field === "Courses") return document.getElementById("courses-id");
  if (Model.current_field === "Labs") return document.getElementById("labs-name");
  if (Model.current_field === "Rooms") return document.getElementById("rooms-name");
  if (Model.current_field === "Time Slots") {
    return document.getElementById("ts-start") || document.getElementById("ts-credits");
  }
  return null;
}

// Reads the response body text, extracts any error message, and displays it inline.
// Returns true if an error was shown, false if the operation can proceed.
// Parameters: res - the fetch Response object, fallback - shown if body has no error
async function check_response_error(res, fallback) {
  const input_el = get_current_id_input();

  let raw_text = "";
  try {
    raw_   = await res.text();
  } catch (_) {
    View.show_field_error(input_el, fallback);
    return true;
  }

  let message = null;
  try {
    const body = JSON.parse(raw_text);
    if (body && typeof body.error === "string" && body.error.trim() !== "") {
      message = body.error;
    } else if (body && typeof body.message === "string" && body.message.trim() !== "") {
      message = body.message;
    }
  } catch (_) {
    if (raw_text.trim() !== "") message = raw_text.trim();
  }

  if (message) {
    View.show_field_error(input_el, message);
    return true;
  }

  if (!res.ok) {
    View.show_field_error(input_el, fallback);
    return true;
  }

  return false;
}

// ---------------------------------------------------------------------------
// Navigation history helpers
// ---------------------------------------------------------------------------

// Navigates to new content by pushing the current view onto the back stack.
// Clears the forward stack on new navigation. Updates button images.
// Parameters: field - field name string
function navigate_to(field) {
  if (Model.current_content !== field) {
    Model.push_back_stack(NavigationOriginator.save());
    Model.set_current_content(field);
    Model.clear_forward_stack();
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
}

// Navigates directly to the given field by fetching and rendering its data.
// Passing null clears the view and disables action buttons.
// Parameters: field - field name string or null
async function go_to_field(field) {
  if (field === null) {
    View.render_navigator_empty();
    Model.set_current_field(null);
    View.render_amd_images(null);
  }
  else if (field === "Faculty") await load_faculty();
  else if (field === "Courses") await load_courses();
  else if (field === "Labs") await load_labs();
  else if (field === "Rooms") await load_rooms();
  else if (field === "Schedule") await load_schedule();
  else if (field === "Time Slots") await load_time_slots();
}

// ---------------------------------------------------------------------------
// Load field methods
// ---------------------------------------------------------------------------

// Fetches the faculty list from the API and renders it in the navigator.
async function load_faculty() {
  const faculty = await Model.api_get_faculty();
  View.render_faculty_list(faculty);
  Model.set_selected_item_data(null);
  View.render_amd_images(Model.current_field, false);
  attach_list_item_listeners();
  navigate_to("Faculty");
}

// Fetches the courses list from the API and renders it in the navigator.
async function load_courses() {
  try {
    const courses = await Model.api_get_courses();
    View.render_courses_list(courses);
    Model.set_selected_item_data(null);
    View.render_amd_images(Model.current_field, false);
    attach_list_item_listeners();
    navigate_to("Courses");
  } catch (err) {
    View.render_load_error("courses", err.message);
    navigate_to("Courses");
  }
}

// Fetches the rooms list from the API and renders it in the navigator.
async function load_rooms() {
  try {
    const rooms = await Model.api_get_rooms();
    View.render_rooms_list(rooms);
    Model.set_selected_item_data(null);
    View.render_amd_images(Model.current_field, false);
    attach_list_item_listeners();
    navigate_to("Rooms");
  } catch (err) {
    View.render_load_error("rooms", err.message);
    navigate_to("Rooms");
  }
}

// Fetches the labs list from the API and renders it in the navigator.
async function load_labs() {
  try {
    const labs = await Model.api_get_labs();
    View.render_labs_list(labs);
    Model.set_selected_item_data(null);
    View.render_amd_images(Model.current_field, false);
    attach_list_item_listeners();
    navigate_to("Labs");
  } catch (err) {
    View.render_load_error("labs", err.message);
    navigate_to("Labs");
  }
}

// Attaches click listeners to each rendered list item.
// On click: selects the item, stores its data, and enables Modify/Delete buttons.
function attach_list_item_listeners() {
  document.querySelectorAll(".navigator-item").forEach(li => {
    li.addEventListener("click", () => {
      const idx = parseInt(li.dataset.index);
      const item = View.get_list_item(idx);
      if (!item) return;
      View.select_list_item(li);
      Model.set_selected_item_data({ ...item, _list_index: idx });
      View.render_amd_images(Model.current_field, true);
    });
  });
}

// Fetches the time slot configuration from the API and renders it in the navigator.
async function load_time_slots() {
  try {
    const data = await Model.api_get_time_slots();
    View.render_time_slots_list(data);
    Model.set_selected_item_data(null);
    View.render_amd_images(Model.current_field, false);
    attach_list_item_listeners();
    navigate_to("Time Slots");
  } catch (err) {
    View.render_load_error("time slots", err.message);
    navigate_to("Time Slots");
  }
}

// Renders the schedule generator form and wires the Generate button.
async function load_schedule() {
  View.render_schedule_form();
  document.getElementById("generate-schedules").addEventListener("click", generate_schedules);
  navigate_to("Schedule");
}

// ---------------------------------------------------------------------------
// Schedule generation
// ---------------------------------------------------------------------------

// Reads the schedule-count and optimize inputs, calls the scheduler API,
// then updates the status area with the result count or an error message.
// Switches the model out of CSV mode so any loaded CSV is replaced by the new results.
async function generate_schedules() {
  const count = parseInt(document.getElementById("schedule-count").value);
  const optimize = document.getElementById("schedule-optimize").checked;

  // New generation replaces any previously-loaded CSV
  Model.set_csv_mode(false);
  Model.set_csv_schedules([]);

  View.render_schedule_status(count, optimize, "Creating schedules...");
  View.render_progress_bar(count, "Creating schedules...");
  document.getElementById("generate-schedules").addEventListener("click", generate_schedules);

  const res = await Model.api_run_scheduler(count, optimize);
  const data = await res.json();

  let status_message;
  if (data.error || data.count === undefined) {
    status_message = "Config file is empty, cannot generate schedules, please load a config file.";
  } else if (data.count === 0) {
    status_message = "No valid schedules. Please modify config.";
  } else {
    Model.set_schedules_generated(true);
    status_message = data.count + " schedules generated.";
    View.render_schedules_generated_buttons();
  }

  View.render_schedule_status(count, optimize, status_message);
  View.render_progress_bar(count, status_message);
  document.getElementById("generate-schedules").addEventListener("click", generate_schedules);
}

// ---------------------------------------------------------------------------
// Schedule viewer
// ---------------------------------------------------------------------------

// Opens the inline schedule viewer starting at the given schedule index.
// Handles both API-backed schedules (generated by the backend) and CSV-loaded
// schedules (parsed client-side), choosing the correct data source automatically.
// Parameters: index - 0-based index of the first schedule to display
async function view_schedule(index = 0) {
  let current_index = index;
  let current_mode = "faculty";

  // When viewing a loaded CSV, use the local parser instead of the backend API.
  const schedule_count = Model.csv_mode ? Model.csv_schedules.length : null;

  const refresh = async () => {
    const data = Model.csv_mode
      ? Model.get_csv_schedule_view(current_index, current_mode)
      : await Model.api_get_schedule_view(current_index, current_mode);
    if (data.error) {
      alert(data.error);
      return;
    }
    View.render_schedule_calendar(data, current_index, current_mode);
  };

  View.render_schedule_view_inline(
    index,
    (new_index) => {
      current_index = new_index;
      refresh();
    },
    (new_mode) => {
      current_mode = new_mode;
      refresh();
    },
    schedule_count
  );

  await refresh();
}

// ---------------------------------------------------------------------------
// Shared form helpers
// ---------------------------------------------------------------------------

// Checks all elements with the given name attr for duplicate values.
// Highlights the second occurrence and returns false if a duplicate is found.
function check_select_duplicates(name_attr, label) {
  const elements = [...document.querySelectorAll(`[name="${name_attr}"]`)];
  const seen = new Map();
  for (const el of elements) {
    const v = el.value.trim();
    if (!v) continue;
    if (seen.has(v)) {
      View.show_field_error(el, `Duplicate ${label}: "${v}" is already selected above.`);
      return false;
    }
    seen.set(v, el);
  }
  return true;
}

// ---------------------------------------------------------------------------
// Faculty form helpers
// ---------------------------------------------------------------------------

// Reads all faculty form fields from the popup and returns a data object.
// Deduplicates multi-select fields; returns null and shows an error if duplicates found.
function read_faculty_form_fields() {
  const max_credits = parseInt(document.getElementById("faculty-max-credits")?.value) || 0;
  const min_credits = parseInt(document.getElementById("faculty-min-credits")?.value) || 0;
  const unique_limit = parseInt(document.getElementById("faculty-unique-course-limit")?.value) || 1;
  const max_days = parseInt(document.getElementById("faculty-max-days")?.value) || 4;

  // Parse time slots: "DAY HH:MM-HH:MM" → { DAY: ["HH:MM-HH:MM", ...] }
  const times = {};
  document.querySelectorAll('input[name="faculty-time-slot"]').forEach(input => {
    const val = input.value.trim();
    if (!val) return;
    const space = val.indexOf(" ");
    if (space < 0) return;
    const day = val.slice(0, space).toUpperCase();
    const range = val.slice(space + 1);
    if (!times[day]) times[day] = [];
    times[day].push(range);
  });

  function read_select_values(name) {
    return [...document.querySelectorAll(`[name="${name}"]`)]
      .map(el => el.value.trim())
      .filter(v => v !== "");
  }

  const course_prefs = read_select_values("faculty-course-preference");
  const room_prefs = read_select_values("faculty-room-preference");
  const lab_prefs = read_select_values("faculty-lab-preference");
  const mand_days = read_select_values("faculty-mandatory-day");

  View.clear_all_errors();
  if (!check_select_duplicates("faculty-course-preference", "course preference")) return null;
  if (!check_select_duplicates("faculty-room-preference", "room preference")) return null;
  if (!check_select_duplicates("faculty-lab-preference", "lab preference")) return null;
  if (!check_select_duplicates("faculty-mandatory-day", "mandatory day")) return null;

  const course_preferences = Object.fromEntries(course_prefs.map(c => [c, 1]));
  const room_preferences = Object.fromEntries(room_prefs.map(r => [r, 1]));
  const lab_preferences = Object.fromEntries(lab_prefs.map(l => [l, 1]));

  return {
    maximum_credits: max_credits,
    minimum_credits: min_credits,
    unique_course_limit: unique_limit,
    maximum_days: max_days,
    times,
    course_preferences,
    room_preferences,
    lab_preferences,
    mandatory_days: mand_days,
  };
}

// ---------------------------------------------------------------------------
// Popup save handler
// ---------------------------------------------------------------------------

// Dispatches the popup Save button click to the correct API call based on
// the current field and operation (add / modify / delete).
// Validates form inputs first; exits early and shows inline errors on failure.
// After each successful mutation a Command is pushed onto command_history so
// the Undo / Redo buttons can reverse or replay the action.
async function handle_popup_save() {
  console.log("SAVE CLICKED", Model.current_field, Model.current_operation);

  if (Model.current_field === "Faculty") {

    if (Model.current_operation === "add" && !validate_faculty_form(true)) return;
    if (Model.current_operation === "modify" && !validate_faculty_form(false)) return;
    if (Model.current_operation === "delete" && !validate_faculty_delete_form()) return;

    const name = document.getElementById("faculty-name").value.trim();

    if (Model.current_operation === "add") {

      const fields = read_faculty_form_fields();
      if (!fields) return;
      const data = { name, ...fields };

      const add_res = await Model.api_add_faculty(data);
      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

      command_history.push({
        label: `Add Faculty "${name}"`,
        field: "Faculty",
        execute: async () => { await Model.api_add_faculty(data); },
        unexecute: async () => { await Model.api_delete_faculty(name); },
      });

    } else if (Model.current_operation === "delete") {

      const del_res = await Model.api_delete_faculty(name);
      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

      // Take snapshot of record so it can be restored on undo.
      const snapshot = Model.selected_item_data ? { ...Model.selected_item_data } : { name };
      command_history.push({
        label: `Delete Faculty "${name}"`,
        field: "Faculty",
        execute: async () => { await Model.api_delete_faculty(name); },
        unexecute: async () => { await Model.api_add_faculty(snapshot); },
      });

    } else if (Model.current_operation === "modify") {

      const fields = read_faculty_form_fields();
      if (!fields) return;
      const new_data = { name, ...fields };
      const original_name = Model.selected_item_data ? Model.selected_item_data.name : name;
      const old_data = Model.selected_item_data ? { ...Model.selected_item_data } : null;

      const mod_res = await Model.api_modify_faculty(original_name, new_data);
      if (await check_response_error(mod_res, `"${original_name}" was not found. Please check the name and try again.`)) return;

      command_history.push({
        label: `Modify Faculty "${original_name}"`,
        field: "Faculty",
        execute: async () => { await Model.api_modify_faculty(original_name, new_data); },
        unexecute: async () => {
          if (old_data) await Model.api_modify_faculty(name, old_data);
        },
      });
    }

    View.render_undo_redo_state(command_history);
    await load_faculty();

  } else if (Model.current_field === "Courses") {
    if (Model.current_operation === "add" && !validate_courses_form(true)) return;
    if (Model.current_operation === "modify" && !validate_courses_form(false)) return;
    if (Model.current_operation === "delete" && !validate_courses_delete_form()) return;

    const id_input = document.getElementById("courses-id");

    if (!id_input) {
      console.error("Course ID input not found");
      return;
    }

    const course_id = id_input.value.trim();

    const credits_input = document.getElementById("courses-credits");
    const credits = credits_input ? parseInt(credits_input.value) : null;

    const rooms = [...document.querySelectorAll('[name="courses-room"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const labs = [...document.querySelectorAll('[name="courses-lab"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const conflicts = [...document.querySelectorAll('[name="courses-conflict"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const faculty = [...document.querySelectorAll('[name="courses-faculty"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    View.clear_all_errors();
    if (!check_select_duplicates("courses-room", "room")) return;
    if (!check_select_duplicates("courses-lab", "lab")) return;
    if (!check_select_duplicates("courses-conflict", "conflict")) return;
    if (!check_select_duplicates("courses-faculty", "faculty")) return;

    const course_data = { course_id, credits, room: rooms, lab: labs, conflicts, faculty };

    if (Model.current_operation === "add") {
      const add_res = await Model.api_add_course(course_data);
      if (await check_response_error(add_res, `"${course_id}" could not be added.`)) return;

      command_history.push({
        label: `Add Course "${course_id}"`,
        field: "Courses",
        execute: async () => { await Model.api_add_course(course_data); },
        unexecute: async () => { await Model.api_delete_course(course_id); },
      });

    } else if (Model.current_operation === "delete") {
      const del_res = await Model.api_delete_course(course_id);
      if (await check_response_error(del_res, `"${course_id}" was not found. Please check the course ID and try again.`)) return;

      const snapshot = Model.selected_item_data ? { ...Model.selected_item_data } : course_data;
      const snap_index = Model.selected_item_data?._list_index ?? null;
      command_history.push({
        label: `Delete Course "${course_id}"`,
        field: "Courses",
        execute: async () => { await Model.api_delete_course(course_id); },
        unexecute: async () => { await Model.api_add_course(snapshot); },
      });

    } else if (Model.current_operation === "modify") {
      const index = Model.selected_item_data?._list_index ?? null;
      if (index === null) {
        View.show_field_error(id_input, "No course selected. Please click a course from the list first.");
        return;
      }
      const old_data = Model.selected_item_data ? { ...Model.selected_item_data } : null;

      const mod_res = await Model.api_modify_course(index, course_data);
      if (await check_response_error(mod_res, `"${course_id}" could not be modified.`)) return;

      command_history.push({
        label: `Modify Course "${course_id}"`,
        field: "Courses",
        execute: async () => { await Model.api_modify_course(index, course_data); },
        unexecute: async () => {
          if (old_data) await Model.api_modify_course(index, old_data);
        },
      });
    }

    View.render_undo_redo_state(command_history);
    await load_courses();

  } else if (Model.current_field === "Labs") {
    const name_input = document.getElementById("labs-name");

    if (!name_input) {
      console.error("Lab name input not found");
      return;
    }

    const name = name_input.value.trim();

    if (Model.current_operation === "add") {
      if (!validate_labs_form()) return;

      const add_res = await Model.api_add_lab(name);
      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

      command_history.push({
        label: `Add Lab "${name}"`,
        field: "Labs",
        execute: async () => { await Model.api_add_lab(name); },
        unexecute: async () => { await Model.api_delete_lab(name); },
      });

    } else if (Model.current_operation === "delete") {
      if (!validate_labs_form()) return;

      const del_res = await Model.api_delete_lab(name);
      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

      command_history.push({
        label: `Delete Lab "${name}"`,
        field: "Labs",
        execute: async () => { await Model.api_delete_lab(name); },
        unexecute: async () => { await Model.api_add_lab(name); },
      });

    } else if (Model.current_operation === "modify") {
      if (!name) {
        View.show_field_error(name_input, "Current lab name is required.");
        return;
      }

      const new_name_input = document.getElementById("labs-new-name");
      const new_name = new_name_input ? new_name_input.value.trim() : "";

      if (!new_name) {
        View.show_field_error(new_name_input, "New lab name is required.");
        return;
      }

      const mod_res = await Model.api_modify_lab(name, new_name);
      if (await check_response_error(mod_res, `"${name}" was not found. Please check the name and try again.`)) return;

      command_history.push({
        label: `Rename Lab "${name}" â†’ "${new_name}"`,
        field: "Labs",
        execute: async () => { await Model.api_modify_lab(name, new_name); },
        unexecute: async () => { await Model.api_modify_lab(new_name, name); },
      });
    }

    View.render_undo_redo_state(command_history);
    await load_labs();

  } else if (Model.current_field === "Rooms") {
    const name_input = document.getElementById("rooms-name");

    if (!name_input) {
      console.error("Room name input not found");
      return;
    }

    const name = name_input.value.trim();

    if (Model.current_operation === "add") {
      if (!validate_rooms_form()) return;

      const add_res = await Model.api_add_room(name);
      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

      command_history.push({
        label: `Add Room "${name}"`,
        field: "Rooms",
        execute: async () => { await Model.api_add_room(name); },
        unexecute: async () => { await Model.api_delete_room(name); },
      });

    } else if (Model.current_operation === "delete") {
      if (!validate_rooms_form()) return;

      const del_res = await Model.api_delete_room(name);
      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

      command_history.push({
        label: `Delete Room "${name}"`,
        field: "Rooms",
        execute: async () => { await Model.api_delete_room(name); },
        unexecute: async () => { await Model.api_add_room(name); },
      });

    } else if (Model.current_operation === "modify") {
      if (!name) {
        View.show_field_error(name_input, "Current room name is required.");
        return;
      }

      const new_name_input = document.getElementById("rooms-new-name");
      const new_name = new_name_input ? new_name_input.value.trim() : "";

      if (!new_name) {
        View.show_field_error(new_name_input, "New room name is required.");
        return;
      }

      const mod_res = await Model.api_modify_room(name, new_name);
      if (await check_response_error(mod_res, `"${name}" was not found. Please check the name and try again.`)) return;

      command_history.push({
        label: `Rename Room "${name}" â†’ "${new_name}"`,
        field: "Rooms",
        execute: async () => { await Model.api_modify_room(name, new_name); },
        unexecute: async () => { await Model.api_modify_room(new_name, name); },
      });
    }

    View.render_undo_redo_state(command_history);
    await load_rooms();

  } else if (Model.current_field === "Time Slots") {
    if (Model.current_operation === "add") {
      const type_sel = document.getElementById("ts-add-type");
      const add_type = type_sel ? type_sel.value : "time";

      if (add_type === "time") {
        if (!validate_time_range_form()) return;

        const day = document.getElementById("ts-day")?.value || "";
        const start = document.getElementById("ts-start")?.value.trim() || "";
        const spacing = parseInt(document.getElementById("ts-spacing")?.value) || 0;
        const end = document.getElementById("ts-end")?.value.trim() || "";
        const time_data = { day, start, spacing, end };

        const res = await Model.api_add_time_range(time_data);
        if (await check_response_error(res, "Time range could not be added.")) return;

        const ts_after = await Model.api_get_time_slots();
        const day_ranges = ts_after?.times?.[day] ?? [];
        const new_index = day_ranges.length - 1;
        command_history.push({
          label: `Add Time Range (${day} ${start}â€“${end})`,
          field: "Time Slots",
          execute: async () => { await Model.api_add_time_range(time_data); },
          unexecute: async () => { await Model.api_delete_time_range(day, new_index); },
        });

      } else {
        if (!validate_class_pattern_form()) return;

        const credits = parseInt(document.getElementById("ts-credits")?.value) || 0;
        const start_time = document.getElementById("ts-class-start-time")?.value.trim() || null;
        const disabled = document.getElementById("ts-disabled")?.checked || false;

        const day_sels = [...document.querySelectorAll('[name="ts-meeting-day"]')];
        const dur_inputs = [...document.querySelectorAll('[name="ts-meeting-duration"]')];
        const lab_cbs = [...document.querySelectorAll('[name="ts-meeting-lab"]')];

        const meetings = day_sels.map((sel, i) => ({
          day: sel.value,
          duration: parseInt(dur_inputs[i]?.value) || 0,
          lab: lab_cbs[i]?.checked || false
        })).filter(m => m.day && m.duration > 0);

        const pattern_data = { credits, meetings, start_time: start_time || null, disabled };

        const res = await Model.api_add_class_pattern(pattern_data);
        if (await check_response_error(res, "Class pattern could not be added.")) return;

        const ts_after = await Model.api_get_time_slots();
        const new_index = (ts_after?.classes?.length ?? 1) - 1;
        command_history.push({
          label: `Add Class Pattern (${credits} credits)`,
          field: "Time Slots",
          execute: async () => { await Model.api_add_class_pattern(pattern_data); },
          unexecute: async () => { await Model.api_delete_class_pattern(new_index); },
        });
      }

    } else if (Model.current_operation === "modify") {
      const item = Model.selected_item_data;
      if (!item) return;

      if (item._type === "time") {
        if (!validate_time_range_form()) return;

        const start = document.getElementById("ts-start")?.value.trim() || "";
        const spacing = parseInt(document.getElementById("ts-spacing")?.value) || 0;
        const end = document.getElementById("ts-end")?.value.trim() || "";
        const new_time_data = { start, spacing, end };
        const old_time_data = { start: item.start, spacing: item.spacing, end: item.end };

        const res = await Model.api_modify_time_range(item._day, item._index, new_time_data);
        if (await check_response_error(res, "Time range could not be modified.")) return;

        command_history.push({
          label: `Modify Time Range (${item._day})`,
          field: "Time Slots",
          execute: async () => { await Model.api_modify_time_range(item._day, item._index, new_time_data); },
          unexecute: async () => { await Model.api_modify_time_range(item._day, item._index, old_time_data); },
        });

      } else {
        if (!validate_class_pattern_form()) return;

        const credits = parseInt(document.getElementById("ts-credits")?.value) || 0;
        const start_time = document.getElementById("ts-class-start-time")?.value.trim() || null;
        const disabled = document.getElementById("ts-disabled")?.checked || false;

        const day_sels = [...document.querySelectorAll('[name="ts-meeting-day"]')];
        const dur_inputs = [...document.querySelectorAll('[name="ts-meeting-duration"]')];
        const lab_cbs = [...document.querySelectorAll('[name="ts-meeting-lab"]')];

        const meetings = day_sels.map((sel, i) => ({
          day: sel.value,
          duration: parseInt(dur_inputs[i]?.value) || 0,
          lab: lab_cbs[i]?.checked || false
        })).filter(m => m.day && m.duration > 0);

        const new_pattern_data = { credits, meetings, start_time: start_time || null, disabled };
        const old_pattern_data = {
          credits: item.credits,
          meetings: item.meetings,
          start_time: item.start_time || null,
          disabled: item.disabled || false,
        };

        const res = await Model.api_modify_class_pattern(item._index, new_pattern_data);
        if (await check_response_error(res, "Class pattern could not be modified.")) return;

        command_history.push({
          label: `Modify Class Pattern (${credits} credits)`,
          field: "Time Slots",
          execute: async () => { await Model.api_modify_class_pattern(item._index, new_pattern_data); },
          unexecute: async () => { await Model.api_modify_class_pattern(item._index, old_pattern_data); },
        });
      }
    }

    View.render_undo_redo_state(command_history);
    await load_time_slots();
  }
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

// Reads a selected file into the model's loaded_file_content state.
// Called by the file input's onchange handler in index.html.
// Parameters: input - the file <input> DOM element
function load_file_content(input) {
  let file_types = ['json', 'csv'];
  let file_reader = new FileReader();
  file_reader.onload = function () {
    // PUT FETCH IN HERE
    Model.set_loaded_file_content(file_reader.result);
  };
  file_reader.readAsText(input.files[0]);
}

// ---------------------------------------------------------------------------
// Event listeners
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", async () => {
  await Model.api_load_empty_config();
  View.config_name.textContent = "Config loaded: empty.json";
  View.render_undo_redo_state(command_history);
});

View.faculty_button.addEventListener("click", () => {
  Model.set_current_field("Faculty");
  load_faculty();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "540px";
  View.popup_box.style.width = "500px";
});

View.courses_button.addEventListener("click", () => {
  Model.set_current_field("Courses");
  load_courses();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "540px";
  View.popup_box.style.width = "500px";
  View.popup_header.style.width = "495px";
});

View.labs_button.addEventListener("click", () => {
  Model.set_current_field("Labs");
  load_labs();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "540px";
  View.popup_box.style.width = "500px";
  View.popup_header.style.width = "495px";
});

View.rooms_button.addEventListener("click", () => {
  Model.set_current_field("Rooms");
  load_rooms();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "540px";
  View.popup_box.style.width = "500px";
  View.popup_header.style.width = "495px";
});

View.schedule_button.addEventListener("click", () => {
  Model.set_current_field("Schedule");
  load_schedule();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "605px";
  View.popup_box.style.width = "600px";
  View.popup_header.style.width = "595px";
});

View.time_slots_button.addEventListener("click", () => {
  Model.set_current_field("Time Slots");
  load_time_slots();
  View.render_amd_images(Model.current_field);
  View.popup_form.style.height = "540px";
  View.popup_box.style.width = "500px";
  View.popup_header.style.width = "495px";
});

// Back button
View.back_button.addEventListener("click", async () => {
  if (Model.back_stack.length > 0) {
    Model.push_forward_stack(NavigationOriginator.save());
    NavigationOriginator.restore(Model.pop_back_stack());
    await go_to_field(Model.current_content);
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
});

// Forward button
View.forward_button.addEventListener("click", async () => {
  if (Model.forward_stack.length > 0) {
    Model.push_back_stack(NavigationOriginator.save());
    NavigationOriginator.restore(Model.pop_forward_stack());
    await go_to_field(Model.current_content);
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
});

// Undo button: undoes the most-recently done mutation.
View.undo_button.addEventListener("click", async () => {
  const cmd = await command_history.undo();
  if (!cmd) return;
  await go_to_field(cmd.field);
  View.render_undo_redo_state(command_history);
});

// Redo button: redoes the most-recently undone mutation.
View.redo_button.addEventListener("click", async () => {
  const cmd = await command_history.redo();
  if (!cmd) return;
  await go_to_field(cmd.field);
  View.render_undo_redo_state(command_history);
});

// View button: allows viewing of schedules.
View.view_button.addEventListener("click", () => {
  if (!Model.schedules_generated) return;
  view_schedule(0);
});

// ---------------------------------------------------------------------------
// Save button functionality
// ---------------------------------------------------------------------------

// Save schedule as JSON
View.save_button.addEventListener("click", async (e) => {
  e.preventDefault();  // stops redirect / form submit

  const config = await Model.api_save_config();

  const blob = new Blob(
    [JSON.stringify(config, null, 2)],
    { type: "application/json" }
  );

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "schedule_config.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

// Save schedule as CSV
View.save_csv.addEventListener("click", async (e) => {
  e.preventDefault();
  if (!Model.schedules_generated) return;

  let csvText;

  if (Model.csv_mode) {
    // Reconstruct CSV from the in-memory parsed schedules
    const sections = Model.csv_schedules.map((schedule, i) => {
      const rows = schedule.map(entry => {
        const course_section = `${entry.course_id}.${entry.section}`;
        const meetings = entry.meetings.map(m =>
          `${m.day} ${m.time_range}${m.is_lab ? "^" : ""}`
        );
        return [course_section, entry.faculty, entry.room, entry.lab, ...meetings].join(",");
      });
      return [`Schedule ${i + 1}:`, ...rows].join("\n");
    });
    csvText = sections.join("\n\n");
  } else {
    // Fetch all generated schedules from the backend
    const res = await fetch("/schedule/export_csv");
    if (!res.ok) return;
    csvText = await res.text();
  }

  const blob = new Blob([csvText], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "schedules.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

// ---------------------------------------------------------------------------
// Load button functionality
// ---------------------------------------------------------------------------

// Load file input
View.file_input.addEventListener("change", async function () {
  const file = View.file_input.files[0];
  if (!file) return;

  const ext = file.name.split(".").pop().toLowerCase();

  if (ext === "csv") {
    // Load a previously-exported CSV schedule
    const text = await file.text();
    const schedules = Model.parse_csv_schedules(text);

    if (schedules.length === 0) {
      View.config_name.textContent = "⚠ No schedules found in the CSV file.";
      return;
    }

    Model.set_csv_schedules(schedules);
    Model.set_csv_mode(true);
    Model.set_schedules_generated(true);
    View.render_schedules_generated_buttons();

    const timestamp = new Date().toLocaleTimeString();
    const label = schedules.length === 1 ? "1 schedule" : `${schedules.length} schedules`;
    View.config_name.textContent = `✔ Schedule loaded: "${file.name}" (${label}) at ${timestamp}`;
    View.config_name.classList.remove("visible");
    void View.config_name.offsetWidth;
    View.config_name.classList.add("visible");

  } else {
    // Load a JSON config file
    Model.set_csv_mode(false);

    const res = await Model.api_load_config(file);
    const data = await res.json();
    console.log(data);

    if (res.ok) {
      View.faculty_button.disabled = false;
      View.courses_button.disabled = false;
      View.labs_button.disabled = false;
      View.rooms_button.disabled = false;
      View.schedule_button.disabled = false;
      View.time_slots_button.disabled = false;
      View.view_button.disabled = false;

      // New config means prior undo/redo history no longer applies.
      command_history.clear();
      View.render_undo_redo_state(command_history);

      const timestamp = new Date().toLocaleTimeString();
      View.config_name.textContent = `✔ Config loaded: "${file.name}" at ${timestamp}`;
      View.config_name.classList.remove("visible");
      void View.config_name.offsetWidth;
      View.config_name.classList.add("visible");
    }
  }
});

// Fetches rooms, labs, course IDs, and faculty names to populate course dropdowns.
async function get_course_options() {
  const [rooms, labs, courses, faculty] = await Promise.all([
    Model.api_get_rooms().catch(() => []),
    Model.api_get_labs().catch(() => []),
    Model.api_get_courses().catch(() => []),
    Model.api_get_faculty().catch(() => []),
  ]);
  return {
    rooms: rooms.map(r => r.name),
    labs: labs.map(l => l.name),
    courses: courses.map(c => c.course_id),
    faculty: faculty.map(f => f.name),
  };
}

// ---------------------------------------------------------------------------
// Add/Modify/Delete buttons functionality
// ---------------------------------------------------------------------------

// Add button: sets current_operation and opens the Add popup for the active field.
View.add_button.addEventListener("click", async () => {
  Model.set_current_operation("add");
  View.focus_field_button(Model.current_field);
  if (Model.current_field === "Time Slots") {
    View.render_add_time_slots_popup();
    return;
  }
  const needs_opts = Model.current_field === "Courses" || Model.current_field === "Faculty";
  const options = needs_opts ? await get_course_options() : null;
  View.render_edit_popup("Add", Model.current_field, null, options);
});

// Modify button: opens Modify popup pre-populated with the selected item's data.
View.modify_button.addEventListener("click", async () => {
  if (!Model.selected_item_data) return;
  Model.set_current_operation("modify");
  View.focus_field_button(Model.current_field);
  if (Model.current_field === "Time Slots") {
    View.render_modify_time_slots_popup(Model.selected_item_data);
    return;
  }
  const needs_opts = Model.current_field === "Courses" || Model.current_field === "Faculty";
  const options = needs_opts ? await get_course_options() : null;
  View.render_edit_popup("Modify", Model.current_field, Model.selected_item_data, options);
});

// Delete button: directly deletes the selected item without opening a popup.
View.delete_button.addEventListener("click", async () => {
  if (!Model.selected_item_data) return;
  Model.set_current_operation("delete");

  const field = Model.current_field;
  const item = Model.selected_item_data;

  if (field === "Faculty") {

    const snapshot = { ...item };

    const res = await Model.api_delete_faculty(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
   
    command_history.push({
      label: `Delete Faculty "${item.name}"`,
      field: "Faculty",
      execute: async () => { await Model.api_delete_faculty(snapshot.name); },
      unexecute: async () => { await Model.api_add_faculty(snapshot); },
    });

    View.render_undo_redo_state(command_history);
    await load_faculty();

  } else if (field === "Courses") {

    const snapshot = { ...item };

    const res = await Model.api_delete_course(item.course_id);
    if (await check_response_error(res, `"${item.course_id}" could not be deleted.`)) return;
    
    command_history.push({
      label: `Delete Course "${item.course_id}"`,
      field: "Courses",
      execute: async () => { await Model.api_delete_course(snapshot.course_id); },
      unexecute: async () => { await Model.api_add_course(snapshot); },
    });

    View.render_undo_redo_state(command_history);
    await load_courses();

  } else if (field === "Labs") {

    const res = await Model.api_delete_lab(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
    
    command_history.push({
      label: `Delete Lab "${item.name}"`,
      field: "Labs",
      execute: async () => { await Model.api_delete_lab(item.name); },
      unexecute: async () => { await Model.api_add_lab(item.name); },
    });
    
    View.render_undo_redo_state(command_history);
    await load_labs();
  
  } else if (field === "Rooms") {

    const res = await Model.api_delete_room(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
    
    command_history.push({
      label: `Delete Room "${item.name}"`,
      field: "Rooms",
      execute: async () => { await Model.api_delete_room(item.name); },
      unexecute: async () => { await Model.api_add_room(item.name); },
    });
    
    View.render_undo_redo_state(command_history);
    await load_rooms();
  
  } else if (field === "Time Slots") {

    if (item._type === "time") {
      const snapshot = { day: item._day, index: item._index, start: item.start, spacing: item.spacing, end: item.end };
      
      const res = await Model.api_delete_time_range(item._day, item._index);
      if (await check_response_error(res, "Time range could not be deleted.")) return;
     
      command_history.push({
        label: `Delete Time Range (${snapshot.day})`,
        field: "Time Slots",
        execute: async () => { await Model.api_delete_time_range(snapshot.day, snapshot.index); },
        unexecute: async () => {
          await Model.api_add_time_range({ day: snapshot.day, start: snapshot.start, spacing: snapshot.spacing, end: snapshot.end });
        },
      });

    } else {
      const snapshot = { index: item._index, credits: item.credits, meetings: item.meetings, start_time: item.start_time || null, disabled: item.disabled || false };
      
      const res = await Model.api_delete_class_pattern(item._index);
      if (await check_response_error(res, "Class pattern could not be deleted.")) return;
      
      command_history.push({
        label: `Delete Class Pattern (${snapshot.credits} credits)`,
        field: "Time Slots",
        execute: async () => { await Model.api_delete_class_pattern(snapshot.index); },
        unexecute: async () => {
          await Model.api_add_class_pattern({ credits: snapshot.credits, meetings: snapshot.meetings, start_time: snapshot.start_time, disabled: snapshot.disabled });
        },
      });
    }

    View.render_undo_redo_state(command_history);
    await load_time_slots();

  }
});

// ---------------------------------------------------------------------------
// Print button functionality
// ---------------------------------------------------------------------------

// Print button: exports a PDF matching the schedule calendar view.
View.print_button.addEventListener("click", () => {
  const btn = View.print_button;
  const original_html = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = "Generating…";

  print_schedules_pdf()
    .catch(err => {
      console.error("PDF export error:", err);
      alert("PDF export failed: " + err.message);
    })
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = original_html;
    });
});

// Exports all generated schedules as a landscape A4 PDF using jsPDF.
//
// Algorithm overview:
//   Pass 1 — fetch schedule data for every (schedule, mode) pair and compute
//             a universal time range so all cards use the same vertical scale.
//   Pass 2 — build a self-contained SVG string for each calendar card via
//             build_card_svg().  SVG coordinates equal PDF points so font
//             sizes are exact without any post-render scaling.
//   Pass 3 — rasterise each SVG onto a 2× canvas (via an <img> blob URL),
//             then stamp the JPEG onto the PDF in a 2-column layout.
//
// Each card covers one entity (e.g. one faculty member, one room) for one schedule
// in one mode (faculty / room / lab).  Cards are placed two per page.
async function print_schedules_pdf() {
  console.log("[PDF] SVG-based export starting (v4)");

  // ── 1. Schedule count ────────────────────────────────────────────────
  let schedule_count;
  if (Model.csv_mode) {
    schedule_count = Model.csv_schedules.length;
  } else {
    const count_data = await Model.api_get_schedule_count();
    schedule_count = count_data.count || 0;
  }
  if (schedule_count === 0) { alert("No schedules to print."); return; }

  const MODES = ["faculty", "room", "lab"];
  const MODE_TITLE = { faculty: "Faculty", room: "Rooms", lab: "Lab" };
  const PALETTE = [
    "#b8deff", "#b8f0d8", "#ffeab8", "#ffc8d0", "#dac8ff",
    "#b8f0f0", "#ffd8b8", "#c8e8b8", "#ffd0f0", "#c8d8ff",
  ];

  const jsPDF = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
  if (!jsPDF) throw new Error("jsPDF library not loaded.");

  // ── 2. PDF / card geometry (landscape A4, 2 cols × 1 row) ──────────
  // All SVG units equal PDF points so font sizes are always correct.
  // Integer card dimensions avoid sub-pixel SVG rendering inconsistencies.
  const PAGE_W = 842, PAGE_H = 595;   // landscape A4 in pt
  const COLS = 2, ROWS = 1;
  const COL_GAP = 10, ROW_GAP = 8;
  const CARD_W = Math.floor((PAGE_W - (COLS - 1) * COL_GAP) / COLS);  // 416 pt
  const CARD_H = Math.floor((PAGE_H - (ROWS - 1) * ROW_GAP) / ROWS);  // 595 pt

  const TITLE_H = 20;
  const SUBTITLE_H = 14;
  const DAY_HDR_H = 18;
  const BOTTOM_PAD = 6;
  const FIXED_H = TITLE_H + SUBTITLE_H + DAY_HDR_H + BOTTOM_PAD;
  const CONTENT_H = CARD_H - FIXED_H;          // height available for time slots
  const CONTENT_TOP = TITLE_H + SUBTITLE_H + DAY_HDR_H;
  const TIME_AXIS_W = 44;
  const DAYS = ["MON", "TUE", "WED", "THU", "FRI"];
  const DAY_COL_W = (CARD_W - TIME_AXIS_W) / DAYS.length;  // 74.4 pt

  // ── 3. Utility helpers ───────────────────────────────────────────────
  function esc(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function fmt_min(m) {
    return `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
  }

  // ── 4. Pass 1 – fetch data, accumulate universal time range ──────────
  const card_entries = [];
  let universal_min = Infinity, universal_max = -Infinity;

  for (let i = 0; i < schedule_count; i++) {
    for (const mode of MODES) {
      const data = Model.csv_mode
        ? Model.get_csv_schedule_view(i, mode)
        : await Model.api_get_schedule_view(i, mode);
      if (data.error) continue;

      const { groups, time_slots, DAY_LABELS } = View.transform_to_calendar(data);
      if (groups.length === 0 || time_slots.length === 0) continue;

      for (const ts of time_slots) {
        const p = ts.split("-");
        const s = View.parse_time_minutes(p[0].trim());
        const e = View.parse_time_minutes(p.length > 1 ? p[1].trim() : p[0].trim());
        if (s < universal_min) universal_min = s;
        if (e > universal_max) universal_max = e;
      }

      // Per-schedule course→colour mapping (consistent within one schedule)
      const course_colors = {};
      let cidx = 0;
      for (const g of groups)
        for (const ds of Object.values(g.day_map))
          for (const ss of Object.values(ds))
            for (const slot of ss)
              if (!course_colors[slot.course])
                course_colors[slot.course] = PALETTE[cidx++ % PALETTE.length];

      card_entries.push({ groups, DAY_LABELS, mode, course_colors, schedule_index: i });
    }
  }

  if (card_entries.length === 0) { alert("No schedule data to print."); return; }

  universal_min = Math.floor(universal_min / 30) * 30;
  universal_max = Math.ceil(universal_max / 30) * 30;
  const range_min = universal_max - universal_min;
  // PX_PER_MIN is computed so the content area fills exactly CONTENT_H pt
  const PX_PER_MIN = CONTENT_H / range_min;

  console.log(`[PDF] universal_min=${universal_min} max=${universal_max} range=${range_min}min  PX_PER_MIN=${PX_PER_MIN.toFixed(3)}  CARD_W=${CARD_W} CARD_H=${CARD_H}`);

  // ── 5. SVG card builder ──────────────────────────────────────────────
  // Builds a complete SVG string for one calendar card.
  //
  // Layout (top to bottom):
  //   TITLE_H    — gradient title bar with entity name
  //   SUBTITLE_H — grey bar with "Schedule N — Mode" label
  //   DAY_HDR_H  — day-name column headers (Mon–Fri)
  //   CONTENT_H  — time-axis + course blocks (proportional to duration)
  //   BOTTOM_PAD — small padding below the last tick
  //
  // All text is wrapped in a <clipPath> so it never overflows its block.
  // Three text lines are drawn per block when height allows:
  //   course ID (always), detail/faculty/room (block_h > 18), time (block_h > 27).
  //
  // Parameters:
  //   group        - { name, day_map } from transform_to_calendar
  //   DAY_LABELS   - map from DAY_ABBREV to full day name
  //   mode         - "faculty" | "room" | "lab"
  //   course_colors - map from course_id to pastel hex colour
  //   sched_idx    - 0-based schedule number (for the subtitle label)
  //   mode_label   - human-readable mode title ("Faculty", "Rooms", "Lab")
  // Returns: SVG markup string
  function build_card_svg(group, DAY_LABELS, mode, course_colors, sched_idx, mode_label) {
    let clip_n = 0;  // unique clip-path counter within this SVG
    const W = CARD_W, H = CARD_H;

    let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`;

    // Gradient definition for the title bar
    s += `<defs>`;
    s += `<linearGradient id="tg" x1="0" x2="1" y1="0" y2="0">`;
    s += `<stop offset="0%" stop-color="#fe523a" stop-opacity="0.85"/>`;
    s += `<stop offset="100%" stop-color="#5286fe" stop-opacity="0.7"/>`;
    s += `</linearGradient>`;
    s += `</defs>`;

    // Card background + border
    s += `<rect width="${W}" height="${H}" fill="#f9f9f9" stroke="#bbb" stroke-width="1.5"/>`;

    // Title bar
    s += `<rect x="0" y="0" width="${W}" height="${TITLE_H}" fill="url(#tg)"/>`;
    const title = esc(group.name !== null ? group.name : mode_label);
    s += `<text x="${W / 2}" y="${TITLE_H - 5}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">${title}</text>`;

    // Subtitle bar
    s += `<rect x="0" y="${TITLE_H}" width="${W}" height="${SUBTITLE_H}" fill="#f0f0f0"/>`;
    s += `<line x1="0" y1="${TITLE_H + SUBTITLE_H}" x2="${W}" y2="${TITLE_H + SUBTITLE_H}" stroke="#ccc" stroke-width="0.5"/>`;
    s += `<text x="${W / 2}" y="${TITLE_H + SUBTITLE_H - 4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#555">`;
    s += `Schedule ${sched_idx + 1} \u2014 ${esc(mode_label)}</text>`;

    // Time-axis background strip
    s += `<rect x="0" y="${CONTENT_TOP}" width="${TIME_AXIS_W}" height="${CONTENT_H + BOTTOM_PAD}" fill="#f4f4f4"/>`;

    // Time-axis labels: one per full hour only.
    // Half-hour ticks get a grid line but no label, so 19:00 and 19:30 never crowd each other.
    // The first tick gets a label even if it falls on a half-hour (e.g. 08:30 start).
    for (let t = universal_min; t <= universal_max; t += 30) {
      const y = CONTENT_TOP + (t - universal_min) * PX_PER_MIN;
      const on_hour = t % 60 === 0;
      const is_first = t === universal_min;
      if (on_hour || is_first) {
        s += `<text x="${TIME_AXIS_W - 3}" y="${y + 3.5}" text-anchor="end" font-family="Arial,sans-serif" font-size="7" fill="#888">${fmt_min(t)}</text>`;
      }
    }

    // Day columns — for each column: white bg → grid lines → course blocks.
    // Drawing grid lines after the white background keeps them visible.
    for (let di = 0; di < DAYS.length; di++) {
      const day = DAYS[di];
      const day_x = TIME_AXIS_W + di * DAY_COL_W;
      const label = (DAY_LABELS && DAY_LABELS[day]) ? DAY_LABELS[day].slice(0, 3) : day.slice(0, 3);
      const day_slot_map = group.day_map[day] || {};
      const has_data = Object.keys(day_slot_map).length > 0;

      // Column left border
      s += `<line x1="${day_x}" y1="${TITLE_H + SUBTITLE_H}" x2="${day_x}" y2="${H}" stroke="#ccc" stroke-width="0.5"/>`;

      // Day header
      const hdr_bg = has_data ? "#dce8f6" : "#e8e8e8";
      s += `<rect x="${day_x}" y="${TITLE_H + SUBTITLE_H}" width="${DAY_COL_W}" height="${DAY_HDR_H}" fill="${hdr_bg}"/>`;
      s += `<line x1="${day_x}" y1="${CONTENT_TOP}" x2="${day_x + DAY_COL_W}" y2="${CONTENT_TOP}" stroke="#aaa" stroke-width="1"/>`;
      s += `<text x="${day_x + DAY_COL_W / 2}" y="${CONTENT_TOP - 5}" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#333">${label}</text>`;

      // White background for content area — drawn first so grid lines paint on top
      s += `<rect x="${day_x}" y="${CONTENT_TOP}" width="${DAY_COL_W}" height="${CONTENT_H + BOTTOM_PAD}" fill="white"/>`;

      // Horizontal grid lines (drawn after white bg so they're visible)
      for (let t = universal_min; t <= universal_max; t += 30) {
        const gy = CONTENT_TOP + (t - universal_min) * PX_PER_MIN;
        const gcol = t % 60 === 0 ? "#d0d0d0" : "#eeeeee";
        s += `<line x1="${day_x}" y1="${gy}" x2="${day_x + DAY_COL_W}" y2="${gy}" stroke="${gcol}" stroke-width="0.5"/>`;
      }

      // Course blocks
      for (const [time_str, slots] of Object.entries(day_slot_map)) {
        const tp = time_str.split("-");
        const start_min = View.parse_time_minutes(tp[0].trim());
        const end_min = View.parse_time_minutes(tp.length > 1 ? tp[1].trim() : tp[0].trim());
        const dur = Math.max(end_min - start_min, 10);
        const block_top = CONTENT_TOP + (start_min - universal_min) * PX_PER_MIN;
        const block_h = Math.max(dur * PX_PER_MIN - 1.5, 10);

        // Skip block if entirely outside the drawable content area
        if (block_top + block_h < CONTENT_TOP || block_top > CONTENT_TOP + CONTENT_H) continue;

        const n = slots.length;
        for (let si = 0; si < n; si++) {
          const slot = slots[si];
          const bg = course_colors[slot.course] || "#e0e0e0";
          const detail = mode === "faculty" ? slot.room : slot.faculty;
          const course_label = slot.section ? `${slot.course}.${slot.section}` : slot.course;
          const bx = day_x + 1 + (si / n) * (DAY_COL_W - 2);
          const bw = (DAY_COL_W - 2) / n;
          const cid = `c${clip_n++}`;

          // ClipPath keeps all text inside the block
          s += `<clipPath id="${cid}"><rect x="${bx}" y="${block_top}" width="${bw}" height="${block_h}"/></clipPath>`;
          s += `<rect x="${bx + 0.5}" y="${block_top + 0.5}" width="${bw - 1}" height="${block_h - 1}" fill="${bg}" rx="2" stroke="rgba(0,0,0,0.18)" stroke-width="0.5"/>`;
          s += `<g clip-path="url(#${cid})" font-family="Arial,sans-serif">`;
          // Course ID (bold)
          s += `<text x="${bx + 2.5}" y="${block_top + 9}" font-size="8" font-weight="bold" fill="#111">${esc(course_label)}</text>`;
          // Detail line (faculty or room) — only if block is tall enough
          if (block_h > 18 && detail && detail !== "None" && detail !== "\u2014") {
            s += `<text x="${bx + 2.5}" y="${block_top + 17}" font-size="7" fill="#333">${esc(detail)}</text>`;
          }
          // Time line — only if block is tall enough
          if (block_h > 27) {
            s += `<text x="${bx + 2.5}" y="${block_top + 25}" font-size="6.5" fill="#555">${esc(time_str)}</text>`;
          }
          // LAB badge
          if (slot.is_lab) {
            s += `<rect x="${bx + bw - 17}" y="${block_top + 1}" width="15" height="9" rx="2" fill="#e0a000"/>`;
            s += `<text x="${bx + bw - 9.5}" y="${block_top + 8.5}" text-anchor="middle" font-size="6" font-weight="bold" fill="white">LAB</text>`;
          }
          s += `</g>`;
        }
      }
    }

    s += `</svg>`;
    return s;
  }

  // ── 6. Pass 2 – build all SVG strings ────────────────────────────────
  const card_svgs = [];
  for (const { groups, DAY_LABELS, mode, course_colors, schedule_index } of card_entries) {
    for (const group of groups) {
      card_svgs.push(
        build_card_svg(group, DAY_LABELS, mode, course_colors, schedule_index, MODE_TITLE[mode])
      );
    }
  }
  if (card_svgs.length === 0) { alert("No schedule data to print."); return; }

  // ── 7. Render each SVG to a canvas (2× for crispness) ────────────────
  const RENDER_SCALE = 2;
  const cv_w = Math.round(CARD_W * RENDER_SCALE);
  const cv_h = Math.round(CARD_H * RENDER_SCALE);

  function svg_to_canvas(svg_str) {
    return new Promise((resolve, reject) => {
      const blob = new Blob([svg_str], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const img = new Image();
      img.onload = () => {
        const cv = document.createElement("canvas");
        cv.width = cv_w;
        cv.height = cv_h;
        const ctx = cv.getContext("2d");
        ctx.fillStyle = "#f9f9f9";
        ctx.fillRect(0, 0, cv_w, cv_h);
        ctx.drawImage(img, 0, 0, cv_w, cv_h);
        URL.revokeObjectURL(url);
        resolve(cv);
      };
      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("SVG render failed")); };
      img.src = url;
    });
  }

  const canvases = [];
  for (const svg of card_svgs) canvases.push(await svg_to_canvas(svg));

  // ── 8. Lay out canvases on PDF pages (fixed 2 × 2 grid) ──────────────
  const doc = new jsPDF({ orientation: "landscape", unit: "pt", format: "a4" });

  for (let ci = 0; ci < canvases.length; ci++) {
    const pos = ci % (COLS * ROWS);
    if (ci > 0 && pos === 0) doc.addPage();
    const col = pos % COLS;
    const row = Math.floor(pos / COLS);
    const x = col * (CARD_W + COL_GAP);
    const y = row * (CARD_H + ROW_GAP);
    doc.addImage(canvases[ci].toDataURL("image/jpeg", 0.88), "JPEG", x, y, CARD_W, CARD_H);
  }

  doc.save("schedules.pdf");
}

// ---------------------------------------------------------------------------
// Misc. functionalities
// ---------------------------------------------------------------------------

// Popup save button
View.popup_save.addEventListener("click", handle_popup_save);

// Close button: clears and hides the popup, restores pointer events, refocuses active field.
View.popup_close.addEventListener("click", () => {
  View.hide_popup();
  View.focus_field_button(Model.current_field);
});

// Keeps field button focused when clicking around the UI
const focus_containers = [
  View.navigator_div,
  View.main,
  View.nav_bar,
  View.top_bar,
  View.team_name,
  View.gui_wrapper,
];
focus_containers.forEach(el => {
  el.addEventListener("click", (e) => {

    if (e.target.closest("#chat-container")) return;
    // Skip form controls so programmatic focus does not steal focus from open dropdowns or inputs.
    if (["SELECT", "INPUT", "TEXTAREA"].includes(e.target.tagName)) return;

    View.focus_field_button(Model.current_field);
  });
});

// Randomizes Clippy's speech bubble's appearance and its content
async function activate_speech_bubble() {
  let shuffled_lines = View.shuffle_lines(View.lines);
  let index = 0;

  while (index < shuffled_lines.length) {
    View.switch_opacity(shuffled_lines, index);
    View.change_bubble_display();
    index++;
  }
}

// ---------------------------------------------------------------------------
// AI chat functionality
// ---------------------------------------------------------------------------

//  below code is for tts/stt and chat interface. currently using stream to 
// backend whisper for stt and browser's built in speech synthesis for tts, 
// but can be easily adapted to use other services or APIs.
// ---------------------------------------------------------------------------
// STT + TTS 
// ---------------------------------------------------------------------------

let mediaRecorder = null;
let isRecording = false;
let currentStream = null;
let chunkBuffer = [];
let audioChunks = [];

// -------------------------
// Start Recording
// -------------------------
async function startRecording() {
  try {
    if (isRecording) return; 

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    currentStream = stream;
    let mimeType = "audio/webm";
    if (!MediaRecorder.isTypeSupported("audio/webm")) {
      if (MediaRecorder.isTypeSupported("audio/ogg")) {
        mimeType = "audio/ogg";
      }
    }

    isRecording = true;

    function startSegment() {
      if (!sttToggle.checked) return;

      mediaRecorder = new MediaRecorder(stream, { mimeType });
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: mimeType });

        console.log("Segment ready:", blob.size);
        await sendToLocalWhisper(blob);

        startSegment();
      };

      mediaRecorder.start();

      // stop after 4s
      setTimeout(() => {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
          mediaRecorder.stop();
        }
      }, 4000);
    }

    startSegment();

  } catch (err) {
    console.error("Mic error:", err);
    sttToggle.checked = false;
  }
}
// -------------------------
// Stop Recording
// -------------------------
function stopRecording() {
  if (mediaRecorder && isRecording) {
    isRecording = false;
    mediaRecorder.stop();

    // stop mic stream
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
      currentStream = null;
    }
  }
}


async function sendToLocalWhisper(blob) {   
  const formData = new FormData();
  formData.append("audio", blob, "speech.webm");
  console.log("Sending blob:", blob.size);
  try {
    const res = await fetch("/transcribe", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    console.log("Response:", data);
    if (data.text) {
      let text = data.text || "";

      text = text.replace(/\.\.\.+/g, "");  
      text = text.replace(/[.,!?]+$/g, ""); 

      if (text.trim().length > 0) {
        chat_input.value += " " + text.trim();
      }
    } else {
      console.error("No transcription:", data);
    }

  } catch (err) {
    console.error("Transcription failed:", err);
  }
}

// -------------------------
// TTS
// -------------------------
function speak(text) {
  if (!text || !ttsToggle?.checked) return;

  // pause STT to avoid feedback loop
  if (isRecording) stopRecording();

  speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);

  utterance.onend = () => {
    if (sttToggle.checked) startRecording();
  };

  speechSynthesis.speak(utterance);
}

// -------------------------
// Toggle handling
// -------------------------
sttToggle.addEventListener("change", () => {
  console.log("Toggle changed:", sttToggle.checked);

  if (sttToggle.checked) {
    setTimeout(() => {
      startRecording();
    }, 0);
  } else {
    stopRecording();
  }
});

// -------------------------
// Chat UI toggle 
// -------------------------
const chat_button = View.get_chat_button();

chat_button.addEventListener("click", () => {
  document.body.classList.toggle("chat-open");
});


const chat_send = document.getElementById("chat-send");
const chat_input = document.getElementById("chat-input");
const chat_box = document.getElementById("chat-box");

chat_send.addEventListener("click", send_message);

chat_input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") send_message();
});

// Reads the chat input, appends the user's message to the chat box,
// posts it to /chat, then appends the agent's reply.
// Handles ui_action responses (e.g. "open_schedule") from the agent.
async function send_message() {
  const message = chat_input.value.trim();
  if (!message) return;

  // show user message
  chat_box.innerHTML += `<div class="chat-msg chat-user"><b>User:</b> ${message}</div>`;
  chat_input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await res.json();

    let result = data.result;
    let did_ui_action = false;

    // Case 1: direct UI action from backend — open the schedule viewer via the View button.
    if (data.ui_action === "open_schedule") {
      Model.set_schedules_generated(true);
      View.view_button.click();
      did_ui_action = true;
    }

    // Parse stringified JSON if needed
    if (typeof result === "string") {
      try {
        result = JSON.parse(result);
      } catch { }
    }

    // Case 2: UI action embedded inside result object — open the schedule viewer via the View button.
    if (result?.ui_action === "open_schedule") {
      Model.set_schedules_generated(true);
      View.view_button.click();
      did_ui_action = true;
    }

    // Decide what to display
    let response_text;

    if (did_ui_action) {
      response_text = message.toLowerCase().includes("generate")
        ? "opening Schedule view..."
        : "Opening schedule view...";
    } else if (result) {
      response_text = format_response(result);
    } else {
      console.error("No result returned:", data);
      response_text = "Something went wrong.";
    }


    // Always render response
    chat_box.innerHTML += `<div class="chat-msg chat-ai"><b>Clippy:</b> ${response_text}</div>`;
    chat_box.scrollTop = chat_box.scrollHeight;

    //TTS hook
    if (ttsToggle && ttsToggle.checked) {
      speak(response_text);
    }
    await refresh_current_field();

  } catch (err) {
    chat_box.innerHTML += `<div class="chat-msg chat-ai">Error: ${err}</div>`;
  }
}

// Refreshes the active tab after an AI chat response and opens the schedule
// viewer via the View button if the backend reports generated schedules.
async function refresh_current_field() {
  // Refresh whichever list tab is active
  if (Model.current_field === "Faculty") await load_faculty();
  else if (Model.current_field === "Courses") await load_courses();
  else if (Model.current_field === "Labs") await load_labs();
  else if (Model.current_field === "Rooms") await load_rooms();
  else if (Model.current_field === "Schedule") await load_schedule();
  else if (Model.current_field === "Time Slots") await load_time_slots();

  // Check if the AI just generated (or re-generated) schedules
  const { count } = await Model.api_get_schedule_count();
  if (count > 0) {
    Model.set_schedules_generated(true);
    View.render_schedules_generated_buttons();
    View.view_button.click();
  }
}

function format_response(res) {
  const clean = s => s.replace(/\\"/g, '"');
  if (typeof res === "string") return clean(res);
  if (res?.error) return clean(res.error);
  if (res?.status) return clean(res.status);
  return clean(JSON.stringify(res));
}
