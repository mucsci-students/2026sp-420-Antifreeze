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

// ---------------------------------------------------------------------------
// State setters
// ---------------------------------------------------------------------------

export function set_current_field(val) { current_field = val; }
export function set_current_operation(val) { current_operation = val; }
export function set_schedules_generated(val) { schedules_generated = val; }
export function set_current_content(val) { current_content = val; }
export function set_loaded_file_content(val) { loaded_file_content = val; }

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

export async function api_modify_course(course_id, form_data) {
  return await fetch(`/courses/${encodeURIComponent(course_id)}`, {
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