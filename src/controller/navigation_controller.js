// ---------------------------------------------------------------------------
// CONTROLLER
//    Orchestrates between Model and View
// ---------------------------------------------------------------------------

import * as Model from "./navigation_model.js";
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

  const start_input   = document.getElementById("ts-start");
  const spacing_input = document.getElementById("ts-spacing");
  const end_input     = document.getElementById("ts-end");

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
    raw_text = await res.text();
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
    Model.push_back_stack(Model.current_content);
    Model.set_current_content(field);
    Model.clear_forward_stack();
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
}

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

async function load_faculty() {
  const faculty = await Model.api_get_faculty();
  View.render_faculty_list(faculty);
  Model.set_selected_item_data(null);
  View.render_amd_images(Model.current_field, false);
  attach_list_item_listeners();
  navigate_to("Faculty");
}

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

async function load_schedule() {
  View.render_schedule_form();
  document.getElementById("generate-schedules").addEventListener("click", generate_schedules);
  navigate_to("Schedule");
}

// ---------------------------------------------------------------------------
// Schedule generation
// ---------------------------------------------------------------------------

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
  const max_credits  = parseInt(document.getElementById("faculty-max-credits")?.value) || 0;
  const min_credits  = parseInt(document.getElementById("faculty-min-credits")?.value) || 0;
  const unique_limit = parseInt(document.getElementById("faculty-unique-course-limit")?.value) || 1;
  const max_days     = parseInt(document.getElementById("faculty-max-days")?.value) || 4;

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
  const room_prefs   = read_select_values("faculty-room-preference");
  const lab_prefs    = read_select_values("faculty-lab-preference");
  const mand_days    = read_select_values("faculty-mandatory-day");

  View.clear_all_errors();
  if (!check_select_duplicates("faculty-course-preference", "course preference")) return null;
  if (!check_select_duplicates("faculty-room-preference",   "room preference"))   return null;
  if (!check_select_duplicates("faculty-lab-preference",    "lab preference"))    return null;
  if (!check_select_duplicates("faculty-mandatory-day",     "mandatory day"))     return null;

  const course_preferences = Object.fromEntries(course_prefs.map(c => [c, 1]));
  const room_preferences   = Object.fromEntries(room_prefs.map(r => [r, 1]));
  const lab_preferences    = Object.fromEntries(lab_prefs.map(l => [l, 1]));

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

      const add_res = await Model.api_add_faculty({ name, ...fields });
      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

    } else if (Model.current_operation === "delete") {

      const del_res = await Model.api_delete_faculty(name);
      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

    } else if (Model.current_operation === "modify") {

      const fields = read_faculty_form_fields();
      if (!fields) return;

      const original_name = Model.selected_item_data ? Model.selected_item_data.name : name;
      const mod_res = await Model.api_modify_faculty(original_name, { name, ...fields });
      if (await check_response_error(mod_res, `"${original_name}" was not found. Please check the name and try again.`)) return;
    }

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
    if (!check_select_duplicates("courses-room",     "room"))     return;
    if (!check_select_duplicates("courses-lab",      "lab"))      return;
    if (!check_select_duplicates("courses-conflict", "conflict")) return;
    if (!check_select_duplicates("courses-faculty",  "faculty"))  return;

    const course_data = { course_id, credits, room: rooms, lab: labs, conflicts, faculty };

    if (Model.current_operation === "add") {

      const add_res = await Model.api_add_course(course_data);

      if (await check_response_error(add_res, `"${course_id}" could not be added.`)) return;

    } else if (Model.current_operation === "delete") {

      const del_res = await Model.api_delete_course(course_id);

      if (await check_response_error(del_res, `"${course_id}" was not found. Please check the course ID and try again.`)) return;

    } else if (Model.current_operation === "modify") {

      const index = Model.selected_item_data?._list_index ?? null;
      if (index === null) {
        View.show_field_error(id_input, "No course selected. Please click a course from the list first.");
        return;
      }
      const mod_res = await Model.api_modify_course(index, course_data);

      if (await check_response_error(mod_res, `"${course_id}" could not be modified.`)) return;
    }

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

    } else if (Model.current_operation === "delete") {

      if (!validate_labs_form()) return;

      const del_res = await Model.api_delete_lab(name);

      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

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
    }

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

    } else if (Model.current_operation === "delete") {
      if (!validate_rooms_form()) return;

      const del_res = await Model.api_delete_room(name);

      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

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
    }

    await load_rooms();

  } else if (Model.current_field === "Time Slots") {

    if (Model.current_operation === "add") {
      const type_sel = document.getElementById("ts-add-type");
      const add_type = type_sel ? type_sel.value : "time";

      if (add_type === "time") {
        if (!validate_time_range_form()) return;

        const day     = document.getElementById("ts-day")?.value || "";
        const start   = document.getElementById("ts-start")?.value.trim() || "";
        const spacing = parseInt(document.getElementById("ts-spacing")?.value) || 0;
        const end     = document.getElementById("ts-end")?.value.trim() || "";

        const res = await Model.api_add_time_range({ day, start, spacing, end });
        if (await check_response_error(res, "Time range could not be added.")) return;

      } else {
        if (!validate_class_pattern_form()) return;

        const credits    = parseInt(document.getElementById("ts-credits")?.value) || 0;
        const start_time = document.getElementById("ts-class-start-time")?.value.trim() || null;
        const disabled   = document.getElementById("ts-disabled")?.checked || false;

        const day_sels   = [...document.querySelectorAll('[name="ts-meeting-day"]')];
        const dur_inputs = [...document.querySelectorAll('[name="ts-meeting-duration"]')];
        const lab_cbs    = [...document.querySelectorAll('[name="ts-meeting-lab"]')];

        const meetings = day_sels.map((sel, i) => ({
          day:      sel.value,
          duration: parseInt(dur_inputs[i]?.value) || 0,
          lab:      lab_cbs[i]?.checked || false
        })).filter(m => m.day && m.duration > 0);

        const res = await Model.api_add_class_pattern({
          credits, meetings,
          start_time: start_time || null,
          disabled
        });
        if (await check_response_error(res, "Class pattern could not be added.")) return;
      }

    } else if (Model.current_operation === "modify") {
      const item = Model.selected_item_data;
      if (!item) return;

      if (item._type === "time") {
        if (!validate_time_range_form()) return;

        const start   = document.getElementById("ts-start")?.value.trim() || "";
        const spacing = parseInt(document.getElementById("ts-spacing")?.value) || 0;
        const end     = document.getElementById("ts-end")?.value.trim() || "";

        const res = await Model.api_modify_time_range(item._day, item._index, { start, spacing, end });
        if (await check_response_error(res, "Time range could not be modified.")) return;

      } else {
        if (!validate_class_pattern_form()) return;

        const credits    = parseInt(document.getElementById("ts-credits")?.value) || 0;
        const start_time = document.getElementById("ts-class-start-time")?.value.trim() || null;
        const disabled   = document.getElementById("ts-disabled")?.checked || false;

        const day_sels   = [...document.querySelectorAll('[name="ts-meeting-day"]')];
        const dur_inputs = [...document.querySelectorAll('[name="ts-meeting-duration"]')];
        const lab_cbs    = [...document.querySelectorAll('[name="ts-meeting-lab"]')];

        const meetings = day_sels.map((sel, i) => ({
          day:      sel.value,
          duration: parseInt(dur_inputs[i]?.value) || 0,
          lab:      lab_cbs[i]?.checked || false
        })).filter(m => m.day && m.duration > 0);

        const res = await Model.api_modify_class_pattern(item._index, {
          credits, meetings,
          start_time: start_time || null,
          disabled
        });
        if (await check_response_error(res, "Class pattern could not be modified.")) return;
      }
    }

    await load_time_slots();
  }
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

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
// Event Listeners
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", async () => {
  await Model.api_load_empty_config();
  View.config_name.textContent = "Config loaded: empty.json";
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
    Model.push_forward_stack(Model.current_content);
    Model.set_current_content(Model.pop_back_stack());
    await go_to_field(Model.current_content);
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
});

// Forward button
View.forward_button.addEventListener("click", async () => {
  if (Model.forward_stack.length > 0) {
    Model.push_back_stack(Model.current_content);
    Model.set_current_content(Model.pop_forward_stack());
    await go_to_field(Model.current_content);
    View.render_button_images(Model.back_stack, Model.forward_stack);
  }
});

// View button
View.view_button.addEventListener("click", () => {
  if (!Model.schedules_generated) return;
  view_schedule(0);
});

// Save config button
// Loads content of json or csv file
// load_button.addEventListener("change", function () { })
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

// Load file input
View.file_input.addEventListener("change", async function () {
  const file = View.file_input.files[0];
  if (!file) return;

  const ext = file.name.split(".").pop().toLowerCase();

  if (ext === "csv") {
    // ---- Load a previously-exported CSV schedule ----
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
    // ---- Load a JSON config file ----
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
    rooms:   rooms.map(r => r.name),
    labs:    labs.map(l => l.name),
    courses: courses.map(c => c.course_id),
    faculty: faculty.map(f => f.name),
  };
}

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
    const res = await Model.api_delete_faculty(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
    await load_faculty();
  } else if (field === "Courses") {
    const res = await Model.api_delete_course(item.course_id);
    if (await check_response_error(res, `"${item.course_id}" could not be deleted.`)) return;
    await load_courses();
  } else if (field === "Labs") {
    const res = await Model.api_delete_lab(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
    await load_labs();
  } else if (field === "Rooms") {
    const res = await Model.api_delete_room(item.name);
    if (await check_response_error(res, `"${item.name}" could not be deleted.`)) return;
    await load_rooms();
  } else if (field === "Time Slots") {
    if (item._type === "time") {
      const res = await Model.api_delete_time_range(item._day, item._index);
      if (await check_response_error(res, "Time range could not be deleted.")) return;
    } else {
      const res = await Model.api_delete_class_pattern(item._index);
      if (await check_response_error(res, "Class pattern could not be deleted.")) return;
    }
    await load_time_slots();
  }
});

// Print button
View.print_button.addEventListener("click", () => {
  if (Model.csv_mode) {
    print_csv_schedules_pdf();
  } else {
    window.open("/print_schedules", "_blank");
  }
});

// Generates and downloads a PDF from the in-memory parsed CSV schedules.
// Mirrors the layout produced by the backend's export_schedules_pdf().
function print_csv_schedules_pdf() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ orientation: "landscape" });

  const DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI"];

  Model.csv_schedules.forEach((schedule, i) => {
    if (i > 0) doc.addPage();

    doc.setFontSize(14);
    doc.setFont(undefined, "bold");
    doc.text(`Schedule ${i + 1}`, 14, 16);

    // Build rows sorted by day then time, matching the Course view mode
    const rows = [];
    for (const entry of schedule) {
      for (const m of entry.meetings) {
        rows.push({
          day: m.day,
          time: m.time_range + (m.is_lab ? " *" : ""),
          course: entry.course_id,
          section: entry.section,
          faculty: entry.faculty,
          room: entry.room,
          lab: entry.lab === "None" ? "—" : entry.lab
        });
      }
    }
    rows.sort((a, b) => {
      const d = DAY_ORDER.indexOf(a.day) - DAY_ORDER.indexOf(b.day);
      return d !== 0 ? d : a.time.localeCompare(b.time);
    });

    const table_rows = rows.map(r => [r.time, r.course, r.section, r.faculty, r.room, r.lab]);

    doc.autoTable({
      startY: 22,
      head: [["Time", "Course", "Section", "Faculty", "Room", "Lab"]],
      body: table_rows,
      styles: { fontSize: 9, cellPadding: 3 },
      headStyles: { fillColor: [200, 200, 200], textColor: 0, fontStyle: "bold" },
      alternateRowStyles: { fillColor: [245, 245, 245] },
      foot: [["* = lab session"]],
      footStyles: { fillColor: 255, textColor: 120, fontStyle: "italic", fontSize: 8 }
    });
  });

  doc.save("schedules.pdf");
}

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

    View.focus_field_button(Model.current_field);
  });
});


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

async function send_message() {
    const message = chat_input.value.trim();
    if (!message) return;

    // show user message
    chat_box.innerHTML += `<div class="chat-msg chat-user"><b>You:</b> ${message}</div>`;
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

        chat_box.innerHTML += `<div class="chat-msg chat-ai"><b>AI:</b> ${format_response(data.result)}</div>`;
        chat_box.scrollTop = chat_box.scrollHeight;

        await refresh_current_field();

    } catch (err) {
        chat_box.innerHTML += `<div class="chat-msg chat-ai">Error: ${err}</div>`;
    }
}

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
        if (Model.current_field !== "Schedule") {
            Model.set_current_field("Schedule");
            await load_schedule();
        }
        View.render_schedules_generated_buttons();
    }
}

function format_response(res) {
    const clean = s => s.replace(/\\"/g, '"');
    if (typeof res === "string") return clean(res);
    if (res?.error) return clean(res.error);
    if (res?.status) return clean(res.status);
    return clean(JSON.stringify(res));
}
