document.addEventListener('DOMContentLoaded', async function() {
    // 한국 시간으로 현재 날짜 표시
    const currentDateElement = document.getElementById('current-date');
    const options = { 
        timeZone: 'Asia/Seoul',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    };
    currentDateElement.textContent = new Date().toLocaleString('ko-KR', options);

    // Collapsible 섹션 설정
    const coll = document.getElementsByClassName("collapsible");
    Array.from(coll).forEach(button => {
        button.addEventListener("click", function() {
            this.classList.toggle("active");
            const content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });

    // 격려 메시지 배열
    const encouragingMessages = [
        "잘했어요! 계속 이렇게 해보세요! 🌟",
        "대단해요! 목표를 향해 한 걸음 더! 💪",
        "와우! 정말 잘하고 있어요! 🎉",
        "오늘도 해냈어요! 멋져요! 🌈",
        "끝내주는 성과예요! 자부심을 가지세요! ⭐",
        "당신의 노력이 빛나고 있어요! 💫",
        "이렇게 꾸준히 하다보면 반드시 성공할 거예요! 🎯",
        "오늘의 작은 성공이 내일의 큰 성취로! 🌅"
    ];

    // 축하 애니메이션 함수
    function showCelebration(message) {
        const modal = document.getElementById('celebration-modal');
        const messageElement = modal.querySelector('.celebration-message');
        const animationContainer = modal.querySelector('.celebration-animation');
        
        messageElement.textContent = message;
        modal.style.display = 'block';
        
        // 컨페티 애니메이션 생성
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
            confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
            animationContainer.appendChild(confetti);
        }

        setTimeout(() => {
            modal.style.display = 'none';
            animationContainer.innerHTML = '';
        }, 3000);
    }

    // 기존 코드...
    const projectForm = document.getElementById('project-form');
    const projectSelect = document.getElementById('project-select');
    const projectDetails = document.getElementById('project-details');
    const taskForm = document.getElementById('task-form');

    // 프로젝트 수정/삭제 버튼 이벤트
    document.getElementById('edit-project-btn').addEventListener('click', function() {
        const selectedProject = JSON.parse(projectSelect.value);
        const modal = document.getElementById('edit-project-modal');
        
        document.getElementById('edit-project-name').value = selectedProject.name;
        document.getElementById('edit-start-date').value = selectedProject.startDate;
        document.getElementById('edit-end-date').value = selectedProject.endDate;
        
        modal.style.display = 'block';
    });

    document.getElementById('delete-project-btn').addEventListener('click', async function() {
        if (!confirm('정말로 이 프로젝트를 삭제하시겠습니까?')) return;
        
        const selectedProject = JSON.parse(projectSelect.value);
        try {
            const response = await fetch('/delete_project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ projectId: selectedProject.id })
            });
            
            const result = await response.json();
            if (result.status === 'success') {
                updateProjectSelect(result.projects);
                projectDetails.style.display = 'none';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('프로젝트 삭제에 실패했습니다.');
        }
    });

    // 프로젝트 수정 폼 제출
    document.getElementById('edit-project-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const selectedProject = JSON.parse(projectSelect.value);
        const data = {
            projectId: selectedProject.id,
            name: document.getElementById('edit-project-name').value,
            startDate: document.getElementById('edit-start-date').value,
            endDate: document.getElementById('edit-end-date').value
        };

        try {
            const response = await fetch('/update_project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            if (result.status === 'success') {
                updateProjectSelect(result.projects);
                document.getElementById('edit-project-modal').style.display = 'none';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('프로젝트 수정에 실패했습니다.');
        }
    });

    // 체크박스 상태 변경 처리 함수
    async function handleCheckboxChange(checkbox, project, task, date) {
        try {
            const response = await fetch('/update_task_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    projectName: project.name,
                    taskName: task.name,
                    date: date,
                    completed: checkbox.checked
                })
            });

            const result = await response.json();
            if (result.status === 'success' && checkbox.checked) {
                // 랜덤 메시지 선택 및 축하 애니메이션 표시
                const randomMessage = encouragingMessages[Math.floor(Math.random() * encouragingMessages.length)];
                showCelebration(randomMessage);
            } else if (result.status !== 'success') {
                checkbox.checked = !checkbox.checked;
                alert('상태 업데이트에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            checkbox.checked = !checkbox.checked;
            alert('상태 업데이트에 실패했습니다.');
        }
    }

    // 태스크 수정/삭제 함수
    function handleTaskEdit(task, project) {
        const modal = document.getElementById('edit-task-modal');
        document.getElementById('edit-task-name').value = task.name;
        document.getElementById('edit-task-goal').value = task.goal;
        
        const form = document.getElementById('edit-task-form');
        form.onsubmit = async function(e) {
            e.preventDefault();
            
            try {
                const response = await fetch('/update_task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        taskId: task.id,
                        name: document.getElementById('edit-task-name').value,
                        goal: parseInt(document.getElementById('edit-task-goal').value)
                    })
                });
                
                const result = await response.json();
                if (result.status === 'success') {
                    modal.style.display = 'none';
                    updateTaskTable(project);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('태스크 수정에 실패했습니다.');
            }
        };
        
        modal.style.display = 'block';
    }

    function handleTaskDelete(task, project) {
        if (!confirm('정말로 이 태스크를 삭제하시겠습니까?')) return;
        
        fetch('/delete_task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ taskId: task.id })
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                updateTaskTable(project);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('태스크 삭제에 실패했습니다.');
        });
    }

    // 모달 닫기 버튼 이벤트
    document.querySelectorAll('.cancel-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });

    // 날짜 입력 필드에 대한 이벤트 리스너 추가
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    function updateProjectDuration() {
        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);
        
        if (startDate && endDate && startDate <= endDate) {
            const durationDays = Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
            const durationElement = document.getElementById('project-duration');
            durationElement.textContent = `프로젝트 기간: ${durationDays}일 (최대 ${durationDays}회 수행 가능)`;
        }
    }

    startDateInput.addEventListener('change', updateProjectDuration);
    endDateInput.addEventListener('change', updateProjectDuration);

    // 프로젝트 선택 시 기간 표시
    if (projectSelect) {
        projectSelect.addEventListener('change', async function() {
            const selectedProject = this.value ? JSON.parse(this.value) : null;

            if (selectedProject) {
                try {
                    // 프로젝트의 최신 데이터를 서버에서 가져오기
                    const response = await fetch(`/get_project/${selectedProject.id}`);
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        document.getElementById('detail-name').textContent = result.project.name;
                        document.getElementById('detail-start').textContent = result.project.startDate;
                        document.getElementById('detail-end').textContent = result.project.endDate;
                        projectDetails.style.display = 'block';
                        updateTaskTable(result.project);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('프로젝트 데이터를 가져오는데 실패했습니다.');
                }
            } else {
                projectDetails.style.display = 'none';
            }
        });
    }

    // 초기 프로젝트 데이터로 드롭다운 업데이트
    if (typeof initialProjects !== 'undefined' && initialProjects.length > 0) {
        updateProjectSelect(initialProjects);
    }

    // 페이지 로드 시 프로젝트 목록 가져오기
    try {
        const response = await fetch('/get_projects');
        const result = await response.json();
        if (result.status === 'success') {
            updateProjectSelect(result.projects);
        }
    } catch (error) {
        console.error('Error loading projects:', error);
    }

    if (projectForm) {
        projectForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const projectData = {
                name: document.getElementById('project-name').value,
                startDate: document.getElementById('start-date').value,
                endDate: document.getElementById('end-date').value
            };

            try {
                const response = await fetch('/create_project', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(projectData)
                });

                const result = await response.json();
                if (result.status === 'success') {
                    updateProjectSelect(result.projects);
                    projectForm.reset();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to create project');
            }
        });
    }

    if (taskForm) {
        taskForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const selectedProject = projectSelect.value ? JSON.parse(projectSelect.value) : null;
            if (!selectedProject) {
                alert('Please select a project first');
                return;
            }

            const taskData = {
                projectName: selectedProject.name,
                taskName: document.getElementById('task-name').value,
                goal: parseInt(document.getElementById('task-goal').value)
            };

            try {
                const response = await fetch('/add_task', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(taskData)
                });

                const result = await response.json();
                if (result.status === 'success') {
                    selectedProject.tasks = result.tasks;
                    updateTaskTable(selectedProject, result.dateRange, result.today);
                    taskForm.reset();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to add task');
            }
        });
    }
});

function updateProjectSelect(projects) {
    const select = document.getElementById('project-select');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="">Choose a project...</option>';
    
    projects.forEach(project => {
        const option = document.createElement('option');
        option.value = JSON.stringify(project);
        option.textContent = project.name;
        select.appendChild(option);
    });

    if (currentValue) {
        const previousProject = JSON.parse(currentValue);
        const options = select.options;
        for (let i = 0; i < options.length; i++) {
            const optionProject = options[i].value ? JSON.parse(options[i].value) : null;
            if (optionProject && optionProject.id === previousProject.id) {
                select.selectedIndex = i;
                const event = new Event('change');
                select.dispatchEvent(event);
                break;
            }
        }
    }
}

function updateTaskTable(project) {
    const table = document.getElementById('task-table');
    const thead = table.querySelector('thead tr');
    const tbody = table.querySelector('tbody');
    
    // 테재 날짜 기준으로 날짜 범위 생성
    const currentDate = new Date();
    const dateRange = [];
    for (let i = -2; i <= 2; i++) {
        const date = new Date(currentDate);
        date.setDate(date.getDate() + i);
        dateRange.push(date.toISOString().split('T')[0]);
    }
    const today = new Date().toISOString().split('T')[0];

    // 테이블 헤더 업데이트
    thead.innerHTML = '';
    ['Task Name', 'Goal', 'Actions', ...dateRange].forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        if (header === today) {
            th.classList.add('today-column');
        }
        thead.appendChild(th);
    });

    // 테이블 내용 업데이트
    tbody.innerHTML = '';
    if (project.tasks && project.tasks.length > 0) {
        project.tasks.forEach(task => {
            const tr = document.createElement('tr');
            
            // Task name
            const tdName = document.createElement('td');
            tdName.textContent = task.name;
            tr.appendChild(tdName);

            // Goal
            const tdGoal = document.createElement('td');
            tdGoal.textContent = task.goal;
            tr.appendChild(tdGoal);

            // Actions
            const tdActions = document.createElement('td');
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'task-actions';

            const editBtn = document.createElement('button');
            editBtn.className = 'edit-task-btn';
            editBtn.textContent = '수정';
            editBtn.onclick = () => handleTaskEdit(task, project);

            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-task-btn';
            deleteBtn.textContent = '삭제';
            deleteBtn.onclick = () => handleTaskDelete(task, project);

            actionsDiv.appendChild(editBtn);
            actionsDiv.appendChild(deleteBtn);
            tdActions.appendChild(actionsDiv);
            tr.appendChild(tdActions);

            // Date checkboxes
            dateRange.forEach(date => {
                const td = document.createElement('td');
                if (date === today) {
                    td.classList.add('today-column');
                }

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'task-checkbox';
                
                // completions 상태 확인 및 설정
                console.log(`Setting checkbox state for task ${task.id}, date ${date}:`, task.completions);
                if (task.completions && task.completions[date] === true) {
                    checkbox.checked = true;
                }

                checkbox.addEventListener('change', async () => {
                    try {
                        console.log('Checkbox changed:', {
                            taskId: task.id,
                            date: date,
                            checked: checkbox.checked,
                            currentCompletions: task.completions
                        });

                        const response = await fetch('/update_task_status', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                taskId: task.id,
                                date: date,
                                completed: checkbox.checked
                            })
                        });

                        const result = await response.json();
                        console.log('Server response:', result);

                        if (result.status === 'success') {
                            task.completions = result.completions;
                            console.log('Updated completions:', task.completions);
                        } else {
                            checkbox.checked = !checkbox.checked;
                            alert('상태 업데이트에 실패했습니다: ' + result.message);
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        checkbox.checked = !checkbox.checked;
                        alert('상태 업데이트에 실패했습니다.');
                    }
                });

                td.appendChild(checkbox);
                tr.appendChild(td);
            });

            tbody.appendChild(tr);
        });
    }
}

// ISO 형식의 날짜 문자열을 반환하는 Date 프로토타입 메서드 추가
Date.prototype.toISOFormat = function() {
    return this.toISOString();
};