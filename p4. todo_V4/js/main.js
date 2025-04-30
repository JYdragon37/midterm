import { loadProjects } from './project.js';
import { updateTaskTable } from './task.js';
import { setupCelebration } from './celebration.js';

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

    // 프로젝트 및 태스크 로드
    await loadProjects();

    // 프로젝트 선택 시 태스크 로드
    const projectSelect = document.getElementById('project-select');
    projectSelect.addEventListener('change', function() {
        const selectedProject = JSON.parse(this.value);
        updateTaskTable(selectedProject.id);
    });

    // 축하 애니메이션 설정
    setupCelebration();
}); 