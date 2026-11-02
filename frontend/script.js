
const tasks = [];

const modal = document.getElementById("taskModal");

const addTaskBtn = document.getElementById("addTaskBtn");
const saveTaskBtn = document.getElementById("saveTaskBtn");
const closeModalBtn = document.getElementById("closeModalBtn");

addTaskBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
});

closeModalBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
});

saveTaskBtn.addEventListener("click", () => {
    const title = document.getElementById("taskTitle").value.trim();
    const priority = document.getElementById("taskPriority").value;
    const status = document.getElementById("taskStatus").value;

    if (!title) {
        alert("Please enter a task title");
        return;
    }

    tasks.push({
        id: Date.now(),
        title,
        priority,
        status
    });

    document.getElementById("taskTitle").value = "";

    modal.classList.add("hidden");

    renderTasks();
});

function renderTasks() {
    const taskList = document.getElementById("taskList");

    taskList.innerHTML = "";

    if (tasks.length === 0) {
        taskList.innerHTML =
            '<p class="empty">No tasks yet. Add your first task!</p>';
    }

    tasks.forEach(task => {
        const item = document.createElement("div");
        item.className = "task-item";

        const title = document.createElement("strong");
        title.textContent = task.title;

        const priority = document.createElement("span");
        priority.textContent = task.priority;

        const status = document.createElement("select");

        ["Pending", "In Progress", "Completed"].forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value;
            status.appendChild(option);
        });

        status.value = task.status;

        status.addEventListener("change", () => {
            task.status = status.value;
            renderTasks();
        });

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";

        deleteBtn.addEventListener("click", () => {
            const index = tasks.findIndex(t => t.id === task.id);
            if (index !== -1) tasks.splice(index, 1);
            renderTasks();
        });

        item.append(title, priority, status, deleteBtn);
        taskList.appendChild(item);
    });

    document.getElementById("totalTasks").textContent = tasks.length;
    document.getElementById("pendingTasks").textContent =
        tasks.filter(t => t.status === "Pending").length;
    document.getElementById("progressTasks").textContent =
        tasks.filter(t => t.status === "In Progress").length;
    document.getElementById("completedTasks").textContent =
        tasks.filter(t => t.status === "Completed").length;
}

renderTasks();
