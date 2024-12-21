document.addEventListener('DOMContentLoaded', function () {

    // Attach change status listeners to all existing buttons
    document.querySelectorAll('.change-status').forEach(btn => {
        attachChangeStatusListener(btn);
    });

    // Enable sortable functionality for all task containers
    const lists = document.querySelectorAll('.card-body'); // Task zones
    lists.forEach(list => {
        activateSortable(list);
    });

    // Attach delete listeners to all existing delete buttons
    document.querySelectorAll('.delete-task').forEach(button => {
        deleteTaskListener(button);
    });

    // Attach focus mode listeners to all existing tasks
    document.querySelectorAll('.start-focus').forEach(btn => {
        btn.addEventListener('click', () => attachFocusModeListener(btn.dataset.id));
    })

    // Handle form submissions for adding new tasks
    document.querySelectorAll('.task-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        console.log(data.message);

                        // Clear the input field
                        form.querySelector('input').value = '';

                        const task = data.task;
                        const containerSelector = getContainerSelector(task.priority);
                        const containerColor = getContainerColor(task.priority);

                        // Create the task element dynamically
                        const taskElement = document.createElement('div');
                        taskElement.classList.add('task-item', 'd-flex', 'justify-content-between', 'border', 'rounded', 'mb-1', 'p-1');
                        taskElement.dataset.id = task.id;
                        taskElement.style.backgroundColor = containerColor;
                        taskElement.innerHTML = `
                            <p class="p-0 m-0">
                                <i class="bi bi-plus-lg m-1" id="move"></i>
                                <span class="task-title " style="cursor: pointer;" data-id="${task.id}">
                                    ${task.completed ? `<del class="opacity-25">${task.title}</del>` : task.title}
                                </span>
                            </p>
                            <div class='d-flex' >
                                    <button class="btn p-0 m-0 dropdown-toggle menu" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>

                                    <!-- Menu Dropdown -->
                                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                        <li><a class="dropdown-item start-focus" href="#" style='cursor: pointer;'>Focus mode</a></li>
                                        <li><a class="dropdown-item text-danger delete-task" data-id="${task.id}" data-status="${task.completed ? 'true' : 'false'} href="#" style='cursor: pointer;' >Delete</a></li>
                                    </ul>
                                    <button data-id="${task.id}" class="dropdown-btn delete-task o btn p-0 m-0" data-status="${task.completed ? 'true' : 'false'}" style='display: none;'>
                                        <i class="bi bi-trash"></i>
                                    </button>
                                <button class="change-status" 
                                    style="background-color: transparent; border: none;"
                                   data-id="${task.id}" 
                                   data-title="${task.title}" 
                                   data-status="${task.completed ? 'Pending' : 'Completed'}">
                                    <i class="bi ${task.completed ? 'bi-arrow-clockwise' : 'bi-check2'} m-1"></i>
                                </button>
                            </div>
                        `;

                        // Add the task element to the appropriate container
                        document.querySelector(containerSelector).appendChild(taskElement);

                        // Re-enable sorting for the updated container
                        activateSortable(taskElement.parentElement);

                        // Update pending task count
                        const p = document.querySelector('#p');
                        const pendingCount = parseInt(p.dataset.count, 10) + 1;
                        p.dataset.count = pendingCount;
                        p.innerHTML = `${pendingCount}`;

                        // Attach event listeners to the new task element
                        taskElement.querySelectorAll('.delete-task').forEach(btn => {
                            deleteTaskListener(btn);
                        } );

                        
                        attachChangeStatusListener(taskElement.querySelector('.change-status'));
                        taskElement.querySelector('.start-focus').addEventListener('click', () => attachFocusModeListener(task.id));                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        });
    });

    // Enable sortable functionality using Sortable.js
    function activateSortable(element) {
        new Sortable(element, {
            group: 'tasks', // Allow moving tasks between containers
            animation: 150, // Smooth animation
            onEnd: function (evt) {
                const taskElement = evt.item;
                const newCategory = evt.to.id; // New category (container ID)
                const taskId = taskElement.dataset.id;
                const backgroundColor = getContainerColor(newCategory);

                // Update task's background color and category
                taskElement.style.backgroundColor = backgroundColor;
                updateTaskCategory(taskId, newCategory);
            }
        });
    }

    // Update task category in the database
    function updateTaskCategory(taskId, newCategory) {
        fetch('/update-task-category/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task_id: taskId,
                category: newCategory
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to update task category');
                }
                return response.json();
            })
            .then(data => {
                console.log('Task moved successfully', data);
            })
            .catch(error => {
                console.error('Error while moving the task:', error);
            });
    }

    // Get the container selector based on task priority
    function getContainerSelector(priority) {
        switch (priority) {
            case 'important and urgent':
                return '.urgent-important .card-body';
            case 'important but not urgent':
                return '.not-urgent-important .card-body';
            case 'not important but ugent':
                return '.urgent-not-important .card-body';
            case 'not important and not urgent':
                return '.not-urgent-not-important .card-body';
            default:
                return null;
        }
    }

    // Get the background color based on task priority
    function getContainerColor(priority) {
        switch (priority) {
            case 'important and urgent':
                return 'rgb(224, 130, 130)';
            case 'important but not urgent':
                return 'rgb(148, 206, 137)';
            case 'not important but ugent':
                return 'rgba(98, 201, 233, 0.808)';
            case 'not important and not urgent':
                return 'rgba(76, 79, 80, 0.808)';
            default:
                return null;
        }
    }

    // Attach click listener for changing task status
    function attachChangeStatusListener(element) {
        element.addEventListener('click', function () {
            const newStatus = this.dataset.status;
            const taskId = this.dataset.id;
            const title = this.dataset.title;

            fetch(`/task/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newStatus }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        
                        const taskElement = this.closest('.task-item');

                        if (newStatus === 'Completed') {
                            taskElement.querySelector('.task-title').innerHTML = `<del class='opacity-25'>${title}</del>`;
                            this.innerHTML = `<i class="bi bi-arrow-clockwise m-1"></i>`;
                            taskElement.querySelector('.menu').style.display = 'none';
                            taskElement.querySelector('.o').style.display = 'block';

                            // Update completed and pending counts
                            updateCount('#c', 1);
                            updateCount('#p', -1);

                            this.dataset.status = 'Pending';

                            Swal.fire({
                                title: 'Task Completed',
                                text: 'Congratulation for completing this task. You are on the right way',
                                icon: 'success',
                                confirmButtonText: 'Got it!',
                                customClass: {
                                    popup: 'custom-popup',
                                    title: 'custom-title',
                                    confirmButton: 'custom-button'
                                }
                            });
                            
                        } else {
                            taskElement.querySelector('.task-title').innerHTML = title;
                            this.innerHTML = `<i class="bi bi-check2 m-1"></i>`;
                            taskElement.querySelector('.menu').style.display = 'block';
                            taskElement.querySelector('.o').style.display = 'none';

                            // Update completed and pending counts
                            updateCount('#p', 1);
                            updateCount('#c', -1);

                            this.dataset.status = 'Completed';
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        });
    }

    // Update the count of tasks
    function updateCount(selector, delta) {
        const element = document.querySelector(selector);
        const currentCount = parseInt(element.dataset.count, 10) + delta;
        element.dataset.count = currentCount;
        element.innerHTML = `${currentCount}`;
    }

    // Attach click listener for deleting tasks
    function deleteTaskListener(element) {
        element.addEventListener('click', function () {
            const taskId = this.dataset.id;
            const taskItem = element.closest('.task-item');

            fetch(`/task/${taskId}`, {
                method: 'DELETE',
            })
                .then(response => {
                    if (response.ok) {
                        Swal.fire({
                            title: 'Delete Task!',
                            text: "You have deleted  this task",
                            icon: 'warning',
                            confirmButtonText: 'Got it!',
                            timer: 5000, 
                            customClass: {
                                popup: 'custom-popup',
                                title: 'custom-title',
                                confirmButton: 'custom-button'
                            }
                        });
                        taskItem.classList.add('opacity-50');
                        taskItem.style.transition = 'opacity 0.5s'

                        setTimeout(() => {
                            taskItem.remove();
                        }, 500);

                        console.log(element.dataset.status)

                        if (element.dataset.status === 'false' ){
                            updateCount('#p', -1)
                        } else {
                            updateCount('#c', -1)
                        }
                    } else {
                        alert('Failed to delete the task.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the task')
                })
            });
        };

    });



    function attachFocusModeListener (taskId) {
        fetch(`/task/${taskId}/focus_mode`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch task data");
            }
            return response.json(); // Analyse la réponse comme JSON
        })
        .then(data => {
            if (data.task && data.task.title) {
                displayModal(data.content); 
                const start = document.querySelector('#start-focus');
                start.addEventListener('click', () => startFocusMode(data.task.title, 25))
                document.getElementById("exit-focus").addEventListener("click", exitFocusMode);
            } else {
                throw new Error("Task data is incomplete.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while starting focus mode. Please try again.");
        });

    };

    let timer;
    let timeLeft;
    let isFocusModeActive = false;
    let isPaused = false;
    
    function startFocusMode(taskName) {
        const customTimeInput = document.getElementById("custom-time");
        const customTime = parseInt(customTimeInput.value, 10);
    
        if (isNaN(customTime) || customTime < 1 || customTime > 120) {
            alert("Please enter a valid time between 1 and 120 minutes.");
            return;
        }
    
        const duration = customTime;
    
        if (!isFocusModeActive) {
            isFocusModeActive = true;
            isPaused = false;
            timeLeft = duration * 60;
            updateStartButton("Pause");
            startTimer();
            Swal.fire({
                title: 'Focus Mode!',
                text: `Focus mode started for ${customTime} minutes! Stay focused!`,
                icon: 'info',
                confirmButtonText: 'Got it!',
                customClass: {
                    popup: 'custom-popup',
                    title: 'custom-title',
                    confirmButton: 'custom-button'
                }
            });
        
        } else if (isPaused) {
            isPaused = false;
            updateStartButton("Pause");
            startTimer();
        } else {
            isPaused = true;
            updateStartButton("Resume");
            clearInterval(timer);
        }
    }
    
    function exitFocusMode() {
        const timerDisplay = document.getElementById("time-left");
        const customTimeInput = document.getElementById("custom-time");
    
        isFocusModeActive = false;
        isPaused = false;
        clearInterval(timer);
        timeLeft = 25 * 60;
        timerDisplay.textContent = "25:00";
        customTimeInput.value = 25;
        updateStartButton("Start");
    }
    
    function startTimer() {
        const timerDisplay = document.getElementById("time-left");
    
        timer = setInterval(() => {
            if (timeLeft <= 0) {
                clearInterval(timer);
                Swal.fire({
                    title: 'Focus Mode!',
                    text: "Time's up! Well done for focusing!",
                    icon: 'success',
                    confirmButtonText: 'Got it!',
                    customClass: {
                        popup: 'custom-popup',
                        title: 'custom-title',
                        confirmButton: 'custom-button'
                    }
                });
                exitFocusMode();
                return;
            }
    
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerDisplay.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
            timeLeft--;
        }, 1000);
    }
    
    function updateStartButton(state) {
        const startButton = document.getElementById("start-focus");
    
        if (state === "Pause") {
            startButton.innerHTML = " <i class=' bi bi-pause-fill'></i> Pause"; 
        } else if (state === "Resume") {
            startButton.innerHTML = " <i class=' bi bi-play-fill'></i> Resume"; 
        } else if (state === "Start") {
            startButton.innerHTML = "<i class=' bi bi-play-fill'></i> Start"; 
        }
    }
    
    function displayModal(content) {
        document.getElementById('modal-body-content').innerHTML = content;
        const taskModal = new bootstrap.Modal(document.getElementById('taskModal'), { keyboard: false });
        taskModal.show();
    }

