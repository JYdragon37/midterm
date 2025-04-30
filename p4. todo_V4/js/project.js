export async function loadProjects() {
    try {
        const response = await fetch('/get_projects');
        const projects = await response.json();
        const projectSelect = document.getElementById('project-select');
        projectSelect.innerHTML = ''; // 기존 내용 초기화

        projects.forEach(project => {
            const option = document.createElement('option');
            option.value = JSON.stringify(project);
            option.textContent = project.name;
            projectSelect.appendChild(option);
        });

        // 첫 번째 프로젝트 자동 로드
        if (projects.length > 0) {
            loadProject(projects[0].id);
        }
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}