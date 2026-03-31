// ---------------------------------------------------------------------------
// VIEW
//    DOM element references and all view rendering/display functions
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// DOM Elements
// ---------------------------------------------------------------------------

// Wrapper
export const wrapper = document.getElementById("wrapper");

// Navigation Buttons
export const load_button = document.getElementById("load-button");
export const save_button = document.getElementById("save-button");
export const back_button = document.getElementById("back-button");
export const forward_button = document.getElementById("forward-button");
export const add_button = document.getElementById("add-button");
export const modify_button = document.getElementById("modify-button");
export const delete_button = document.getElementById("delete-button");
export const view_button = document.getElementById("view-button");
export const print_button = document.getElementById("print-button");

// Field Buttons
export const faculty_button = document.getElementById("faculty-button");
export const courses_button = document.getElementById("courses-button");
export const labs_button = document.getElementById("labs-button");
export const rooms_button = document.getElementById("rooms-button");
export const schedule_button = document.getElementById("schedule-button");

// Images inside buttons
export const back_img = back_button.querySelector("img");
export const forward_img = forward_button.querySelector("img");
export const add_img = add_button.querySelector("img");
export const modify_img = modify_button.querySelector("img");
export const delete_img = delete_button.querySelector("img");
export const view_img = view_button.querySelector("img");
export const print_img = print_button.querySelector("img");

// Whitespace where information is printed
export const navigator_div = document.querySelector(".navigator");
export const main = document.querySelector(".main");

// Navigation bar and outer assets
export const nav_bar = document.querySelector(".nav-bar");
export const top_bar = document.querySelector(".top-bar");
export const team_name = document.querySelector(".team-name");
export const gui_wrapper = document.getElementById("wrapper");
export const config_name = document.getElementById("config-name");

// Popup elements
export const amd_popup = document.getElementById("amd-popup");
export const popup_save = document.getElementById("popup-save");
export const popup_title = document.getElementById("popup-title");
export const popup_form = document.getElementById("popup-form");
export const popup_close = document.getElementById("popup-close");
export const popup_box = document.querySelector(".popup-box");
export const popup_header = document.getElementById("popup-header");

// File input when loading a config
export const file_input = document.getElementById("load");

// ---------------------------------------------------------------------------
// Inline error helpers
// ---------------------------------------------------------------------------

// Displays an inline error message directly below a given input element.
// Highlights the input border red and inserts an error span after it.
// Clears any pre-existing error on that input first.
// Parameters: input_el - the input DOM element, message - error string to display
export function show_field_error(input_el, message) {
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
export function clear_field_error(input_el) {
  if (!input_el) return;
  input_el.style.borderColor = "";
  const next = input_el.nextElementSibling;
  if (next && next.classList.contains("field-error")) {
    next.remove();
  }
}

// Clears all inline field errors currently visible in the popup form.
export function clear_all_errors() {
  popup_form.querySelectorAll(".field-error").forEach(el => el.remove());
  popup_form.querySelectorAll("input").forEach(el => (el.style.borderColor = ""));
}

// ---------------------------------------------------------------------------
// Dynamic input helpers
// ---------------------------------------------------------------------------

// Adds a single dynamic input row to a container when its associated button is clicked.
// Each row contains a text input and a remove button.
// Parameters: button_id, container_id, name (input name attr), placeholder
export function add_dynamic_input(button_id, container_id, name, placeholder) {
  const button = document.getElementById(button_id);
  if (!button) return;

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
export function setup_dynamic_fields(fields) {
  fields.forEach(({ button_id, container_id, name, placeholder }) => {
    add_dynamic_input(button_id, container_id, name, placeholder);
  });
}

// ---------------------------------------------------------------------------
// Button state rendering
// ---------------------------------------------------------------------------

// Updates back and forward button images based on stack state.
// Dims buttons when their respective stacks are empty.
// Parameters: back_stack, forward_stack - the current history arrays
export function render_button_images(back_stack, forward_stack) {
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

// Updates add/modify/delete button images and colors based on whether a field is selected.
// Dims buttons when no field is active.
// Parameters: current_field - the currently selected field string or null
export function render_amd_images(current_field) {
  if (current_field == null || current_field == "Schedule") {
    add_img.src = "/static/images/add_shadow.png";
    modify_img.src = "/static/images/modify_shadow.png";
    delete_img.src = "/static/images/delete_shadow.png";
    add_button.style.color = "#808080";
    modify_button.style.color = "#808080";
    delete_button.style.color = "#808080";

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

    add_button.disabled = false;
    modify_button.disabled = false;
    delete_button.disabled = false;
  }
}

// ---------------------------------------------------------------------------
// Field list renderers
// ---------------------------------------------------------------------------

export function render_faculty_list(faculty) {
  main.classList.remove("schedule-view-expanded");
  let html = "<ul>";
  faculty.forEach(f => { html += `<li>${f.name}</li>`; });
  html += "</ul>";
  navigator_div.innerHTML = html;
}

export function render_courses_list(courses) {
  main.classList.remove("schedule-view-expanded");
  let html = "<ul>";
  courses.forEach(c => { html += `<li>${c.course_id} (${c.credits} credits)</li>`; });
  html += "</ul>";
  navigator_div.innerHTML = html;
}

export function render_rooms_list(rooms) {
  main.classList.remove("schedule-view-expanded");
  let html = "<ul>";
  rooms.forEach(r => { html += `<li>${r.name}</li>`; });
  html += "</ul>";
  navigator_div.innerHTML = html;
}

export function render_labs_list(labs) {
  main.classList.remove("schedule-view-expanded");
  let html = "<ul>";
  labs.forEach(l => { html += `<li>${l.name}</li>`; });
  html += "</ul>";
  navigator_div.innerHTML = html;
}

export function render_load_error(field, message) {
  navigator_div.innerHTML = `<p style="color:red;">Error loading ${field}: ${message}</p>`;
}

export function render_navigator_empty() {
  navigator_div.innerHTML = "";
}

export function clear_field_containers() {
  document.getElementById("faculty").innerHTML = "";
  document.getElementById("courses").innerHTML = "";
  document.getElementById("rooms").innerHTML = "";
  document.getElementById("labs").innerHTML = "";
  document.getElementById("schedule").innerHTML = "";
}

// ---------------------------------------------------------------------------
// Schedule renderers
// ---------------------------------------------------------------------------

export function render_schedule_form(count = 10, optimize = true) {
  main.classList.remove("schedule-view-expanded");
  navigator_div.innerHTML = `
    <h3 id="schedule-generator">Schedule Generator</h3>
    <div class="schedule-form-line">
      <label>Number of schedules:</label>
      <input id="schedule-count" type="number" value="${count}" min="1">
    </div>
    <div class="schedule-form-line">
      <label>Optimize schedules:</label>
      <input id="schedule-optimize" type="checkbox" ${optimize ? "checked" : ""}>
    </div>
    <div class="schedule-form-line">
      <button id="generate-schedules">Generate</button>
    </div>
    <hr id="schedule-hr"/>
    <div id="schedule-status">Waiting to generate schedules...</div>
  `;
}

export function render_schedule_status(count, optimize, status_message) {
  navigator_div.innerHTML = `
    <h3 id="schedule-generator">Schedule Generator</h3>
    <div class="schedule-form-line">
      <label>Number of schedules:</label>
      <input id="schedule-count" type="number" value="${count}" min="1">
    </div>
    <div class="schedule-form-line">
      <label>Optimize schedules:</label>
      <input id="schedule-optimize" type="checkbox" ${optimize ? "checked" : ""}>
    </div>
    <div class="schedule-form-line">
      <button id="generate-schedules">Generate</button>
    </div>
    <hr id="schedule-hr"/>
    <div id="schedule-status">${status_message}</div>
    <div class="progress-bar-container">
      <div id="progress-bar" class="w3-container w3-green">0%</div>
    </div>
  `;
}

export function render_progress_bar(count, status_message) {
  var progress_bar = document.getElementById("progress-bar");
  var width = 0;
  var id;

  if (count <= 2) { id = setInterval(frame, 100); }
  if (count <= 4) { id = setInterval(frame, 150); }
  if (count <= 6) { id = setInterval(frame, 200); }
  if (count <= 8) { id = setInterval(frame, 250); }
  if (count <= 10) { id = setInterval(frame, 300); }
  if (count > 10) { id = setInterval(frame, 400); }

  function frame() {
    if (status_message.localeCompare("Creating schedules...") == 0) {
      if (width >= 99) {
        clearInterval(id);
      }
      else {
        width++;
        progress_bar.style.width = width + '%';
        progress_bar.innerHTML = width * 1 + '%';
      }
    }
  }

  progress_bar.style.width = '100%';
  progress_bar.innerHTML = '100%';
}

export function render_schedules_generated_buttons() {
  view_img.src = "/static/images/view.png";
  print_img.src = "/static/images/print.png";
  print_button.style.color = "#484848";
  view_button.style.color = "#484848";
  view_button.disabled = false;
  print_button.disabled = false;
}

// Renders the schedule table inside popup_form for the given data and group mode.
// mode is one of: "course", "faculty", "room", "lab".
// Parameters: data - schedule data object from the API, index - schedule index, mode - grouping mode
export function render_schedule_table(data, index, mode) {
  // Remove everything below the two control rows
  const all_children = Array.from(popup_form.children);
  all_children.forEach(child => {
    if (!child.classList.contains("schedule-control-row")) {
      child.remove();
    }
  });

  const MODE_LABEL = { faculty: "Faculty", room: "Room", lab: "Lab" };

  // Column definitions — the grouped-by column is omitted
  const all_cols = [
    { header: "Time", value: slot => slot.is_lab ? `${slot.time} *` : slot.time },
    { header: "Course", value: slot => slot.course },
    { header: "Section", value: slot => slot.section || "—" },
    { header: "Faculty", value: slot => slot.faculty },
    { header: "Room", value: slot => slot.room },
    { header: "Lab", value: slot => slot.lab !== "None" ? slot.lab : "—" },
  ];

  const hidden_col = { faculty: "Faculty", room: "Room", lab: "Lab" }[mode] || null;
  const col_defs = hidden_col ? all_cols.filter(c => c.header !== hidden_col) : all_cols;

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

  const wrapper_div = document.createElement("div");
  wrapper_div.style.marginTop = "8px";

  const table = document.createElement("table");
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";

  const thead = document.createElement("thead");
  const header_row = document.createElement("tr");
  col_defs.forEach(c => header_row.appendChild(make_th(c.header)));
  thead.appendChild(header_row);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");

  data.days.forEach(day_group => {
    // Day heading row
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
      // Optional sub-group heading
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

  const legend = document.createElement("div");
  legend.style.fontSize = "0.8em";
  legend.style.color = "#666";
  legend.style.marginTop = "6px";
  legend.textContent = "* = lab session";

  wrapper_div.appendChild(table);
  wrapper_div.appendChild(legend);
  popup_form.appendChild(wrapper_div);
}

// Builds the schedule view popup with number selector and group-by controls.
// Parameters: index - 0-based schedule index, on_load_click(newIndex), on_group_change(newMode),
//             schedule_count - optional total number of schedules (shows "of N" label when provided)
export function render_view_schedule_popup(index, on_load_click, on_group_change, schedule_count = null) {
  popup_save.style.display = "none";
  popup_title.textContent = `Schedule ${index + 1}`;
  popup_form.innerHTML = "";

  // Row 1: schedule number selector
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
  if (schedule_count !== null) num_input.max = String(schedule_count);

  const of_label = document.createElement("span");
  if (schedule_count !== null) {
    of_label.textContent = `of ${schedule_count}`;
    of_label.style.color = "#666";
    of_label.style.fontSize = "0.9em";
  }

  const load_btn = document.createElement("button");
  load_btn.id = "schedule-load-button";
  load_btn.textContent = "Load";

  selector.appendChild(sel_label);
  selector.appendChild(num_input);
  if (schedule_count !== null) selector.appendChild(of_label);
  selector.appendChild(load_btn);
  popup_form.appendChild(selector);

  // Row 2: group-by selector
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

  load_btn.addEventListener("click", () => on_load_click(parseInt(num_input.value) - 1));
  group_select.addEventListener("change", () => on_group_change(group_select.value));
}

// ---------------------------------------------------------------------------
// Inline schedule view renderers
// ---------------------------------------------------------------------------

// Renders the schedule viewer controls (schedule selector + group-by) directly
// into navigator_div, replacing whatever was there. Appends an empty
// #schedule-calendar-container div where render_schedule_calendar() will write.
// Parameters: same as render_view_schedule_popup
export function render_schedule_view_inline(index, on_load_click, on_group_change, schedule_count = null) {
  const max_attr = schedule_count !== null ? ` max="${schedule_count}"` : "";
  const of_html = schedule_count !== null
    ? `<span class="schedule-of-label">of ${schedule_count}</span>` : "";

  main.classList.add("schedule-view-expanded");

  navigator_div.innerHTML = `
    <h3 id="schedule-generator">Schedule Viewer</h3>
    <div class="schedule-control-row">
      <label>Schedule number:</label>
      <input type="number" id="schedule-num-input" min="1" value="${index + 1}"${max_attr} style="width:60px">
      ${of_html}
      <button id="schedule-load-btn">Load</button>
    </div>
    <div class="schedule-control-row">
      <label>Group by:</label>
      <select id="schedule-group-by">
        <option value="faculty">Faculty</option>
        <option value="room">Room</option>
        <option value="lab">Lab</option>
        <option value="course">Course</option>
      </select>
    </div>
    <div id="schedule-calendar-container"></div>
  `;

  document.getElementById("schedule-load-btn").addEventListener("click", () => {
    const val = parseInt(document.getElementById("schedule-num-input").value);
    on_load_click(isNaN(val) ? 0 : val - 1);
  });
  document.getElementById("schedule-group-by").addEventListener("change", () => {
    on_group_change(document.getElementById("schedule-group-by").value);
  });
}

// Renders calendar grids into #schedule-calendar-container.
// For faculty/room/lab modes: one card per entity with a Mon–Fri grid.
// For course mode: a single grid with all courses.
// Parameters: data - schedule view object from API or get_csv_schedule_view,
//             index - 0-based schedule index, mode - grouping mode string
export function render_schedule_calendar(data, index, mode) {
  const container = document.getElementById("schedule-calendar-container");
  if (!container) return;
  container.innerHTML = "";

  const { groups, time_slots, DAY_ABBREVS, DAY_LABELS } = _transform_to_calendar(data);

  if (groups.length === 0 || time_slots.length === 0) {
    container.textContent = "No schedule data to display.";
    return;
  }

  const MODE_TITLE = { faculty: "Faculty", room: "Rooms", lab: "Lab", course: "Course" };
  const section_title = document.createElement("h4");
  section_title.className = "schedule-section-title";
  section_title.textContent = `Schedule ${index + 1} — grouped by ${MODE_TITLE[mode] || mode}`;
  container.appendChild(section_title);

  const grid_wrap = document.createElement("div");
  grid_wrap.className = "schedule-calendar-grid";
  container.appendChild(grid_wrap);

  // Assign a pastel color per course ID
  const PALETTE = [
    "#b8deff", "#b8f0d8", "#ffeab8", "#ffc8d0", "#dac8ff",
    "#b8f0f0", "#ffd8b8", "#c8e8b8", "#ffd0f0", "#c8d8ff",
  ];
  const course_colors = {};
  let color_idx = 0;
  for (const group of groups) {
    for (const day_slots of Object.values(group.day_map)) {
      for (const slot_list of Object.values(day_slots)) {
        for (const slot of slot_list) {
          if (!course_colors[slot.course]) {
            course_colors[slot.course] = PALETTE[color_idx % PALETTE.length];
            color_idx++;
          }
        }
      }
    }
  }

  groups.forEach(group => {
    const card = document.createElement("div");
    card.className = "schedule-calendar-card";

    if (group.name !== null) {
      const title = document.createElement("div");
      title.className = "calendar-card-title";
      title.textContent = group.name;
      card.appendChild(title);
    }

    const table = document.createElement("table");
    table.className = "calendar-table";

    // Only show days that have at least one event for this group
    const active_days = DAY_ABBREVS.filter(d =>
      group.day_map[d] && Object.keys(group.day_map[d]).length > 0
    );
    const display_days = active_days.length > 0 ? active_days : DAY_ABBREVS;

    // Header row
    const thead = document.createElement("thead");
    const head_row = document.createElement("tr");
    const blank_th = document.createElement("th");
    blank_th.className = "cal-time-header";
    head_row.appendChild(blank_th);
    display_days.forEach(day => {
      const th = document.createElement("th");
      th.className = "cal-day-header";
      th.textContent = DAY_LABELS[day];
      head_row.appendChild(th);
    });
    thead.appendChild(head_row);
    table.appendChild(thead);

    // One row per unique time slot
    const tbody = document.createElement("tbody");
    time_slots.forEach(time => {
      const row = document.createElement("tr");

      const time_td = document.createElement("td");
      time_td.className = "cal-time-cell";
      time_td.textContent = time.split("-")[0].trim();
      row.appendChild(time_td);

      display_days.forEach(day => {
        const cell_td = document.createElement("td");
        cell_td.className = "cal-day-cell";

        const slots = (group.day_map[day] && group.day_map[day][time]) || [];
        slots.forEach(slot => {
          const block = document.createElement("div");
          block.className = "cal-course-block";
          block.style.backgroundColor = course_colors[slot.course] || "#e0e0e0";

          const id_line = document.createElement("div");
          id_line.className = "cal-course-id";
          id_line.textContent = slot.section ? `${slot.course}.${slot.section}` : slot.course;
          block.appendChild(id_line);

          // Secondary detail depends on group mode
          const detail = mode === "faculty" ? slot.room
                       : mode === "room"    ? slot.faculty
                       : mode === "lab"     ? slot.faculty
                       :                      slot.faculty;
          if (detail && detail !== "None" && detail !== "—") {
            const detail_line = document.createElement("div");
            detail_line.className = "cal-course-detail";
            detail_line.textContent = detail;
            block.appendChild(detail_line);
          }

          const time_line = document.createElement("div");
          time_line.className = "cal-course-time";
          time_line.textContent = time;
          block.appendChild(time_line);

          if (slot.is_lab) {
            const badge = document.createElement("span");
            badge.className = "cal-lab-badge";
            badge.textContent = "LAB";
            block.appendChild(badge);
          }

          cell_td.appendChild(block);
        });

        row.appendChild(cell_td);
      });

      tbody.appendChild(row);
    });

    table.appendChild(tbody);
    card.appendChild(table);
    grid_wrap.appendChild(card);
  });
}

// Transforms API schedule data { mode, days } into calendar-grid format.
// Returns { groups, time_slots, DAY_ABBREVS, DAY_LABELS }.
function _transform_to_calendar(data) {
  const DAY_ABBREVS = ["MON", "TUE", "WED", "THU", "FRI"];
  const DAY_LABELS = { MON: "Monday", TUE: "Tuesday", WED: "Wednesday", THU: "Thursday", FRI: "Friday" };
  // Reverse lookup used when day_group only has day_name (CSV mode)
  const DAY_NAME_TO_ABBREV = { Monday: "MON", Tuesday: "TUE", Wednesday: "WED", Thursday: "THU", Friday: "FRI" };

  // Flatten all slots, injecting the day abbreviation from the parent day_group.
  // The backend includes day_group.day ("MON"); the CSV path uses day_group.day_name ("Monday").
  // Individual slot objects from the backend do NOT carry a day field.
  const all_slots = [];
  for (const day_group of data.days) {
    const day_abbrev = day_group.day || DAY_NAME_TO_ABBREV[day_group.day_name] || "";
    for (const sg of day_group.sub_groups) {
      for (const slot of sg.slots) {
        all_slots.push({ ...slot, day: slot.day || day_abbrev });
      }
    }
  }

  // Unique time strings sorted by start time
  const time_set = new Set(all_slots.map(s => s.time));
  const time_slots = [...time_set].sort((a, b) =>
    _parse_time_minutes(a.split("-")[0].trim()) - _parse_time_minutes(b.split("-")[0].trim())
  );

  const mode = data.mode;
  let groups;
  if (mode === "course") {
    groups = [{ name: null, day_map: _build_day_time_map(all_slots) }];
  } else {
    const key_fn = mode === "faculty" ? s => s.faculty
                 : mode === "room"    ? s => s.room
                 :                      s => s.lab;
    const group_map = {};
    for (const slot of all_slots) {
      const key = key_fn(slot);
      if (!group_map[key]) group_map[key] = [];
      group_map[key].push(slot);
    }
    groups = Object.entries(group_map)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([name, slots]) => ({ name, day_map: _build_day_time_map(slots) }));
  }

  return { groups, time_slots, DAY_ABBREVS, DAY_LABELS };
}

// Builds a nested { day: { time: [slots] } } map from a flat slots array.
function _build_day_time_map(slots) {
  const day_map = {};
  for (const slot of slots) {
    if (!day_map[slot.day]) day_map[slot.day] = {};
    if (!day_map[slot.day][slot.time]) day_map[slot.day][slot.time] = [];
    day_map[slot.day][slot.time].push(slot);
  }
  return day_map;
}

// Parses a time string to minutes since midnight.
// Handles "9:00", "09:00", "9:00AM", "10:00AM" formats.
function _parse_time_minutes(t) {
  const is_pm = /PM/i.test(t);
  const is_am = /AM/i.test(t);
  const clean = t.replace(/[APMapm\s]/g, "");
  const parts = clean.split(":");
  let hours = parseInt(parts[0]) || 0;
  const mins = parseInt(parts[1]) || 0;
  if (is_pm && hours < 12) hours += 12;
  if (is_am && hours === 12) hours = 0;
  return hours * 60 + mins;
}

// ---------------------------------------------------------------------------
// Popup form renderers (Add / Modify / Delete)
// ---------------------------------------------------------------------------

// Opens the add/modify/delete popup for the currently selected field.
// Shows an error if no field is selected.
// Parameters: action - "Add", "Modify", or "Delete"; current_field - active field string or null
export function render_edit_popup(action, current_field) {
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

// ---------------------------------------------------------------------------
// Popup helpers
// ---------------------------------------------------------------------------

export function show_popup() {
  amd_popup.classList.remove("popup-hidden");
  wrapper.style.pointerEvents = "none";
}

export function hide_popup() {
  popup_form.innerHTML = "";
  amd_popup.classList.add("popup-hidden");
  wrapper.style.pointerEvents = "all";
  popup_save.style.display = "block";
}

// Focuses the field button matching the current_field string.
export function focus_field_button(current_field) {
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
  else if (current_field === "Schedule") schedule_button.focus();
}