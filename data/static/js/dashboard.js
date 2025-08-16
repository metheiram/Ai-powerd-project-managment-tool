
document.addEventListener('DOMContentLoaded', () => {
    const currentDate = new Date();
    const currentDay = currentDate.getDate();
    const calenderDays = document.querySelectorAll('.calender-day');
    const taskList = document.getElementById('task-list');

    // Task data for different dates (for example purposes)
    const tasksData = {
        '1': [
            { task: 'Working on Asia Project', time: '08:00 - 10:00 AM' },
            { task: 'Team Meeting', time: '10:00 - 12:00 PM' }
        ],
        '2': [
            { task: 'Research Task', time: '09:00 - 11:00 AM' }
        ],
        // Add more dates and tasks here
        '30': [
            { task: 'Finalize Reports', time: '03:00 - 05:00 PM' }
        ]
    };

    // Function to update the task list based on the selected date
    function updateTaskList(date) {
        const tasks = tasksData[date] || [];
        taskList.innerHTML = tasks.map(task => `
            <li class="flex justify-between items-center">
                <span>${task.task}</span>
                <span class="text-gray-500">${task.time}</span>
            </li>
        `).join('');
    }

    // Set the current day as highlighted
    calenderDays.forEach(day => {
        if (parseInt(day.textContent) === currentDay) {
            day.classList.add('bg-purple-600', 'text-white');
            day.classList.remove('text-gray-700');
        }
    });

    // Add event listeners for each date
    calenderDays.forEach(day => {
        day.addEventListener('click', () => {
            // Remove highlight from previous selected day
            calenderDays.forEach(d => d.classList.remove('bg-purple-600', 'text-white'));
            day.classList.add('bg-purple-600', 'text-white');
            day.classList.remove('text-gray-700');

            // Update the tasks for the clicked date
            updateTaskList(day.textContent);
        });
    });

    // Set the default task list for the current date
    updateTaskList(currentDay);
});


document.addEventListener('DOMContentLoaded', () => {
  const calendarDays = document.querySelectorAll('.calendar-day');
  const taskList = document.getElementById('task-list');
  const projectList = document.getElementById('project-list');

  calendarDays.forEach(day => {
    day.addEventListener('click', () => {
      const selectedDate = day.getAttribute('data-date');

      // Highlight selected date
      calendarDays.forEach(d => d.classList.remove('bg-purple-700'));
      day.classList.add('bg-purple-700');

      // Fetch Tasks
      fetch(`/tasks/by-date/?date=${selectedDate}`)
        .then(res => res.json())
        .then(data => {
          taskList.innerHTML = '';
          if (data.tasks?.length) {
            data.tasks.forEach(task => {
              const li = document.createElement('li');
              li.classList.add('bg-gray-700', 'p-4', 'rounded', 'shadow');
              li.innerHTML = `
                <strong>${task.title}</strong><br/>
                <span>${task.description}</span><br/>
                <span class="text-sm text-gray-300">Status: ${task.status}</span><br/>
                <span class="text-sm text-gray-400">Project: ${task.project}</span>`;
              taskList.appendChild(li);
            });
          } else {
            taskList.innerHTML = `<li class="text-gray-400">No tasks for this date.</li>`;
          }
        });

      // Fetch Projects
      fetch(`/projects/by-date/?date=${selectedDate}`)
        .then(res => res.json())
        .then(data => {
          projectList.innerHTML = '';
          if (data.projects?.length) {
            data.projects.forEach(project => {
              const div = document.createElement('div');
              div.classList.add('flex', 'justify-between', 'items-center');
              div.innerHTML = `
                <div>
                  <strong>${project.title}</strong>
                  <p class="text-sm text-gray-300">${project.description}</p>
                  <p class="text-sm text-gray-400">Status: ${project.status}</p>
                </div>
                <button class="bg-gradient-to-r from-cyan-400 to-purple-500 text-white px-4 py-2 rounded-full hover:scale-110 transition-transform duration-300">View</button>`;
              projectList.appendChild(div);
            });
          } else {
            projectList.innerHTML = `<div class="text-gray-400">No projects for this date.</div>`;
          }
        });
    });
  });
});
