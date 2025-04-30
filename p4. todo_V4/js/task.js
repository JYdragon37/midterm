export function updateTaskTable(project) {
    const table = document.getElementById('task-table');
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = ''; // 기존 내용 초기화

    project.tasks.forEach(task => {
        const tr = document.createElement('tr');
        const tdName = document.createElement('td');
        tdName.textContent = task.name;
        tr.appendChild(tdName);

        // 날짜 범위에 대한 체크박스 생성
        dateRange.forEach(date => {
            const td = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'task-checkbox';
            checkbox.checked = task.completions && task.completions[date] === true;

            checkbox.addEventListener('change', async () => {
                const isChecked = checkbox.checked; // 현재 체크 상태 저장
                try {
                    const response = await fetch('/update_task_status', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            taskId: task.id,
                            date: date,
                            completed: isChecked
                        })
                    });

                    const result = await response.json();
                    if (result.status === 'success') {
                        task.completions[date] = isChecked; // 상태 업데이트
                    } else {
                        checkbox.checked = !isChecked; // 상태 되돌리기
                    }
                } catch (error) {
                    console.error('Error:', error);
                    checkbox.checked = !isChecked; // 상태 되돌리기
                }
            });

            td.appendChild(checkbox);
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });
}

export function setupCelebration() {
    // 축하 애니메이션 관련 로직
    const celebrationButton = document.getElementById('celebration-button');
    celebrationButton.addEventListener('click', () => {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        alert(randomMessage); // 팝업 메시지 표시
    });
} 