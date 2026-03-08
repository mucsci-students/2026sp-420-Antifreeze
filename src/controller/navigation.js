// index.html elements
const wrapper = document.getElementById("wrapper");

// Navigation Buttons
const load_button = document.getElementById("load-button");
const save_button = document.getElementById("save-button");
const back_button = document.getElementById("back-button");
const forward_button = document.getElementById("forward-button");
const add_button = document.getElementById("add-button");
const modify_button = document.getElementById("modify-button");
const delete_button = document.getElementById("delete-button");
const view_button = document.getElementById("view-button");
const print_button = document.getElementById("print-button");

// Fields Buttons
const faculty_button = document.getElementById("faculty-button");
const courses_button = document.getElementById("courses-button");
const labs_button = document.getElementById("labs-button");
const rooms_button = document.getElementById("rooms-button");
const schedule_button = document.getElementById("schedule-button");

// Disable the buttons until file is loaded
back_button.disabled = true;
forward_button.disabled = true;
add_button.disabled = true;
modify_button.disabled = true;
delete_button.disabled = true;
view_button.disabled = true;
print_button.disabled = true;

// Images inside buttons
const back_img = back_button.querySelector("img");
const forward_img = forward_button.querySelector("img");
const add_img = add_button.querySelector("img");
const modify_img = modify_button.querySelector("img");
const delete_img = delete_button.querySelector("img");
const view_img = view_button.querySelector("img");
const print_img = print_button.querySelector("img");

// Whitespace where information is printed
const navigator_div = document.querySelector(".navigator");
const main = document.querySelector(".main");

// Navigation bar and outer assets
const nav_bar = document.querySelector(".nav-bar");
const top_bar = document.querySelector(".top-bar");
const team_name = document.querySelector(".team-name");
const gui_wrapper = document.getElementById("wrapper");

// Popup elements
const amd_popup = document.getElementById("amd-popup");
const popup_save = document.getElementById("popup-save");
const popup_title = document.getElementById("popup-title");
const popup_form = document.getElementById("popup-form");
const popup_close = document.getElementById("popup-close");
const popup_box = document.querySelector(".popup-box");
const popup_header = document.getElementById("popup-header");

// Holds contents of loaded file
let loaded_file_content = null;
let loaded_file_extension = null;

// Field we are currently editing
let current_field = null;
let current_operation = null;
let schedules_generated = false;

// History stacks
let back_stack = [];
let forward_stack = [];
let current_content = navigator_div.innerHTML;

// Adds a single dynamic input row to a container when its associated button is clicked.
// Each row contains a text input and a remove button.
// Parameters: button_id, container_id, name (input name attr), placeholder
function add_dynamic_input(button_id, container_id, name, placeholder) {
  const button = document.getElementById(button_id);
  if (!button) {
    return;
  }
  button.addEventListener("click", () => {
    const container = document.getElementById(container_id);
    if (!container) return;
    const wrapper = document.createElement("div");
    wrapper.className = "input-wrapper";

    const input = document.createElement("input");
    input.type = "text";
    input.name = name;
    input.placeholder = placeholder;

    const remove_button = document.createElement("button");
    remove_button.id = "remove-button";
    remove_button.type = "button";
    remove_button.textContent = "-";
    remove_button.addEventListener("click", () => wrapper.remove());

    wrapper.appendChild(input);
    wrapper.appendChild(remove_button);
    container.appendChild(wrapper);
  });
}

// Sets up multiple dynamic input fields by calling add_dynamic_input for each.
// Parameters: fields - array of { button_id, container_id, name, placeholder }
function setup_dynamic_fields(fields) {
  fields.forEach(({ button_id, container_id, name, placeholder }) => {
    add_dynamic_input(button_id, container_id, name, placeholder);
  });
}

// Updates back and forward button images based on stack state.
// Dims buttons when their respective stacks are empty.
function update_button_images() {
  if (back_stack.length > 0) {
    back_img.src = "/static/images/back.png";
    back_button.style.color = "#484848";
    back_button.disabled = false;
  } else {
    back_img.src = "/static/images/back_shadow.png";
    back_button.style.color = "#808080";
    back_button.disabled = true;
  }

  if (forward_stack.length > 0) {
    forward_img.src = "/static/images/forward.png";
    forward_button.style.color = "#484848";
    forward_button.disabled = false;
  } else {
    forward_img.src = "/static/images/forward_shadow.png";
    forward_button.style.color = "#808080";
    forward_button.disabled = true;
  }
}

// Navigates to new content by pushing the current view onto the back stack.
// Clears the forward stack on new navigation. Updates button images.
// Parameters: content - HTML string to display in navigator_div
function navigate_to(content) {
  if (current_content !== content) {
    back_stack.push(current_content);
    current_content = content;
    navigator_div.innerHTML = current_content;

    // Clear forward stack on new navigation
    forward_stack = [];
    update_button_images();
  }
}

// Displays an inline error message directly below a given input element.
// Highlights the input border red and inserts an error span after it.
// Clears any pre-existing error on that input first.
// Parameters: input_el - the input DOM element, message - error string to display
function show_field_error(input_el, message) {
  if (!input_el) return;

  clear_field_error(input_el);

  input_el.style.borderColor = "#cc0000";

  const error_span = document.createElement("span");
  error_span.className = "field-error";
  error_span.style.color = "#cc0000";
  error_span.style.fontSize = "0.82em";
  error_span.style.display = "block";
  error_span.style.marginTop = "2px";
  error_span.textContent = message;

  input_el.insertAdjacentElement("afterend", error_span);
}

// Removes the inline error state (red border + error span) from a given input element.
// Parameters: input_el - the input DOM element
function clear_field_error(input_el) {
  if (!input_el) return;
  input_el.style.borderColor = "";
  const next = input_el.nextElementSibling;
  if (next && next.classList.contains("field-error")) {
    next.remove();
  }
}

// Clears all inline field errors currently visible in the popup form.
function clear_all_errors() {
  popup_form.querySelectorAll(".field-error").forEach(el => el.remove());
  popup_form.querySelectorAll("input").forEach(el => (el.style.borderColor = ""));
}

// Returns the identifying input element for the current field (used for error display).
function get_current_id_input() {
  if (current_field === "Faculty") return document.getElementById("faculty-name");
  if (current_field === "Courses") return document.getElementById("courses-id");
  if (current_field === "Labs") return document.getElementById("labs-name");
  if (current_field === "Rooms") return document.getElementById("rooms-name");
  return null;
}

// Reads the response body text, extracts any error message, and displays it on
// the identifying input for the current field. Returns true if an error was shown,
// false if no error was found and the operation can proceed.
// Parameters: res - the fetch Response object, fallback - shown if body has no error
async function check_response_error(res, fallback) {
  const input_el = get_current_id_input();

  let raw_text = "";
  try {
    raw_text = await res.text();
  } catch (_) {
    // Could not read body at all — show fallback
    show_field_error(input_el, fallback);
    return true;
  }

  // Try to extract an error string from the body
  let message = null;
  try {
    const body = JSON.parse(raw_text);
    if (body && typeof body.error === "string" && body.error.trim() !== "") {
      message = body.error;
    } else if (body && typeof body.message === "string" && body.message.trim() !== "") {
      message = body.message;
    }
  } catch (_) {
    // Body was plain text, not JSON
    if (raw_text.trim() !== "") {
      message = raw_text.trim();
    }
  }

  if (message) {
    show_field_error(input_el, message);
    return true;
  }

  if (!res.ok) {
    show_field_error(input_el, fallback);
    return true;
  }

  return false;
}

// Validates all inputs for the Faculty Add/Modify form.
// Returns true if all fields are valid, false if any errors were shown.
// Parameters: is_add - boolean, true when adding (all fields required)
function validate_faculty_form(is_add) {
  clear_all_errors();
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
    show_field_error(name_input, "Faculty name is required.");
    valid = false;
  } else if (!/^[A-Za-z\s'\-]+$/.test(name)) {
    show_field_error(name_input, "Faculty name must contain only letters, spaces, hyphens, or apostrophes.");
    valid = false;
  }

  // Max credits: required on add; must be a non-negative integer if provided
  if (is_add || max_credits !== "") {
    if (max_credits === "") {
      show_field_error(max_credits_input, "Max credits is required.");
      valid = false;
    } else if (isNaN(max_credits) || !Number.isInteger(parseFloat(max_credits)) || parseInt(max_credits) < 0) {
      show_field_error(max_credits_input, "Max credits must be a non-negative whole number.");
      valid = false;
    }
  }

  // Min credits: required on add; must be a non-negative integer if provided
  if (is_add || min_credits !== "") {
    if (min_credits === "") {
      show_field_error(min_credits_input, "Min credits is required.");
      valid = false;
    } else if (isNaN(min_credits) || !Number.isInteger(parseFloat(min_credits)) || parseInt(min_credits) < 0) {
      show_field_error(min_credits_input, "Min credits must be a non-negative whole number.");
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
    show_field_error(min_credits_input, "Min credits must be less than or equal to max credits.");
    valid = false;
  }

  // Unique course limit: required on add; must be a positive integer if provided
  if (is_add || unique_limit !== "") {
    if (unique_limit === "") {
      show_field_error(unique_limit_input, "Unique course limit is required.");
      valid = false;
    } else if (isNaN(unique_limit) || !Number.isInteger(parseFloat(unique_limit)) || parseInt(unique_limit) < 1) {
      show_field_error(unique_limit_input, "Unique course limit must be a whole number of at least 1.");
      valid = false;
    }
  }

  // Max days: required on add; must be 1–5 if provided
  if (is_add || max_days !== "") {
    if (max_days === "") {
      show_field_error(max_days_input, "Max days is required.");
      valid = false;
    } else if (isNaN(max_days) || !Number.isInteger(parseFloat(max_days)) || parseInt(max_days) < 1 || parseInt(max_days) > 5) {
      show_field_error(max_days_input, "Max days must be a whole number between 1 and 5.");
      valid = false;
    }
  }

  // Time slots: optional, but if filled must match "DAY HH:MM-HH:MM"
  const time_slot_pattern = /^(MON|TUE|WED|THU|FRI)\s+([01]\d|2[0-3]):[0-5]\d-([01]\d|2[0-3]):[0-5]\d$/;
  document.querySelectorAll('input[name="faculty-time-slot"]').forEach(input => {
    const val = input.value.trim();
    if (val !== "" && !time_slot_pattern.test(val)) {
      show_field_error(input, "Time slot must be in the format: MON 09:00-12:00");
      valid = false;
    }
  });

  // Mandatory days: optional, but if filled must be a valid abbreviation
  const day_pattern = /^(MON|TUE|WED|THU|FRI)$/;
  document.querySelectorAll('input[name="faculty-mandatory-day"]').forEach(input => {
    const val = input.value.trim();
    if (val !== "" && !day_pattern.test(val)) {
      show_field_error(input, "Day must be one of: MON, TUE, WED, THU, FRI");
      valid = false;
    }
  });

  return valid;
}

// Validates the Faculty Delete form (name only).
// Returns true if valid, false otherwise.
function validate_faculty_delete_form() {
  clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("faculty-name");
  const name = name_input ? name_input.value.trim() : "";

  if (!name) {
    show_field_error(name_input, "Faculty name is required.");
    valid = false;
  } else if (!/^[A-Za-z\s'\-]+$/.test(name)) {
    show_field_error(name_input, "Faculty name must contain only letters, spaces, hyphens, or apostrophes.");
    valid = false;
  }

  return valid;
}

// Validates all inputs for the Courses Add/Modify form.
// Returns true if all fields are valid, false if any errors were shown.
// Parameters: is_add - boolean, true when adding (stricter required checks)
function validate_courses_form(is_add) {
  clear_all_errors();
  let valid = true;

  const id_input = document.getElementById("courses-id");
  const credits_input = document.getElementById("courses-credits");

  const course_id = id_input ? id_input.value.trim() : "";
  const credits = credits_input ? credits_input.value.trim() : "";

  // Course ID: required always; must match format like "CMSC 420"
  const course_id_pattern = /^[A-Z]{2,6}\s+\d{3,4}$/;
  if (!course_id) {
    show_field_error(id_input, "Course ID is required.");
    valid = false;
  } else if (!course_id_pattern.test(course_id)) {
    show_field_error(id_input, "Course ID must be in the format: CMSC 420 (uppercase letters, space, then 3–4 digits).");
    valid = false;
  }

  // Credits: required on add; must be a positive integer if provided
  if (is_add || credits !== "") {
    if (credits === "") {
      show_field_error(credits_input, "Credits is required.");
      valid = false;
    } else if (isNaN(credits) || !Number.isInteger(parseFloat(credits)) || parseInt(credits) < 1) {
      show_field_error(credits_input, "Credits must be a whole number greater than 0.");
      valid = false;
    }
  }

  // Rooms: at least one non-empty entry required when adding
  if (is_add) {
    const room_inputs = [...document.querySelectorAll('input[name="courses-room"]')];
    const filled_rooms = room_inputs.filter(i => i.value.trim() !== "");
    if (room_inputs.length > 0 && filled_rooms.length === 0) {
      show_field_error(room_inputs[0], "At least one room is required.");
      valid = false;
    }
  }

  return valid;
}

// Validates the Courses Delete form (course ID only).
// Returns true if valid, false otherwise.
function validate_courses_delete_form() {
  clear_all_errors();
  let valid = true;

  const id_input = document.getElementById("courses-id");
  const course_id = id_input ? id_input.value.trim() : "";

  const course_id_pattern = /^[A-Z]{2,6}\s+\d{3,4}$/;
  if (!course_id) {
    show_field_error(id_input, "Course ID is required.");
    valid = false;
  } else if (!course_id_pattern.test(course_id)) {
    show_field_error(id_input, "Course ID must be in the format: CMSC 420 (uppercase letters, space, then 3–4 digits).");
    valid = false;
  }

  return valid;
}

// Validates the Labs Add/Modify/Delete form (name only).
// Returns true if valid, false otherwise.
function validate_labs_form() {
  clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("labs-name");
  const name = name_input ? name_input.value.trim() : "";

  if (!name) {
    show_field_error(name_input, "Lab name is required.");
    valid = false;
  } else if (name.length > 64) {
    show_field_error(name_input, "Lab name must be 64 characters or fewer.");
    valid = false;
  }

  return valid;
}

// Validates the Rooms Add/Modify/Delete form (name only).
// Returns true if valid, false otherwise.
function validate_rooms_form() {
  clear_all_errors();
  let valid = true;

  const name_input = document.getElementById("rooms-name");
  const name = name_input ? name_input.value.trim() : "";

  // Room name must start with a letter; may contain letters, digits, spaces, hyphens
  const room_pattern = /^[A-Za-z][\w\s\-]*$/;
  if (!name) {
    show_field_error(name_input, "Room name is required.");
    valid = false;
  } else if (!room_pattern.test(name)) {
    show_field_error(name_input, "Room name must start with a letter and contain only letters, numbers, spaces, or hyphens.");
    valid = false;
  }

  return valid;
}

// Opens the add/modify/delete popup for the currently selected field.
// Shows an error if no field is selected. Renders the appropriate form
// fields for each combination of action and current_field.
// Parameters: action - "Add", "Modify", or "Delete"
function edit_popup(action) {
  if (current_field == null) {
    popup_title.textContent = "Error";
    popup_form.innerHTML = `<div class="form-line"><p>Please select a field first.</p></div>`;
    amd_popup.classList.remove("popup-hidden");
    return;
  }

  popup_title.textContent = action + " " + current_field;
  popup_form.innerHTML = "";

  if (action === "Add") {
    switch (current_field) {
      case "Faculty":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="faculty-name">Faculty Name:</label>
            <input type="text" id="faculty-name" placeholder="e.g. Hobbs" required/>
          </div>

          <div class="form-line">
            <label for="faculty-max-credits">Max Credits:</label>
            <input type="number" id="faculty-max-credits" placeholder="Must be >= min credits" required/>
          </div>

          <div class="form-line">
            <label for="faculty-min-credits">Min Credits:</label>
            <input type="number" id="faculty-min-credits" placeholder="Must be <= max credits" required/>
          </div>

          <div class="form-line">
            <label for="faculty-unique-course-limit">Unique Course Limit:</label>
            <input type="number" id="faculty-unique-course-limit" required/>
          </div>

          <div class="form-line">
            <label for="faculty-max-days">Max Days:</label>
            <input type="number" id="faculty-max-days" placeholder="1-5" required/>
          </div>

          <hr />

          <div class="form-line">
            <label>Time Slots:</label>
            <div id="faculty-time-slots-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-time-slot" placeholder="e.g. MON 13:00-17:00" />
              </div>
            </div>
            <button type="button" id="add-faculty-time-slots">+</button>
          </div>

          <div class="form-line">
            <label>Course Preferences:</label>
            <div id="faculty-course-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-course-preference" placeholder="e.g. CMSC 162" />
              </div>
            </div>
            <button type="button" id="add-faculty-course-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Room Preferences:</label>
            <div id="faculty-room-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-room-preference" placeholder="e.g. Roddy 136" />
              </div>
            </div>
            <button type="button" id="add-faculty-room-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Lab Preferences:</label>
            <div id="faculty-lab-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-lab-preference" placeholder="e.g. Mac" />
              </div>
            </div>
            <button type="button" id="add-faculty-lab-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Mandatory Days:</label>
            <div id="faculty-mandatory-days-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-mandatory-day" placeholder="e.g. MON/TUE/WED/THU/FRI" required/>
              </div>
            </div>
            <button type="button" id="add-faculty-mandatory-days">+</button>
          </div>
        `;

        // Setup dynamic inputs
        setup_dynamic_fields([
          {
            button_id: "add-faculty-time-slots",
            container_id: "faculty-time-slots-container",
            name: "faculty-time-slot",
            placeholder: "e.g. TUE 09:00-12:00",
          },
          {
            button_id: "add-faculty-course-preferences",
            container_id: "faculty-course-preferences-container",
            name: "faculty-course-preference",
            placeholder: "e.g. CMSC 162",
          },
          {
            button_id: "add-faculty-room-preferences",
            container_id: "faculty-room-preferences-container",
            name: "faculty-room-preference",
            placeholder: "e.g. Roddy 136",
          },
          {
            button_id: "add-faculty-lab-preferences",
            container_id: "faculty-lab-preferences-container",
            name: "faculty-lab-preference",
            placeholder: "e.g. Mac",
          },
          {
            button_id: "add-faculty-mandatory-days",
            container_id: "faculty-mandatory-days-container",
            name: "faculty-mandatory-day",
            placeholder: "e.g. TUE",
          },
        ]);
        break;

      case "Courses":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="courses-id">Course ID:</label>
            <input type="text" id="courses-id" placeholder="e.g. CMSC 420" required/>
          </div>

          <div class="form-line">
            <label for="courses-credits">Credits:</label>
            <input type="number" id="courses-credits" placeholder="Must be greater than 0" required/>
          </div>

          <hr />

          <div class="form-line">
            <label>Rooms:</label>
            <div id="courses-rooms-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-room" placeholder="e.g. Roddy 140" required/>
              </div>
            </div>
            <button type="button" id="add-courses-rooms">+</button>
          </div>

          <div class="form-line">
            <label>Labs:</label>
            <div id="courses-labs-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-lab" placeholder="e.g. Linux" />
              </div>
            </div>
            <button type="button" id="add-courses-labs">+</button>
          </div>

          <div class="form-line">
            <label>Conflicts:</label>
            <div id="courses-conflicts-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-conflict" placeholder="e.g. CMSC 380" />
              </div>
            </div>
            <button type="button" id="add-courses-conflicts">+</button>
          </div>

          <div class="form-line">
            <label>Faculty:</label>
            <div id="courses-faculty-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-faculty" placeholder="e.g. Hobbs" />
              </div>
            </div>
            <button type="button" id="add-courses-faculty">+</button>
          </div>
        `;

        setup_dynamic_fields([
          {
            button_id: "add-courses-rooms",
            container_id: "courses-rooms-container",
            name: "courses-room",
            placeholder: "e.g. Roddy 140",
          },
          {
            button_id: "add-courses-labs",
            container_id: "courses-labs-container",
            name: "courses-lab",
            placeholder: "e.g. Linux",
          },
          {
            button_id: "add-courses-conflicts",
            container_id: "courses-conflicts-container",
            name: "courses-conflict",
            placeholder: "e.g. CMSC 380",
          },
          {
            button_id: "add-courses-faculty",
            container_id: "courses-faculty-container",
            name: "courses-faculty",
            placeholder: "e.g. Hobbs",
          },
        ]);
        break;

      case "Labs":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="labs-name">Lab Name:</label>
            <input type="text" id="labs-name" placeholder="e.g. Mac" required/>
          </div>
        `;
        break;

      case "Rooms":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="rooms-name">Room Name:</label>
            <input type="text" id="rooms-name" placeholder="e.g. Roddy 147" required/>
          </div>
        `;
        break;
    }
  } else if (action === "Modify") {
    switch (current_field) {
      case "Faculty":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="faculty-name">Faculty Name:</label>
            <input type="text" id="faculty-name" placeholder="e.g. Hobbs" />
          </div>

          <div class="form-line">
            <label for="faculty-max-credits">Max Credits:</label>
            <input type="number" id="faculty-max-credits" placeholder="Must be >= min credits" />
          </div>

          <div class="form-line">
            <label for="faculty-min-credits">Min Credits:</label>
            <input type="number" id="faculty-min-credits" placeholder="Must be <= max credits" />
          </div>

          <div class="form-line">
            <label for="faculty-unique-course-limit">Unique Course Limit:</label>
            <input type="number" id="faculty-unique-course-limit" />
          </div>

          <div class="form-line">
            <label for="faculty-max-days">Max Days:</label>
            <input type="number" id="faculty-max-days" placeholder="1-5" />
          </div>

          <hr />

          <div class="form-line">
            <label>Time Slots:</label>
            <div id="faculty-time-slots-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-time-slot" placeholder="e.g. MON 13:00-17:00" />
              </div>
            </div>
            <button type="button" id="add-faculty-time-slots">+</button>
          </div>

          <div class="form-line">
            <label>Course Preferences:</label>
            <div id="faculty-course-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-course-preference" placeholder="e.g. CMSC 162" />
              </div>
            </div>
            <button type="button" id="add-faculty-course-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Room Preferences:</label>
            <div id="faculty-room-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-room-preference" placeholder="e.g. Roddy 136" />
              </div>
            </div>
            <button type="button" id="add-faculty-room-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Lab Preferences:</label>
            <div id="faculty-lab-preferences-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-lab-preference" placeholder="e.g. Mac" />
              </div>
            </div>
            <button type="button" id="add-faculty-lab-preferences">+</button>
          </div>

          <div class="form-line">
            <label>Mandatory Days:</label>
            <div id="faculty-mandatory-days-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="faculty-mandatory-day" placeholder="e.g. MON/TUE/WED/THU/FRI" />
              </div>
            </div>
            <button type="button" id="add-faculty-mandatory-days">+</button>
          </div>
        `;

        // Setup dynamic inputs
        setup_dynamic_fields([
          {
            button_id: "add-faculty-time-slots",
            container_id: "faculty-time-slots-container",
            name: "faculty-time-slot",
            placeholder: "e.g. TUE 09:00-12:00",
          },
          {
            button_id: "add-faculty-course-preferences",
            container_id: "faculty-course-preferences-container",
            name: "faculty-course-preference",
            placeholder: "e.g. CMSC 162",
          },
          {
            button_id: "add-faculty-room-preferences",
            container_id: "faculty-room-preferences-container",
            name: "faculty-room-preference",
            placeholder: "e.g. Roddy 136",
          },
          {
            button_id: "add-faculty-lab-preferences",
            container_id: "faculty-lab-preferences-container",
            name: "faculty-lab-preference",
            placeholder: "e.g. Mac",
          },
          {
            button_id: "add-faculty-mandatory-days",
            container_id: "faculty-mandatory-days-container",
            name: "faculty-mandatory-day",
            placeholder: "e.g. TUE",
          },
        ]);
        break;

      case "Courses":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="courses-id">Course ID:</label>
            <input type="text" id="courses-id" placeholder="e.g. CMSC 420"/>
          </div>

          <div class="form-line">
            <label for="courses-credits">Credits:</label>
            <input type="number" id="courses-credits" placeholder="Must be greater than 0" />
          </div>

          <hr />

          <div class="form-line">
            <label>Rooms:</label>
            <div id="courses-rooms-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-room" placeholder="e.g. Roddy 140"/>
              </div>
            </div>
            <button type="button" id="add-courses-rooms">+</button>
          </div>

          <div class="form-line">
            <label>Labs:</label>
            <div id="courses-labs-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-lab" placeholder="e.g. Linux"/>
              </div>
            </div>
            <button type="button" id="add-courses-labs">+</button>
          </div>

          <div class="form-line">
            <label>Conflicts:</label>
            <div id="courses-conflicts-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-conflict" placeholder="e.g. CMSC 380"/>
              </div>
            </div>
            <button type="button" id="add-courses-conflicts">+</button>
          </div>

          <div class="form-line">
            <label>Faculty:</label>
            <div id="courses-faculty-container" class="dynamic-container">
              <div class="input-wrapper">
                <input type="text" name="courses-faculty" placeholder="e.g. Hobbs"/>
              </div>
            </div>
            <button type="button" id="add-courses-faculty">+</button>
          </div>
        `;

        setup_dynamic_fields([
          {
            button_id: "add-courses-rooms",
            container_id: "courses-rooms-container",
            name: "courses-room",
            placeholder: "e.g. Roddy 140",
          },
          {
            button_id: "add-courses-labs",
            container_id: "courses-labs-container",
            name: "courses-lab",
            placeholder: "e.g. Linux",
          },
          {
            button_id: "add-courses-conflicts",
            container_id: "courses-conflicts-container",
            name: "courses-conflict",
            placeholder: "e.g. CMSC 380",
          },
          {
            button_id: "add-courses-faculty",
            container_id: "courses-faculty-container",
            name: "courses-faculty",
            placeholder: "e.g. Hobbs",
          },
        ]);
        break;

      case "Labs":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="labs-name">Current Lab Name:</label>
            <input type="text" id="labs-name" placeholder="e.g. Mac" />
          </div>
          <div class="form-line">
            <label for="labs-new-name">New Lab Name:</label>
            <input type="text" id="labs-new-name" placeholder="e.g. Linux" />
          </div>
        `;
        break;

      case "Rooms":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="rooms-name">Current Room Name:</label>
            <input type="text" id="rooms-name" placeholder="e.g. Roddy 147" />
          </div>
          <div class="form-line">
            <label for="rooms-new-name">New Room Name:</label>
            <input type="text" id="rooms-new-name" placeholder="e.g. Roddy 148" />
          </div>
        `;
        break;
    }
  } else if (action === "Delete") {
    switch (current_field) {
      case "Faculty":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="faculty-name">Faculty Name:</label> 
            <input type="text" id="faculty-name" placeholder="e.g. Hobbs" required/>
          </div>
        `;
        break;
      case "Courses":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="courses-id">Course ID:</label>
            <input type="text" id="courses-id" placeholder="e.g. CMSC 420" required/>
          </div>
        `;
        break;
      case "Labs":
        popup_form.innerHTML = `
            <div class="form-line">
              <label for="labs-name">Lab Name:</label>
              <input type="text" id="labs-name" placeholder="e.g. Mac" required/>
            </div>
          `;
        break;

      case "Rooms":
        popup_form.innerHTML = `
            <div class="form-line">
              <label for="rooms-name">Room Name:</label>
              <input type="text" id="rooms-name" placeholder="e.g. Roddy 147" required/>
            </div>
          `;
        break;
    }
  }

  amd_popup.classList.remove("popup-hidden");
  wrapper.style.pointerEvents = "none";
}

// Updates add/modify/delete button images and colors based on whether a field is selected.
// Dims buttons when no field is active.
function update_amd_images() {
  if (current_field == null || current_field == "Schedule") {
    add_img.src = "/static/images/add_shadow.png";
    modify_img.src = "/static/images/modify_shadow.png";
    delete_img.src = "/static/images/delete_shadow.png";
    add_button.style.color = "#808080";
    modify_button.style.color = "#808080";
    delete_button.style.color = "#808080";

    // Disable the buttons
    add_button.disabled = true;
    modify_button.disabled = true;
    delete_button.disabled = true;
    print_button.disabled = true;
  } else {
    add_img.src = "/static/images/add.png";
    modify_img.src = "/static/images/modify.png";
    delete_img.src = "/static/images/delete.png";
    add_button.style.color = "#484848";
    modify_button.style.color = "#484848";
    delete_button.style.color = "#484848";

    // Disable the buttons
    add_button.disabled = false;
    modify_button.disabled = false;
    delete_button.disabled = false;
  }
}

// Fields event listeners
faculty_button.addEventListener("click", () => {
  current_field = "Faculty";
  navigate_to("Existing faculty would be printed here");
  load_faculty();
  update_amd_images();
  popup_form.style.height = "540px";
  popup_box.style.width = "500px";
});

courses_button.addEventListener("click", () => {
  current_field = "Courses";
  navigate_to("Existing courses would be printed here");
  load_courses();
  update_amd_images();
  popup_form.style.height = "540px";
  popup_box.style.width = "500px";
  popup_header.style.width = "495px";
});

labs_button.addEventListener("click", () => {
  current_field = "Labs";
  navigate_to("Existing labs would be printed here");
  load_labs();
  update_amd_images();
  popup_form.style.height = "540px";
  popup_box.style.width = "500px";
  popup_header.style.width = "495px";
});

rooms_button.addEventListener("click", () => {
  current_field = "Rooms";
  navigate_to(`Existing ${current_field} would be printed here`);
  load_rooms();
  update_amd_images();
  popup_form.style.height = "540px";
  popup_box.style.width = "500px";
  popup_header.style.width = "495px";
});

schedule_button.addEventListener("click", () => {
  current_field = "Schedule";
  navigate_to("Schedule generator");
  load_schedule();
  update_amd_images();
  popup_form.style.height = "605px";
  popup_box.style.width = "600px";
  popup_header.style.width = "595px";
});

// Back button
back_button.addEventListener("click", () => {
  if (back_stack.length > 0) {
    forward_stack.push(current_content);
    current_content = back_stack.pop();
    navigator_div.innerHTML = current_content;
    update_button_images();
  }
});

// Forward button
forward_button.addEventListener("click", () => {
  if (forward_stack.length > 0) {
    back_stack.push(current_content);
    current_content = forward_stack.pop();
    navigator_div.innerHTML = current_content;
    update_button_images();
  }
});

view_button.addEventListener("click", () => {

  if (!schedules_generated) {
    return;
  }

  view_schedule(0);

});

// Loads content of json or csv file
//load_button.addEventListener("change", function () {
//})
save_button.addEventListener("click", async (e) => {

  e.preventDefault();  // stops redirect / form submit

  const res = await fetch("/save_config");
  const config = await res.json();

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


function load_file_content(input) {
  let file_types = ['json', 'csv'];
  let file_reader = new FileReader();

  file_reader.onload = function () {
    // PUT FETCH IN HERE
    loaded_file_content = file_reader.result;
  }

  file_reader.readAsText(input.files[0]);
}

// Add button: sets current_operation and opens the Add popup for the active field.
add_button.addEventListener("click", () => {
  current_operation = "add";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();

  edit_popup("Add");
});

// Modify button: sets current_operation and opens the Modify popup for the active field.
modify_button.addEventListener("click", () => {
  current_operation = "modify";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();

  edit_popup("Modify");
});

// Delete button: sets current_operation and opens the Delete popup for the active field.
delete_button.addEventListener("click", () => {
  current_operation = "delete";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();

  edit_popup("Delete");
});

// Keeps field button focused when clicking around in navigator_div
navigator_div.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Keeps field button focused when clicking around in main
main.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Keeps field button focused when clicking around in nav_bar
nav_bar.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Keeps field button focused when clicking around in top_bar
top_bar.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Keeps field button focused when clicking around in team_name
team_name.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Keeps field button focused when clicking around in gui_wrapper
gui_wrapper.addEventListener("click", () => {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// Save button: validates form inputs, then POSTs to the appropriate API route
// based on current_field and current_operation. Refreshes the list on success.
popup_save.addEventListener("click", async () => {
  console.log("SAVE CLICKED", current_field, current_operation);

  if (current_field === "Faculty") {

    if (current_operation === "add" && !validate_faculty_form(true)) return;
    if (current_operation === "modify" && !validate_faculty_form(false)) return;
    if (current_operation === "delete" && !validate_faculty_delete_form()) return;

    const name = document.getElementById("faculty-name").value.trim();

    if (current_operation === "add") {

      const max_credits = parseInt(
        document.getElementById("faculty-max-credits").value
      );

      await fetch("/faculty", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name,
          maximum_credits: max_credits,
          maximum_days: 4,
          minimum_credits: 0,
          unique_course_limit: 1,
          times: {},
          course_preferences: {},
          room_preferences: {},
          lab_preferences: {},
          mandatory_days: []
        })
      });

    } else if (current_operation === "delete") {

      const del_res = await fetch(`/faculty/${encodeURIComponent(name)}`, {
        method: "DELETE"
      });

      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

    } else if (current_operation === "modify") {

      const max_credits = parseInt(
        document.getElementById("faculty-max-credits").value
      );

      const data = {
        maximum_credits: max_credits,
        maximum_days: 4,
        minimum_credits: 0,
        unique_course_limit: 1,
        times: {},
        course_preferences: {},
        room_preferences: {},
        lab_preferences: {},
        mandatory_days: []
      };

      const mod_res = await fetch(`/faculty/${encodeURIComponent(name)}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (await check_response_error(mod_res, `"${name}" was not found. Please check the name and try again.`)) return;

    }

    await load_faculty();

  } else if (current_field === "Courses") {

    if (current_operation === "add" && !validate_courses_form(true)) return;
    if (current_operation === "modify" && !validate_courses_form(false)) return;
    if (current_operation === "delete" && !validate_courses_delete_form()) return;

    const id_input = document.getElementById("courses-id");

    if (!id_input) {
      console.error("Course ID input not found");
      return;
    }

    const course_id = id_input.value.trim();

    const credits_input = document.getElementById("courses-credits");
    const credits = credits_input ? parseInt(credits_input.value) : null;

    const rooms = [...document.querySelectorAll('input[name="courses-room"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const labs = [...document.querySelectorAll('input[name="courses-lab"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const conflicts = [...document.querySelectorAll('input[name="courses-conflict"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    const faculty = [...document.querySelectorAll('input[name="courses-faculty"]')]
      .map(i => i.value.trim())
      .filter(v => v !== "");

    if (current_operation === "add") {

      await fetch("/courses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          course_id: course_id,
          credits: credits,
          room: rooms,
          lab: labs,
          conflicts: conflicts,
          faculty: faculty
        })
      });

    } else if (current_operation === "delete") {

      const del_res = await fetch(`/courses/${encodeURIComponent(course_id)}`, {
        method: "DELETE"
      });

      if (await check_response_error(del_res, `"${course_id}" was not found. Please check the course ID and try again.`)) return;

    } else if (current_operation === "modify") {

      const mod_res = await fetch(`/courses/${encodeURIComponent(course_id)}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          course_id: course_id,
          credits: credits,
          room: rooms,
          lab: labs,
          conflicts: conflicts,
          faculty: faculty
        })
      });

      if (await check_response_error(mod_res, `"${course_id}" was not found. Please check the course ID and try again.`)) return;

    }

    await load_courses();

  } else if (current_field === "Labs") {

    const name_input = document.getElementById("labs-name");

    if (!name_input) {
      console.error("Lab name input not found");
      return;
    }

    const name = name_input.value.trim();

    if (current_operation === "add") {

      if (!validate_labs_form()) return;

      const add_res = await fetch("/labs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name
        })
      });

      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

    } else if (current_operation === "delete") {

      if (!validate_labs_form()) return;

      const del_res = await fetch(`/labs/${encodeURIComponent(name)}`, {
        method: "DELETE"
      });

      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

    } else if (current_operation === "modify") {

      if (!name) {
        show_field_error(name_input, "Current lab name is required.");
        return;
      }

      const new_name_input = document.getElementById("labs-new-name");
      const new_name = new_name_input ? new_name_input.value.trim() : "";

      if (!new_name) {
        show_field_error(new_name_input, "New lab name is required.");
        return;
      }

      const mod_res = await fetch(`/labs/${encodeURIComponent(name)}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: new_name
        })
      });

      if (await check_response_error(mod_res, `"${name}" was not found. Please check the name and try again.`)) return;

    }

    await load_labs();

  } else if (current_field === "Rooms") {

    const name_input = document.getElementById("rooms-name");

    if (!name_input) {
      console.error("Room name input not found");
      return;
    }

    const name = name_input.value.trim();

    if (current_operation === "add") {

      if (!validate_rooms_form()) return;

      const add_res = await fetch("/rooms", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name
        })
      });

      if (await check_response_error(add_res, `"${name}" could not be added.`)) return;

    } else if (current_operation === "delete") {

      if (!validate_rooms_form()) return;

      const del_res = await fetch(`/rooms/${encodeURIComponent(name)}`, {
        method: "DELETE"
      });

      if (await check_response_error(del_res, `"${name}" was not found. Please check the name and try again.`)) return;

    } else if (current_operation === "modify") {

      if (!name) {
        show_field_error(name_input, "Current room name is required.");
        return;
      }

      const new_name_input = document.getElementById("rooms-new-name");
      const new_name = new_name_input ? new_name_input.value.trim() : "";

      if (!new_name) {
        show_field_error(new_name_input, "New room name is required.");
        return;
      }

      const mod_res = await fetch(`/rooms/${encodeURIComponent(name)}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: new_name
        })
      });

      if (await check_response_error(mod_res, `"${name}" was not found. Please check the name and try again.`)) return;

    }

    await load_rooms();

  }

});

print_button.addEventListener("click", () => {

  window.open("/print_schedules", "_blank");

});

// Listens for file selection on the load input, uploads the file to /load_config,
// and logs the server response.
const file_input = document.getElementById("load");

file_input.addEventListener("change", async function () {
  const file = file_input.files[0];

  const form_data = new FormData();
  form_data.append("file", file);

  const res = await fetch("/load_config", {
    method: "POST",
    body: form_data
  });

  const data = await res.json();
  console.log(data);
});

// Close button: clears and hides the popup, restores pointer events, refocuses active field.
popup_close.addEventListener("click", () => {
  popup_form.innerHTML = "";
  amd_popup.classList.add("popup-hidden");
  wrapper.style.pointerEvents = "all";
  popup_save.style.display = "block";

  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
});

// posts a new faculty member to the API and logs the response.
// Parameters: form_data - object containing faculty fields
async function add_faculty(form_data) {
  const res = await fetch("/faculty", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(form_data)
  });

  const data = await res.json();
  console.log(data);
}


async function load_courses() {
  clear_field_containers();
  navigator_div.innerHTML = "";
  const res = await fetch("/courses");
  const courses = await res.json();

  console.log("courses response:", courses);

  const container = document.getElementById("courses");
  container.innerHTML = "";

  courses.forEach(c => {
    const div = document.createElement("div");
    div.textContent = `${c.course_id} (${c.credits})`;
    container.appendChild(div);
  });

}

async function load_faculty() {
  clear_field_containers();
  navigator_div.innerHTML = "";
  const res = await fetch("/faculty");
  const faculty = await res.json();

  const container = document.getElementById("faculty");
  container.innerHTML = "";

  faculty.forEach(f => {
    const div = document.createElement("div");
    div.textContent = f.name;
    container.appendChild(div);
  });

}


async function load_rooms() {
  clear_field_containers();
  navigator_div.innerHTML = "";
  const res = await fetch("/rooms");
  const rooms = await res.json();

  console.log("rooms response:", rooms);

  const container = document.getElementById("rooms");
  container.innerHTML = "";

  rooms.forEach(r => {
    const div = document.createElement("div");
    div.textContent = r.name;
    container.appendChild(div);
  });
}

async function load_labs() {
  clear_field_containers();
  navigator_div.innerHTML = "";
  const res = await fetch("/labs");
  const labs = await res.json();

  console.log("labs response:", labs);

  const container = document.getElementById("labs");
  container.innerHTML = "";

  labs.forEach(l => {
    const div = document.createElement("div");
    div.textContent = l.name;
    container.appendChild(div);
  });
}

async function generate_schedules() {

  const status = document.getElementById("schedule-status");

  const count = parseInt(
    document.getElementById("schedule-count").value
  );

  const optimize =
    document.getElementById("schedule-optimize").checked;

  status.textContent = "Creating schedules...";

  const res = await fetch("/run_scheduler", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      limit: count,
      optimize: optimize
    })
  });

  const data = await res.json();
  console.log(data);

  if (data.error || data.count === undefined) {
    status.textContent =
      "Config file is empty, cannot generate schedules, please load a config file.";
  }
  else if (data.count === 0) {
    status.textContent =
      "No valid schedules. Please modify config.";
  }
  else {
    schedules_generated = true;
    status.textContent =
      data.count + " schedules generated.";
    view_img.src = "/static/images/view.png";
    print_img.src = "/static/images/print.png";
    print_button.style.color = "#484848";
    view_button.style.color = "#484848";

    // allow printing of schedules now
    view_button.disabled = false;
    print_button.disabled = false;
  }
}

async function load_schedule() {
  clear_field_containers();

  const container = document.getElementById("schedule");

  container.innerHTML = `
    <h3 id="schedule-generator">Schedule Generator</h3>

    <div class="schedule-form-line">
      <label>Number of schedules:</label>
      <input id="schedule-count" type="number" value="10" min="1">
    </div>

    <div class="schedule-form-line">
      <label>Optimize schedules:</label>
      <input id="schedule-optimize" type="checkbox" checked>
    </div>

    <div class="schedule-form-line">
      <button id="generate-schedules">Generate</button>
    </div>

    <hr id="schedule-hr"/>

    <div id="schedule-status">
      Waiting to generate schedules...
    </div>
  `;

  document
    .getElementById("generate-schedules")
    .addEventListener("click", generate_schedules);
}

// Renders the schedule table inside popup_form for the given index and group mode.
// mode is one of: "course", "faculty", "room", "lab".
// Layout mirrors the room-schedule sheet format: day heading, then rows sorted by
// time.  The chosen mode adds an optional sub-heading within each day block.
async function render_schedule_table(index, mode) {

  const res = await fetch(`/schedule/${index}/view/${mode}`);
  const data = await res.json();

  if (data.error) {
    alert(data.error);
    return;
  }

  // Remove everything below the two control rows
  const all_children = Array.from(popup_form.children);
  const control_rows = popup_form.querySelectorAll(".schedule-control-row");
  all_children.forEach(child => {
    if (!child.classList.contains("schedule-control-row")) {
      child.remove();
    }
  });

  const MODE_LABEL = { faculty: "Faculty", room: "Room", lab: "Lab" };

  // ---- Column definitions — the grouped-by column is omitted ----
  const all_cols = [
    { header: "Time", value: slot => slot.is_lab ? `${slot.time} *` : slot.time },
    { header: "Course", value: slot => slot.course },
    { header: "Section", value: slot => slot.section || "—" },
    { header: "Faculty", value: slot => slot.faculty },
    { header: "Room", value: slot => slot.room },
    { header: "Lab", value: slot => slot.lab !== "None" ? slot.lab : "—" },
  ];

  // Drop the column that matches the active grouping mode
  const hidden_col = { faculty: "Faculty", room: "Room", lab: "Lab" }[mode] || null;
  const col_defs = hidden_col
    ? all_cols.filter(c => c.header !== hidden_col)
    : all_cols;

  function make_th(text) {
    const th = document.createElement("th");
    th.textContent = text;
    th.style.borderBottom = "2px solid #989898";
    th.style.padding = "4px 8px";
    th.style.textAlign = "left";
    th.style.fontWeight = "bold";
    return th;
  }

  function make_td(text) {
    const td = document.createElement("td");
    td.textContent = text;
    td.style.padding = "3px 8px";
    td.style.verticalAlign = "top";
    td.style.borderBottom = "1px solid #e0e0e0";
    return td;
  }

  // Outer wrapper so the whole thing scrolls as one
  const wrapper_div = document.createElement("div");
  wrapper_div.style.marginTop = "8px";

  const table = document.createElement("table");
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";

  // Global header — only the visible columns
  const thead = document.createElement("thead");
  const header_row = document.createElement("tr");
  col_defs.forEach(c => header_row.appendChild(make_th(c.header)));
  thead.appendChild(header_row);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");

  data.days.forEach(day_group => {

    // ---- Day heading row (e.g. "Monday") ----
    const day_heading_row = document.createElement("tr");
    const day_td = document.createElement("td");
    day_td.colSpan = col_defs.length;
    day_td.textContent = day_group.day_name;
    day_td.style.fontWeight = "bold";
    day_td.style.paddingTop = "12px";
    day_td.style.paddingBottom = "2px";
    day_td.style.paddingLeft = "8px";
    day_td.style.borderBottom = "1px solid #bbb";
    day_heading_row.appendChild(day_td);
    tbody.appendChild(day_heading_row);

    day_group.sub_groups.forEach(sub => {

      // Optional sub-group heading (e.g. "Room: Roddy 140")
      if (sub.sub_key !== null) {
        const sub_row = document.createElement("tr");
        const sub_td = document.createElement("td");
        sub_td.colSpan = col_defs.length;
        sub_td.textContent = `${MODE_LABEL[data.mode] || ""}: ${sub.sub_key}`;
        sub_td.style.fontStyle = "italic";
        sub_td.style.paddingLeft = "16px";
        sub_td.style.paddingTop = "6px";
        sub_td.style.paddingBottom = "2px";
        sub_td.style.color = "#555";
        sub_row.appendChild(sub_td);
        tbody.appendChild(sub_row);
      }

      sub.slots.forEach(slot => {
        const row = document.createElement("tr");
        col_defs.forEach(c => row.appendChild(make_td(c.value(slot))));
        tbody.appendChild(row);
      });
    });
  });

  table.appendChild(tbody);

  // Small legend for lab marker
  const legend = document.createElement("div");
  legend.style.fontSize = "0.8em";
  legend.style.color = "#666";
  legend.style.marginTop = "6px";
  legend.textContent = "* = lab session";

  wrapper_div.appendChild(table);
  wrapper_div.appendChild(legend);
  popup_form.appendChild(wrapper_div);
}

async function view_schedule(index = 0) {

  popup_save.style.display = "none";

  popup_title.textContent = `Schedule ${index + 1}`;
  popup_form.innerHTML = "";

  // ---- Row 1: schedule number selector ----
  const selector = document.createElement("div");
  selector.className = "form-line schedule-control-row";
  selector.style.display = "flex";
  selector.style.alignItems = "center";
  selector.style.gap = "6px";
  selector.style.marginBottom = "4px";

  const sel_label = document.createElement("label");
  sel_label.textContent = "Schedule number:";

  const num_input = document.createElement("input");
  num_input.type = "number";
  num_input.min = "1";
  num_input.value = index + 1;
  num_input.style.width = "60px";

  const load_btn = document.createElement("button");
  load_btn.id = "schedule-load-button";
  load_btn.textContent = "Load";

  selector.appendChild(sel_label);
  selector.appendChild(num_input);
  selector.appendChild(load_btn);
  popup_form.appendChild(selector);

  // ---- Row 2: group-by selector ----
  const group_row = document.createElement("div");
  group_row.className = "form-line schedule-control-row";
  group_row.style.display = "flex";
  group_row.style.alignItems = "center";
  group_row.style.gap = "6px";
  group_row.style.marginBottom = "8px";

  const group_label = document.createElement("label");
  group_label.textContent = "Group by:";

  const group_select = document.createElement("select");
  group_select.id = "schedule-group-by";
  [
    { value: "course", label: "Course" },
    { value: "faculty", label: "Faculty" },
    { value: "room", label: "Room" },
    { value: "lab", label: "Lab" },
  ].forEach(opt => {
    const o = document.createElement("option");
    o.value = opt.value;
    o.textContent = opt.label;
    group_select.appendChild(o);
  });

  group_row.appendChild(group_label);
  group_row.appendChild(group_select);
  popup_form.appendChild(group_row);

  // ---- Wire up events ----
  let current_index = index;
  let current_mode = "course";

  const refresh = () => render_schedule_table(current_index, current_mode);

  load_btn.addEventListener("click", () => {
    current_index = parseInt(num_input.value) - 1;
    popup_title.textContent = `Schedule ${current_index + 1}`;
    refresh();
  });

  group_select.addEventListener("change", () => {
    current_mode = group_select.value;
    refresh();
  });

  // ---- Initial render ----
  await refresh();

  amd_popup.classList.remove("popup-hidden");
  wrapper.style.pointerEvents = "none";
}

function clear_field_containers() {
  document.getElementById("faculty").innerHTML = "";
  document.getElementById("courses").innerHTML = "";
  document.getElementById("rooms").innerHTML = "";
  document.getElementById("labs").innerHTML = "";
  document.getElementById("schedule").innerHTML = "";
}