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

// Popup elements
const amd_popup = document.getElementById("amd-popup");
const popup_save = document.getElementById("popup-save");
const popup_title = document.getElementById("popup-title");
const popup_form = document.getElementById("popup-form");
const popup_close = document.getElementById("popup-close");

// Holds contents of loaded file
let loaded_file_content = null;
let loaded_file_extension = null;

// Field we are currently editing
let current_field = null;
let current_operation = null;

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
  } else {
    back_img.src = "/static/images/back_shadow.png";
    back_button.style.color = "#808080";
  }

  if (forward_stack.length > 0) {
    forward_img.src = "/static/images/forward.png";
    forward_button.style.color = "#484848";
  } else {
    forward_img.src = "/static/images/forward_shadow.png";
    forward_button.style.color = "#808080";
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
            <label for="labs-name">Lab Name:</label>
            <input type="text" id="labs-name" placeholder="e.g. Mac" />
          </div>
        `;
        break;

      case "Rooms":
        popup_form.innerHTML = `
          <div class="form-line">
            <label for="rooms-name">Room Name:</label>
            <input type="text" id="rooms-name" placeholder="e.g. Roddy 147" />
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
  if (current_field !== null) {
    add_img.src = "/static/images/add.png";
    modify_img.src = "/static/images/modify.png";
    delete_img.src = "/static/images/delete.png";
    add_button.style.color = "#484848";
    modify_button.style.color = "#484848";
    delete_button.style.color = "#484848";
  } else {
    add_img.src = "/static/images/add_shadow.png";
    modify_img.src = "/static/images/modify_shadow.png";
    delete_img.src = "/static/images/delete_shadow.png";
    add_button.style.color = "#808080";
    modify_button.style.color = "#808080";
    delete_button.style.color = "#808080";
  }
}

// Fields event listeners
faculty_button.addEventListener("click", () => {
  current_field = "Faculty";
  navigate_to("Existing faculty would be printed here");
  console.log(loaded_file_content);
  update_amd_images();
});

courses_button.addEventListener("click", () => {
  current_field = "Courses";
  navigate_to("Existing courses would be printed here");
  update_amd_images();
});

labs_button.addEventListener("click", () => {
  current_field = "Labs";
  navigate_to("Existing labs would be printed here");
  update_amd_images();
});

rooms_button.addEventListener("click", () => {
  current_field = "Rooms";
  navigate_to(`Existing ${current_field} would be printed here`);
  update_amd_images();
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

// Loads content of json or csv file
//load_button.addEventListener("change", function () {
//})

// Reads a file input and stores its text content in loaded_file_content.
// Parameters: input - file input element
function load_file_content(input) {
  let fileTypes = ['json', 'csv'];
  let fileReader = new FileReader();

  fileReader.onload = function () {
    // PUT FETCH IN HERE
    loaded_file_content = fileReader.result;
  }

  fileReader.readAsText(input.files[0]);
}

// Add button: sets current_operation and opens the Add popup for the active field.
add_button.addEventListener("click", () => {
  current_operation = "add";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();

  edit_popup("Add");
});

// Modify button: sets current_operation and opens the Modify popup for the active field.
modify_button.addEventListener("click", () => {
  current_operation = "modify";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();

  edit_popup("Modify");
});

// Delete button: sets current_operation and opens the Delete popup for the active field.
delete_button.addEventListener("click", () => {
  current_operation = "delete";
  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();

  edit_popup("Delete");
});

// Save button: reads form inputs and POSTs to the appropriate API route
// based on current_field and current_operation. Refreshes faculty list on success.
popup_save.addEventListener("click", async () => {
  console.log("SAVE CLICKED", current_field, current_operation);
  if (current_field === "Faculty") {

    const name = document.getElementById("faculty-name").value.trim();

    if (!name) {
      alert("Enter a faculty name");
      return;
    }

    if (current_operation === "add") {

      const maxCredits = parseInt(
        document.getElementById("faculty-max-credits").value
      );

      await fetch("/faculty", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name,
          maximum_credits: maxCredits,
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

    }

    else if (current_operation === "delete") {

      await fetch(`/faculty/${encodeURIComponent(name)}`, {
        method: "DELETE"
      });

    }

    else if (current_operation === "modify") {

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

      await fetch(`/faculty/${encodeURIComponent(name)}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

    }
    console.log("MODIFY DATA:", data);
    await loadFaculty();
  }

});

// Listens for file selection on the load input, uploads the file to /load_config,
// and logs the server response.
const fileInput = document.getElementById("load");

fileInput.addEventListener("change", async function () {
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/load_config", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  console.log(data);
});

// Close button: clears and hides the popup, restores pointer events, refocuses active field.
popup_close.addEventListener("click", () => {
  popup_form.innerHTML = "";
  amd_popup.classList.add("popup-hidden");
  wrapper.style.pointerEvents = "all";

  if (current_field === "Faculty") faculty_button.focus();
  else if (current_field === "Courses") courses_button.focus();
  else if (current_field === "Labs") labs_button.focus();
  else if (current_field === "Rooms") rooms_button.focus();
});

const facultyButton = document.getElementById("faculty-button");

// Fetches all faculty from the API and renders each name as a div in the faculty container.
async function loadFaculty() {

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

// POSTs a new faculty member to the API and logs the response.
// Parameters: formData - object containing faculty fields
async function addFaculty(formData) {
  const res = await fetch("/faculty", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  });

  const data = await res.json();
  console.log(data);
}

facultyButton.addEventListener("click", loadFaculty);

// Fetches a single faculty member by name and populates the modify form fields.
// Shows an alert if the faculty member is not found.
// Parameters: name - faculty member's name
async function load_faculty_into_form(name) {

  const res = await fetch(`/faculty/${encodeURIComponent(name)}`);
  const data = await res.json();

  if (data.error) {
    alert("Faculty not found");
    return;
  }

  document.getElementById("faculty-max-credits").value = data.maximum_credits;
  document.getElementById("faculty-min-credits").value = data.minimum_credits;
  document.getElementById("faculty-max-days").value = data.maximum_days;
}