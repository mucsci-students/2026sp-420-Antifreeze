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
export function get_chat_button() {
    return document.getElementById("chat-toggle");
}
// Field Buttons
export const faculty_button = document.getElementById("faculty-button");
export const courses_button = document.getElementById("courses-button");
export const labs_button = document.getElementById("labs-button");
export const rooms_button = document.getElementById("rooms-button");
export const schedule_button = document.getElementById("schedule-button");
export const time_slots_button = document.getElementById("time-slots-button");

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
  error_span.textContent = message;

  // If the element is inside an .input-wrapper, attach the error to the
  // wrapper's parent so it appears below the whole row without shifting
  // the remove button sideways.
  const wrapper = input_el.closest(".input-wrapper");
  const anchor = wrapper ?? input_el;
  anchor.insertAdjacentElement("afterend", error_span);
}

// Removes the inline error state (red border + error span) from a given input element.
// Parameters: input_el - the input DOM element
export function clear_field_error(input_el) {
  if (!input_el) return;
  input_el.style.borderColor = "";

  // Check after both the element itself and its wrapper
  const wrapper = input_el.closest(".input-wrapper");
  const anchor = wrapper ?? input_el;
  const next = anchor.nextElementSibling;
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

// Updates add/modify/delete button images based on field and item selection state.
// Add is enabled whenever a field is active. Modify/Delete only light up when an
// item is also selected in the list. item_selected defaults to false.
// Parameters: current_field - active field string or null, item_selected - boolean
export function render_amd_images(current_field, item_selected = false) {
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
    // Add is always available when a field is active
    add_img.src = "/static/images/add.png";
    add_button.style.color = "#484848";
    add_button.disabled = false;

    // Modify and Delete only activate after clicking a specific item
    if (item_selected) {
      modify_img.src = "/static/images/modify.png";
      delete_img.src = "/static/images/delete.png";
      modify_button.style.color = "#484848";
      delete_button.style.color = "#484848";
      modify_button.disabled = false;
      delete_button.disabled = false;
    } else {
      modify_img.src = "/static/images/modify_shadow.png";
      delete_img.src = "/static/images/delete_shadow.png";
      modify_button.style.color = "#808080";
      delete_button.style.color = "#808080";
      modify_button.disabled = true;
      delete_button.disabled = true;
    }
  }
}

// ---------------------------------------------------------------------------
// Field list renderers
// ---------------------------------------------------------------------------

// Cached array of the items currently rendered in the navigator list.
let _list_items = [];

// Returns the full item data object at the given index in the current list.
export function get_list_item(i) { return _list_items[i] ?? null; }

// Builds and renders a clickable <ul> list into navigator_div.
// label_fn(item) produces the display string for each item.
function _make_list(items, label_fn) {
  _list_items = items;
  navigator_div.innerHTML = "";
  const ul = document.createElement("ul");
  ul.className = "navigator-list";
  items.forEach((item, i) => {
    const li = document.createElement("li");
    li.className = "navigator-item";
    li.dataset.index = String(i);
    li.textContent = label_fn(item);
    ul.appendChild(li);
  });
  navigator_div.appendChild(ul);
}

// Highlights the given <li> as selected and removes selection from any other item.
export function select_list_item(li) {
  navigator_div.querySelectorAll(".navigator-item.selected")
    .forEach(el => el.classList.remove("selected"));
  li.classList.add("selected");
}

// Removes the selected highlight from all list items.
export function clear_item_selection() {
  navigator_div.querySelectorAll(".navigator-item.selected")
    .forEach(el => el.classList.remove("selected"));
}

export function render_faculty_list(faculty) {
  main.classList.remove("schedule-view-expanded");
  _make_list(faculty, f => f.name);   // full object stored; label shows name only
}

export function render_courses_list(courses) {
  main.classList.remove("schedule-view-expanded");
  _make_list(courses, c => `${c.course_id} (${c.credits} credits)`);  // full object stored
}

export function render_rooms_list(rooms) {
  main.classList.remove("schedule-view-expanded");
  _make_list(rooms, r => r.name);
}

export function render_labs_list(labs) {
  main.classList.remove("schedule-view-expanded");
  _make_list(labs, l => l.name);
}

// Renders the time slot configuration as two labeled sections (Time Ranges and
// Class Patterns) in the navigator. Each clickable item stores its type,
// parent day (for time ranges), and 0-based index so the controller can
// dispatch the correct API call.
// Parameters: data - { times: {DAY: [{start,spacing,end}]}, classes: [{...}] }
export function render_time_slots_list(data) {
  main.classList.remove("schedule-view-expanded");

  const DAYS = ["MON", "TUE", "WED", "THU", "FRI"];

  // Build a flat items array that the existing click-listener infrastructure
  // can index into via dataset.index.
  const items = [];

  for (const day of DAYS) {
    const ranges = (data.times || {})[day] || [];
    ranges.forEach((r, i) => {
      items.push({ _type: "time", _day: day, _index: i,
                   start: r.start, spacing: r.spacing, end: r.end });
    });
  }

  (data.classes || []).forEach((cls, i) => {
    items.push({ _type: "class", _index: i,
                 credits: cls.credits, meetings: cls.meetings,
                 start_time: cls.start_time || null, disabled: cls.disabled || false });
  });

  _list_items = items;
  navigator_div.innerHTML = "";

  const ul = document.createElement("ul");
  ul.className = "navigator-list";

  // ---- Time Ranges section ----
  const tr_header = document.createElement("li");
  tr_header.className = "navigator-section-header";
  tr_header.textContent = "Time Ranges";
  ul.appendChild(tr_header);

  const time_items = items.filter(it => it._type === "time");
  if (time_items.length === 0) {
    const empty = document.createElement("li");
    empty.className = "navigator-section-empty";
    empty.textContent = "(none)";
    ul.appendChild(empty);
  } else {
    items.forEach((item, idx) => {
      if (item._type !== "time") return;
      const li = document.createElement("li");
      li.className = "navigator-item";
      li.dataset.index = String(idx);
      li.textContent = `${item._day}: ${item.start} \u2013 ${item.end}  (spacing ${item.spacing} min)`;
      ul.appendChild(li);
    });
  }

  // ---- Class Patterns section ----
  const cp_header = document.createElement("li");
  cp_header.className = "navigator-section-header";
  cp_header.textContent = "Class Patterns";
  ul.appendChild(cp_header);

  const class_items = items.filter(it => it._type === "class");
  if (class_items.length === 0) {
    const empty = document.createElement("li");
    empty.className = "navigator-section-empty";
    empty.textContent = "(none)";
    ul.appendChild(empty);
  } else {
    items.forEach((item, idx) => {
      if (item._type !== "class") return;
      const li = document.createElement("li");
      li.className = "navigator-item";
      li.dataset.index = String(idx);
      const meetings_str = (item.meetings || [])
        .map(m => `${m.day} ${m.duration}min${m.lab ? " (lab)" : ""}`)
        .join(", ");
      li.textContent = `${item.credits} credits \u2014 ${meetings_str}${item.disabled ? " [DISABLED]" : ""}`;
      ul.appendChild(li);
    });
  }

  navigator_div.appendChild(ul);
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
export function render_schedule_table(data, _index, mode) {
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
        <option value="course">Day</option>
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
// Classes are absolutely positioned by their actual start/end times so that
// heights are proportional to duration and the time axis has no duplicate labels.
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

  const MODE_TITLE = { faculty: "Faculty", room: "Rooms", lab: "Lab", course: "Day" };
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

  // Compute the global time range from all time slot strings so the axis
  // is consistent across every card.
  let global_min = Infinity, global_max = -Infinity;
  for (const ts of time_slots) {
    const parts = ts.split("-");
    const s = _parse_time_minutes(parts[0].trim());
    const e = _parse_time_minutes(parts.length > 1 ? parts[1].trim() : parts[0].trim());
    if (s < global_min) global_min = s;
    if (e > global_max) global_max = e;
  }
  // Round outward to the nearest 30-minute boundary for clean tick alignment
  global_min = Math.floor(global_min / 30) * 30;
  global_max = Math.ceil(global_max / 30) * 30;

  const PX_PER_MIN  = 2.0;   // vertical scale: pixels per minute
  const TICK_MIN    = 30;    // draw a grid line every 30 minutes
  const HEADER_H    = 26;    // px height of day-name header row
  const BOTTOM_PAD  = 12;    // extra px below last tick so its label isn't clipped
  const total_height = (global_max - global_min) * PX_PER_MIN;

  // Format minutes-since-midnight as "HH:MM"
  function fmt_min(minutes) {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
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

    // Only show days that have at least one event for this group
    const active_days = DAY_ABBREVS.filter(d =>
      group.day_map[d] && Object.keys(group.day_map[d]).length > 0
    );
    const display_days = active_days.length > 0 ? active_days : DAY_ABBREVS;

    // ── Outer row: time-axis column + one column per displayed day ──────────
    const grid_outer = document.createElement("div");
    grid_outer.style.display = "flex";
    grid_outer.style.alignItems = "flex-start";

    // ---- Time-axis column ----
    const time_col = document.createElement("div");
    time_col.style.flexShrink = "0";
    time_col.style.width = "48px";
    time_col.style.display = "flex";
    time_col.style.flexDirection = "column";

    // Blank cell to align vertically with the day-name headers
    const time_blank = document.createElement("div");
    time_blank.style.height = HEADER_H + "px";
    time_blank.style.flexShrink = "0";
    time_col.appendChild(time_blank);

    // Time label strip
    const time_axis = document.createElement("div");
    time_axis.style.position = "relative";
    time_axis.style.height = (total_height + BOTTOM_PAD) + "px";
    for (let t = global_min; t <= global_max; t += TICK_MIN) {
      const lbl = document.createElement("div");
      lbl.style.position = "absolute";
      lbl.style.top = ((t - global_min) * PX_PER_MIN) + "px";
      lbl.style.transform = "translateY(-50%)";
      lbl.style.fontSize = "0.70em";
      lbl.style.color = "#888";
      lbl.style.right = "4px";
      lbl.style.whiteSpace = "nowrap";
      lbl.textContent = fmt_min(t);
      time_axis.appendChild(lbl);
    }
    time_col.appendChild(time_axis);
    grid_outer.appendChild(time_col);

    // ---- One column per displayed day ----
    display_days.forEach(day => {
      const day_wrap = document.createElement("div");
      day_wrap.style.flex = "1";
      day_wrap.style.minWidth = "90px";
      day_wrap.style.display = "flex";
      day_wrap.style.flexDirection = "column";
      day_wrap.style.borderLeft = "1px solid #ccc";

      // Day-name header
      const day_hdr = document.createElement("div");
      day_hdr.style.height = HEADER_H + "px";
      day_hdr.style.display = "flex";
      day_hdr.style.alignItems = "center";
      day_hdr.style.justifyContent = "center";
      day_hdr.style.fontWeight = "bold";
      day_hdr.style.fontSize = "0.78em";
      day_hdr.style.background = "#e8e8e8";
      day_hdr.style.borderBottom = "2px solid #999";
      day_hdr.textContent = DAY_LABELS[day];
      day_wrap.appendChild(day_hdr);

      // Day body — fixed height, relative for absolute children
      const day_body = document.createElement("div");
      day_body.style.position = "relative";
      day_body.style.height = (total_height + BOTTOM_PAD) + "px";
      day_body.style.overflow = "hidden";
      day_body.style.background = "#fff";

      // Horizontal grid lines
      for (let t = global_min; t <= global_max; t += TICK_MIN) {
        const line = document.createElement("div");
        line.style.position = "absolute";
        line.style.top = ((t - global_min) * PX_PER_MIN) + "px";
        line.style.left = "0";
        line.style.right = "0";
        line.style.height = "1px";
        line.style.background = t % 60 === 0 ? "#d0d0d0" : "#efefef";
        day_body.appendChild(line);
      }

      // Absolutely-positioned class blocks
      const day_slots = group.day_map[day] || {};
      for (const [time_str, slots] of Object.entries(day_slots)) {
        const parts = time_str.split("-");
        const start_min = _parse_time_minutes(parts[0].trim());
        const end_min   = _parse_time_minutes(parts.length > 1 ? parts[1].trim() : parts[0].trim());
        const duration  = Math.max(end_min - start_min, 10); // guard against zero-length

        const top_px    = (start_min - global_min) * PX_PER_MIN;
        const height_px = Math.max(duration * PX_PER_MIN - 3, 14);
        const n = slots.length;

        slots.forEach((slot, si) => {
          const block = document.createElement("div");
          block.className = "cal-course-block";
          block.style.position = "absolute";
          block.style.top = top_px + "px";
          block.style.height = height_px + "px";
          block.style.left = `calc(${(si / n) * 100}% + 2px)`;
          block.style.width = `calc(${(1 / n) * 100}% - 4px)`;
          block.style.backgroundColor = course_colors[slot.course] || "#e0e0e0";
          block.style.overflow = "hidden";
          block.style.boxSizing = "border-box";
          block.style.margin = "0";

          const detail = mode === "faculty" ? slot.room
                       : mode === "room"    ? slot.faculty
                       : mode === "lab"     ? slot.faculty
                       :                      slot.faculty;
          const course_label = slot.section ? `${slot.course}.${slot.section}` : slot.course;

          // Always put everything in a tooltip so no info is ever truly lost
          const tooltip_parts = [course_label];
          if (detail && detail !== "None" && detail !== "—") tooltip_parts.push(detail);
          tooltip_parts.push(time_str);
          if (slot.is_lab) tooltip_parts.push("LAB");
          block.title = tooltip_parts.join(" | ");

          // Course ID is always shown
          const id_line = document.createElement("div");
          id_line.className = "cal-course-id";
          id_line.textContent = course_label;
          block.appendChild(id_line);

          // Detail (faculty/room)
          if (detail && detail !== "None" && detail !== "—") {
            const detail_line = document.createElement("div");
            detail_line.className = "cal-course-detail";
            detail_line.textContent = detail;
            block.appendChild(detail_line);
          }

          // Time range
          const time_line = document.createElement("div");
          time_line.className = "cal-course-time";
          time_line.textContent = time_str;
          block.appendChild(time_line);

          if (slot.is_lab) {
            const badge = document.createElement("span");
            badge.className = "cal-lab-badge";
            badge.textContent = "LAB";
            block.appendChild(badge);
          }

          day_body.appendChild(block);
        });
      }

      day_wrap.appendChild(day_body);
      grid_outer.appendChild(day_wrap);
    });

    card.appendChild(grid_outer);
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

// Creates one <select> dropdown row with a remove button.
// Parameters: name - the select name attr, choices - string[], selected_value - pre-selected string
function _create_select_row(name, choices, selected_value = "") {
  const wrapper = document.createElement("div");
  wrapper.className = "input-wrapper";

  const select = document.createElement("select");
  select.name = name;
  select.className = "dynamic-select";

  const blank_opt = document.createElement("option");
  blank_opt.value = "";
  blank_opt.textContent = "— select —";
  select.appendChild(blank_opt);

  choices.forEach(choice => {
    const opt = document.createElement("option");
    opt.value = choice;
    opt.textContent = choice;
    if (choice === selected_value) opt.selected = true;
    select.appendChild(opt);
  });

  const remove_btn = document.createElement("button");
  remove_btn.type = "button";
  remove_btn.id = "remove-button";
  remove_btn.textContent = "-";
  remove_btn.addEventListener("click", () => wrapper.remove());

  select.addEventListener("change", () => clear_field_error(select));

  wrapper.appendChild(select);
  wrapper.appendChild(remove_btn);
  return wrapper;
}

// Wires the "+" button for a dropdown-based dynamic field to append new select rows.
// Parameters: button_id, container_id, name - same as add_dynamic_input,
//             choices - the option strings to show in the dropdown
function _setup_dynamic_select(button_id, container_id, name, choices) {
  const btn = document.getElementById(button_id);
  if (!btn) return;
  btn.addEventListener("click", () => {
    const container = document.getElementById(container_id);
    if (container) container.appendChild(_create_select_row(name, choices));
  });
}

// Fills a dynamic dropdown container with pre-selected rows.
// Parameters: container_id, name, choices - full option list, selected_values - pre-selected string[]
function _fill_dynamic_select_container(container_id, name, choices, selected_values) {
  const container = document.getElementById(container_id);
  if (!container) return;
  container.innerHTML = "";
  const values = selected_values && selected_values.length > 0 ? selected_values : [""];
  values.forEach(val => {
    container.appendChild(_create_select_row(name, choices, val));
  });
}

// Fills a dynamic list container (e.g. rooms, labs) with an array of string values.
// Replaces the single blank input row that the inline HTML already provides.
// Parameters: container_id - id of the .dynamic-container div,
//             name - input name attr, values - string[]
function _fill_dynamic_container(container_id, name, values) {
  if (!values || values.length === 0) return;
  const container = document.getElementById(container_id);
  if (!container) return;
  container.innerHTML = "";
  values.forEach(val => {
    const wrapper = document.createElement("div");
    wrapper.className = "input-wrapper";
    const input = document.createElement("input");
    input.type = "text";
    input.name = name;
    input.value = val;
    const remove_btn = document.createElement("button");
    remove_btn.type = "button";
    remove_btn.id = "remove-button";
    remove_btn.textContent = "-";
    remove_btn.addEventListener("click", () => wrapper.remove());
    wrapper.appendChild(input);
    wrapper.appendChild(remove_btn);
    container.appendChild(wrapper);
  });
}

// Opens the add/modify/delete popup for the currently selected field.
// Shows an error if no field is selected.
// Parameters: action - "Add", "Modify", or "Delete"; current_field - active field string or null
// prefill - optional data object to pre-populate the Modify form fields
// options - optional { rooms, labs, courses, faculty } arrays used to build dropdowns
export function render_edit_popup(action, current_field, prefill = null, options = null) {
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
      case "Faculty": {
        const courses_opts = options?.courses || [];
        const rooms_opts   = options?.rooms   || [];
        const labs_opts    = options?.labs    || [];
        const DAY_OPTS = ["MON", "TUE", "WED", "THU", "FRI"];

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
            <div id="faculty-course-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-course-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Room Preferences:</label>
            <div id="faculty-room-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-room-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Lab Preferences:</label>
            <div id="faculty-lab-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-lab-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Mandatory Days:</label>
            <div id="faculty-mandatory-days-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-mandatory-days">+</button>
          </div>
        `;

        // Time slots stay as free-text inputs
        add_dynamic_input("add-faculty-time-slots", "faculty-time-slots-container", "faculty-time-slot", "e.g. TUE 09:00-12:00");

        // Preferences and mandatory days use dropdowns
        _fill_dynamic_select_container("faculty-course-preferences-container", "faculty-course-preference", courses_opts, []);
        _fill_dynamic_select_container("faculty-room-preferences-container",   "faculty-room-preference",   rooms_opts,   []);
        _fill_dynamic_select_container("faculty-lab-preferences-container",    "faculty-lab-preference",    labs_opts,    []);
        _fill_dynamic_select_container("faculty-mandatory-days-container",     "faculty-mandatory-day",     DAY_OPTS,     []);

        _setup_dynamic_select("add-faculty-course-preferences", "faculty-course-preferences-container", "faculty-course-preference", courses_opts);
        _setup_dynamic_select("add-faculty-room-preferences",   "faculty-room-preferences-container",   "faculty-room-preference",   rooms_opts);
        _setup_dynamic_select("add-faculty-lab-preferences",    "faculty-lab-preferences-container",    "faculty-lab-preference",    labs_opts);
        _setup_dynamic_select("add-faculty-mandatory-days",     "faculty-mandatory-days-container",     "faculty-mandatory-day",     DAY_OPTS);
        break;
      }

      case "Courses": {
        const rooms_opts   = options?.rooms    || [];
        const labs_opts    = options?.labs     || [];
        const courses_opts = options?.courses  || [];
        const faculty_opts = options?.faculty  || [];

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
            <div id="courses-rooms-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-rooms">+</button>
          </div>
          <div class="form-line">
            <label>Labs:</label>
            <div id="courses-labs-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-labs">+</button>
          </div>
          <div class="form-line">
            <label>Conflicts:</label>
            <div id="courses-conflicts-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-conflicts">+</button>
          </div>
          <div class="form-line">
            <label>Faculty:</label>
            <div id="courses-faculty-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-faculty">+</button>
          </div>
        `;

        // Seed each container with one blank dropdown row
        _fill_dynamic_select_container("courses-rooms-container",     "courses-room",     rooms_opts,   []);
        _fill_dynamic_select_container("courses-labs-container",      "courses-lab",      labs_opts,    []);
        _fill_dynamic_select_container("courses-conflicts-container", "courses-conflict", courses_opts, []);
        _fill_dynamic_select_container("courses-faculty-container",   "courses-faculty",  faculty_opts, []);

        // Wire "+" buttons to append new dropdown rows
        _setup_dynamic_select("add-courses-rooms",     "courses-rooms-container",     "courses-room",     rooms_opts);
        _setup_dynamic_select("add-courses-labs",      "courses-labs-container",      "courses-lab",      labs_opts);
        _setup_dynamic_select("add-courses-conflicts", "courses-conflicts-container", "courses-conflict", courses_opts);
        _setup_dynamic_select("add-courses-faculty",   "courses-faculty-container",   "courses-faculty",  faculty_opts);
        break;
      }

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
      case "Faculty": {
        const courses_opts = options?.courses || [];
        const rooms_opts   = options?.rooms   || [];
        const labs_opts    = options?.labs    || [];
        const DAY_OPTS = ["MON", "TUE", "WED", "THU", "FRI"];

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
            <div id="faculty-course-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-course-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Room Preferences:</label>
            <div id="faculty-room-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-room-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Lab Preferences:</label>
            <div id="faculty-lab-preferences-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-lab-preferences">+</button>
          </div>
          <div class="form-line">
            <label>Mandatory Days:</label>
            <div id="faculty-mandatory-days-container" class="dynamic-container"></div>
            <button type="button" id="add-faculty-mandatory-days">+</button>
          </div>
        `;

        add_dynamic_input("add-faculty-time-slots", "faculty-time-slots-container", "faculty-time-slot", "e.g. TUE 09:00-12:00");

        // Prefill values (or blank row if none)
        const pref_courses  = prefill ? Object.keys(prefill.course_preferences || {}) : [];
        const pref_rooms    = prefill ? Object.keys(prefill.room_preferences || {})   : [];
        const pref_labs     = prefill ? Object.keys(prefill.lab_preferences || {})    : [];
        const pref_days     = prefill ? (prefill.mandatory_days || [])                : [];

        _fill_dynamic_select_container("faculty-course-preferences-container", "faculty-course-preference", courses_opts, pref_courses);
        _fill_dynamic_select_container("faculty-room-preferences-container",   "faculty-room-preference",   rooms_opts,   pref_rooms);
        _fill_dynamic_select_container("faculty-lab-preferences-container",    "faculty-lab-preference",    labs_opts,    pref_labs);
        _fill_dynamic_select_container("faculty-mandatory-days-container",     "faculty-mandatory-day",     DAY_OPTS,     pref_days);

        _setup_dynamic_select("add-faculty-course-preferences", "faculty-course-preferences-container", "faculty-course-preference", courses_opts);
        _setup_dynamic_select("add-faculty-room-preferences",   "faculty-room-preferences-container",   "faculty-room-preference",   rooms_opts);
        _setup_dynamic_select("add-faculty-lab-preferences",    "faculty-lab-preferences-container",    "faculty-lab-preference",    labs_opts);
        _setup_dynamic_select("add-faculty-mandatory-days",     "faculty-mandatory-days-container",     "faculty-mandatory-day",     DAY_OPTS);

        if (prefill) {
          document.getElementById("faculty-name").value = prefill.name ?? "";
          document.getElementById("faculty-max-credits").value = prefill.maximum_credits ?? "";
          document.getElementById("faculty-min-credits").value = prefill.minimum_credits ?? "";
          document.getElementById("faculty-unique-course-limit").value = prefill.unique_course_limit ?? "";
          document.getElementById("faculty-max-days").value = prefill.maximum_days ?? "";

          const time_strings = [];
          for (const [day, ranges] of Object.entries(prefill.times || {})) {
            for (const r of ranges) time_strings.push(`${day} ${r}`);
          }
          _fill_dynamic_container("faculty-time-slots-container", "faculty-time-slot", time_strings);
        }
        break;
      }

      case "Courses": {
        const rooms_opts   = options?.rooms    || [];
        const labs_opts    = options?.labs     || [];
        const courses_opts = options?.courses  || [];
        const faculty_opts = options?.faculty  || [];

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
            <div id="courses-rooms-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-rooms">+</button>
          </div>
          <div class="form-line">
            <label>Labs:</label>
            <div id="courses-labs-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-labs">+</button>
          </div>
          <div class="form-line">
            <label>Conflicts:</label>
            <div id="courses-conflicts-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-conflicts">+</button>
          </div>
          <div class="form-line">
            <label>Faculty:</label>
            <div id="courses-faculty-container" class="dynamic-container"></div>
            <button type="button" id="add-courses-faculty">+</button>
          </div>
        `;

        // Pre-populate with existing values (prefill) or one blank row
        _fill_dynamic_select_container("courses-rooms-container",     "courses-room",     rooms_opts,   prefill?.room      || []);
        _fill_dynamic_select_container("courses-labs-container",      "courses-lab",      labs_opts,    prefill?.lab       || []);
        _fill_dynamic_select_container("courses-conflicts-container", "courses-conflict", courses_opts, prefill?.conflicts || []);
        _fill_dynamic_select_container("courses-faculty-container",   "courses-faculty",  faculty_opts, prefill?.faculty   || []);

        _setup_dynamic_select("add-courses-rooms",     "courses-rooms-container",     "courses-room",     rooms_opts);
        _setup_dynamic_select("add-courses-labs",      "courses-labs-container",      "courses-lab",      labs_opts);
        _setup_dynamic_select("add-courses-conflicts", "courses-conflicts-container", "courses-conflict", courses_opts);
        _setup_dynamic_select("add-courses-faculty",   "courses-faculty-container",   "courses-faculty",  faculty_opts);

        if (prefill) {
          document.getElementById("courses-id").value = prefill.course_id ?? "";
          document.getElementById("courses-credits").value = prefill.credits ?? "";
        }
        break;
      }

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
        if (prefill) {
          document.getElementById("labs-name").value = prefill.name ?? "";
        }
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
        if (prefill) {
          document.getElementById("rooms-name").value = prefill.name ?? "";
        }
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
// Time Slots popup helpers
// ---------------------------------------------------------------------------

const _TS_DAY_OPTS = ["MON", "TUE", "WED", "THU", "FRI"];

// Creates one meeting row for the class-pattern form.
// Row layout: [Day dropdown] [Duration input] [Lab checkbox label] [-]
// Parameters: selected_day - pre-selected day string (or "" for blank),
//             duration - pre-filled duration value (or "" for blank),
//             lab - whether the lab checkbox should be checked
// Returns: div.input-wrapper element ready to append to the meetings container
function _create_meeting_row(selected_day = "", duration = "", lab = false) {
  const wrapper = document.createElement("div");
  wrapper.className = "input-wrapper ts-meeting-row";

  const day_sel = document.createElement("select");
  day_sel.name = "ts-meeting-day";
  day_sel.className = "dynamic-select";
  const blank = document.createElement("option");
  blank.value = ""; blank.textContent = "Day";
  day_sel.appendChild(blank);
  _TS_DAY_OPTS.forEach(d => {
    const opt = document.createElement("option");
    opt.value = d; opt.textContent = d;
    if (d === selected_day) opt.selected = true;
    day_sel.appendChild(opt);
  });

  const dur_input = document.createElement("input");
  dur_input.type = "number";
  dur_input.name = "ts-meeting-duration";
  dur_input.min = "1";
  dur_input.placeholder = "min";
  dur_input.style.width = "60px";
  if (duration !== "") dur_input.value = duration;

  const lab_label = document.createElement("label");
  lab_label.style.display = "flex";
  lab_label.style.alignItems = "center";
  lab_label.style.gap = "4px";
  lab_label.style.fontSize = "0.85em";
  const lab_cb = document.createElement("input");
  lab_cb.type = "checkbox";
  lab_cb.name = "ts-meeting-lab";
  if (lab) lab_cb.checked = true;
  lab_label.appendChild(lab_cb);
  lab_label.appendChild(document.createTextNode("Lab"));

  const remove_btn = document.createElement("button");
  remove_btn.type = "button";
  remove_btn.id = "remove-button";
  remove_btn.textContent = "-";
  remove_btn.addEventListener("click", () => wrapper.remove());

  wrapper.appendChild(day_sel);
  wrapper.appendChild(dur_input);
  wrapper.appendChild(lab_label);
  wrapper.appendChild(remove_btn);
  return wrapper;
}

// Returns the inner HTML string for the time-range sub-form fields
// (day, start, spacing, end). Pre-populates values when prefill is given.
// Parameters: prefill - optional item data object ({ _day, start, spacing, end })
// Returns: HTML string
function _ts_time_range_html(prefill = null) {
  const day_options = _TS_DAY_OPTS.map(d =>
    `<option value="${d}"${prefill && prefill._day === d ? " selected" : ""}>${d}</option>`
  ).join("");
  return `
    <div class="form-line">
      <label for="ts-day">Day:</label>
      <select id="ts-day">${day_options}</select>
    </div>
    <div class="form-line">
      <label for="ts-start">Start (HH:MM):</label>
      <input type="text" id="ts-start" placeholder="08:00" value="${prefill ? prefill.start : ""}"/>
    </div>
    <div class="form-line">
      <label for="ts-spacing">Spacing (min):</label>
      <input type="number" id="ts-spacing" min="1" placeholder="30" value="${prefill ? prefill.spacing : ""}"/>
    </div>
    <div class="form-line">
      <label for="ts-end">End (HH:MM):</label>
      <input type="text" id="ts-end" placeholder="17:00" value="${prefill ? prefill.end : ""}"/>
    </div>
  `;
}

// Returns the inner HTML string for the class-pattern sub-form skeleton
// (credits, meetings container, optional start_time, disabled checkbox).
// The meetings container is populated separately by _setup_ts_meetings.
// Parameters: prefill - optional item data object ({ credits, start_time, disabled })
// Returns: HTML string
function _ts_class_pattern_html(prefill = null) {
  const start_val = prefill && prefill.start_time ? prefill.start_time : "";
  const disabled_attr = prefill && prefill.disabled ? " checked" : "";
  return `
    <div class="form-line">
      <label for="ts-credits">Credits:</label>
      <input type="number" id="ts-credits" min="1" placeholder="3" value="${prefill ? prefill.credits : ""}"/>
    </div>
    <div class="form-line">
      <label>Meetings:</label>
      <div id="ts-meetings-container" class="dynamic-container"></div>
      <button type="button" id="ts-add-meeting">+</button>
    </div>
    <div class="form-line">
      <label for="ts-class-start-time">Start Time (optional):</label>
      <input type="text" id="ts-class-start-time" placeholder="08:00" value="${start_val}"/>
    </div>
    <div class="form-line">
      <label for="ts-disabled">Disabled:</label>
      <input type="checkbox" id="ts-disabled"${disabled_attr}/>
    </div>
  `;
}

// Fills the meetings container with rows from prefill (or one blank row
// when no prefill is given), then wires the + button to append more rows.
// Must be called after _ts_class_pattern_html has been inserted into the DOM.
// Parameters: prefill - optional item data object with a meetings array
//             ({ meetings: [{day, duration, lab}, ...] })
function _setup_ts_meetings(prefill = null) {
  const container = document.getElementById("ts-meetings-container");
  if (!container) return;

  if (prefill && prefill.meetings && prefill.meetings.length > 0) {
    prefill.meetings.forEach(m => {
      container.appendChild(_create_meeting_row(m.day, m.duration, m.lab));
    });
  } else {
    container.appendChild(_create_meeting_row());
  }

  const add_btn = document.getElementById("ts-add-meeting");
  if (add_btn) {
    add_btn.addEventListener("click", () => {
      container.appendChild(_create_meeting_row());
    });
  }
}

// Renders the Add Time Slots popup: a type selector toggles between the
// time-range sub-form and the class-pattern sub-form.
export function render_add_time_slots_popup() {
  popup_title.textContent = "Add Time Slots";
  popup_form.innerHTML = `
    <div class="form-line">
      <label for="ts-add-type">Type:</label>
      <select id="ts-add-type">
        <option value="time">Time Range</option>
        <option value="class">Class Pattern</option>
      </select>
    </div>
    <hr/>
    <div id="ts-time-range-section">${_ts_time_range_html()}</div>
    <div id="ts-class-section" style="display:none">${_ts_class_pattern_html()}</div>
  `;

  _setup_ts_meetings();

  document.getElementById("ts-add-type").addEventListener("change", (e) => {
    const is_time = e.target.value === "time";
    document.getElementById("ts-time-range-section").style.display = is_time ? "" : "none";
    document.getElementById("ts-class-section").style.display    = is_time ? "none" : "";
  });

  amd_popup.classList.remove("popup-hidden");
  wrapper.style.pointerEvents = "none";
}

// Renders the Modify Time Slots popup pre-filled with the selected item's data.
// prefill must include _type ("time" or "class") and the relevant fields.
export function render_modify_time_slots_popup(prefill) {
  popup_title.textContent = "Modify Time Slots";

  if (!prefill || prefill._type === "time") {
    popup_form.innerHTML = _ts_time_range_html(prefill);
    if (prefill) {
      // Day is fixed for modify (route uses the original day); show it read-only
      const day_sel = document.getElementById("ts-day");
      if (day_sel) day_sel.disabled = true;
    }
  } else {
    popup_form.innerHTML = _ts_class_pattern_html(prefill);
    _setup_ts_meetings(prefill);
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
  else if (current_field === "Time Slots") time_slots_button.focus();
}