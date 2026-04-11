// ===============================
// MODEL
//    Application states and all API/data operations
// ===============================

// ---------------------------------------------------------------------------
// States
// ---------------------------------------------------------------------------

// Holds contents of loaded file
export let loaded_file_content = null;
export let loaded_file_extension = null;

// Field we are currently editing
export let current_field = null;
export let current_operation = null;
export let schedules_generated = false;

// History stacks
export let back_stack = [];
export let forward_stack = [];
export let current_content = null;

// CSV schedule state (populated when a CSV file is loaded instead of generated)
export let csv_schedules = [];
export let csv_mode = false;

// The full data object of the currently selected list item (faculty, course, lab, or room)
export let selected_item_data = null;

// ---------------------------------------------------------------------------
// State setters
// ---------------------------------------------------------------------------

export function set_current_field(val) { current_field = val; }
export function set_current_operation(val) { current_operation = val; }
export function set_schedules_generated(val) { schedules_generated = val; }
export function set_current_content(val) { current_content = val; }
export function set_loaded_file_content(val) { loaded_file_content = val; }
export function set_csv_schedules(val) { csv_schedules = val; }
export function set_csv_mode(val) { csv_mode = val; }
export function set_selected_item_data(val) { selected_item_data = val; }

// ---------------------------------------------------------------------------
// History stack helpers
// ---------------------------------------------------------------------------

export function push_back_stack(val) { back_stack.push(val); }
export function pop_back_stack() { return back_stack.pop(); }
export function push_forward_stack(val) { forward_stack.push(val); }
export function pop_forward_stack() { return forward_stack.pop(); }
export function clear_forward_stack() { forward_stack = []; }

// ---------------------------------------------------------------------------
// Config API
// ---------------------------------------------------------------------------

export async function api_load_empty_config() {
 return await fetch("/load_empty_config", { method: "POST" });
}

export async function api_load_config(file) {
  const form_data = new FormData();
  form_data.append("file", file);
  return await fetch("/load_config", { method: "POST", body: form_data });
}

export async function api_save_config() {
  const res = await fetch("/save_config");
  return await res.json();
}

// ---------------------------------------------------------------------------
// Faculty API
// ---------------------------------------------------------------------------

export async function api_get_faculty() {
  const res = await fetch("/faculty");
  return await res.json();
}

export async function api_add_faculty(form_data) {
  return await fetch("/faculty", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form_data)
  });
}

export async function api_modify_faculty(name, form_data) {
  return await fetch(`/faculty/${encodeURIComponent(name)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form_data)
  });
}

export async function api_delete_faculty(name) {
  return await fetch(`/faculty/${encodeURIComponent(name)}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// Courses API
// ---------------------------------------------------------------------------

export async function api_get_courses() {
  const res = await fetch("/courses");
  if (!res.ok) throw new Error("Failed to load courses");
  return await res.json();
}

export async function api_add_course(form_data) {
  return await fetch("/courses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form_data)
  });
}

export async function api_modify_course(index, form_data) {
  return await fetch(`/courses/${index}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form_data)
  });
}

export async function api_delete_course(course_id) {
  return await fetch(`/courses/${encodeURIComponent(course_id)}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// Labs API
// ---------------------------------------------------------------------------

export async function api_get_labs() {
  const res = await fetch("/labs");
  if (!res.ok) throw new Error("Failed to load labs");
  return await res.json();
}

export async function api_add_lab(name) {
  return await fetch("/labs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });
}

export async function api_modify_lab(name, new_name) {
  return await fetch(`/labs/${encodeURIComponent(name)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: new_name })
  });
}

export async function api_delete_lab(name) {
  return await fetch(`/labs/${encodeURIComponent(name)}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// Rooms API
// ---------------------------------------------------------------------------

export async function api_get_rooms() {
  const res = await fetch("/rooms");
  if (!res.ok) throw new Error("Failed to load rooms");
  return await res.json();
}

export async function api_add_room(name) {
  return await fetch("/rooms", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });
}

export async function api_modify_room(name, new_name) {
  return await fetch(`/rooms/${encodeURIComponent(name)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: new_name })
  });
}

export async function api_delete_room(name) {
  return await fetch(`/rooms/${encodeURIComponent(name)}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// Time Slots API
// ---------------------------------------------------------------------------

export async function api_get_time_slots() {
  const res = await fetch("/time_slots");
  if (!res.ok) throw new Error("Failed to load time slots");
  return await res.json();
}

export async function api_add_time_range(data) {
  return await fetch("/time_slots/times", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}

export async function api_modify_time_range(day, index, data) {
  return await fetch(`/time_slots/times/${encodeURIComponent(day)}/${index}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}

export async function api_delete_time_range(day, index) {
  return await fetch(`/time_slots/times/${encodeURIComponent(day)}/${index}`, { method: "DELETE" });
}

export async function api_add_class_pattern(data) {
  return await fetch("/time_slots/classes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}

export async function api_modify_class_pattern(index, data) {
  return await fetch(`/time_slots/classes/${index}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}

export async function api_delete_class_pattern(index) {
  return await fetch(`/time_slots/classes/${index}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// Scheduler API
// ---------------------------------------------------------------------------

export async function api_run_scheduler(count, optimize) {
  return await fetch("/run_scheduler", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ limit: count, optimize })
  });
}

export async function api_get_schedule_view(index, mode) {
  const res = await fetch(`/schedule/${index}/view/${mode}`);
  return await res.json();
}

export async function api_get_schedule_count() {
  const res = await fetch("/schedule/count");
  return await res.json();
}

// ---------------------------------------------------------------------------
// CSV schedule loading
// ---------------------------------------------------------------------------

// Parses a multi-schedule CSV file into an array of schedules.
// Each schedule is an array of course-entry objects.
// CSV format per row: COURSE.SECTION,FACULTY,ROOM,LAB,TIME1,TIME2,...
// Times are "DAY HH:MM-HH:MM" with an optional trailing "^" marking a lab meeting.
// "Schedule N:" lines are used as delimiters between schedules.
export function parse_csv_schedules(text) {
  const schedules = [];
  let current = null;

  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line) continue;

    // "Schedule N:" starts a new schedule block
    if (/^Schedule\s+\d+:/i.test(line)) {
      current = [];
      schedules.push(current);
      continue;
    }

    // If the file has no "Schedule" headers, treat everything as one schedule
    if (current === null) {
      current = [];
      schedules.push(current);
    }

    const parts = line.split(",").map(p => p.trim());
    if (parts.length < 5) continue;

    const course_section = parts[0];
    const dot = course_section.lastIndexOf(".");
    const course_id = dot >= 0 ? course_section.slice(0, dot) : course_section;
    const section = dot >= 0 ? course_section.slice(dot + 1) : "";

    const faculty = parts[1];
    const room = parts[2];
    const lab = parts[3];

    const meetings = [];
    for (const tp of parts.slice(4)) {
      const is_lab = tp.endsWith("^");
      const clean = is_lab ? tp.slice(0, -1).trim() : tp.trim();
      const space = clean.indexOf(" ");
      if (space < 0) continue;
      meetings.push({
        day: clean.slice(0, space),
        time_range: clean.slice(space + 1),
        is_lab
      });
    }

    current.push({ course_id, section, faculty, room, lab, meetings });
  }

  return schedules;
}

// Converts a parsed CSV schedule into the same data structure the backend
// returns from /schedule/{index}/view/{mode}, so the existing render functions
// can display it without any changes.
export function get_csv_schedule_view(index, mode) {
  if (index < 0 || index >= csv_schedules.length) {
    return { error: `Schedule ${index + 1} not found. Only ${csv_schedules.length} schedule(s) loaded.` };
  }

  const DAY_NAMES = { MON: "Monday", TUE: "Tuesday", WED: "Wednesday", THU: "Thursday", FRI: "Friday" };
  const DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI"];

  // Flatten all course entries into individual meeting slots
  const all_slots = [];
  for (const entry of csv_schedules[index]) {
    for (const m of entry.meetings) {
      all_slots.push({
        day: m.day,
        time: m.time_range,
        course: entry.course_id,
        section: entry.section,
        faculty: entry.faculty,
        room: entry.room,
        lab: entry.lab,
        is_lab: m.is_lab
      });
    }
  }

  // Sort by day order then by start time
  all_slots.sort((a, b) => {
    const d = DAY_ORDER.indexOf(a.day) - DAY_ORDER.indexOf(b.day);
    return d !== 0 ? d : a.time.localeCompare(b.time);
  });

  // Group by day, then optionally sub-group by mode key
  const key_fn = {
    faculty: s => s.faculty,
    room: s => (s.is_lab ? s.lab : s.room),
    lab: s => s.lab
  }[mode] || null;

  const view_slots = mode === "lab" ? all_slots.filter(s => s.is_lab) : all_slots;

  const days_map = {};
  for (const slot of view_slots) {
    (days_map[slot.day] = days_map[slot.day] || []).push(slot);
  }

  const days = [];
  for (const day of DAY_ORDER) {
    if (!days_map[day]) continue;
    const slots = days_map[day];

    let sub_groups;
    if (!key_fn) {
      sub_groups = [{ sub_key: null, slots }];
    } else {
      const sub_map = {};
      for (const slot of slots) {
        const k = key_fn(slot);
        (sub_map[k] = sub_map[k] || []).push(slot);
      }
      sub_groups = Object.entries(sub_map)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, ss]) => ({ sub_key: k, slots: ss }));
    }

    days.push({ day_name: DAY_NAMES[day] || day, sub_groups });
  }

  return { mode, days };
}