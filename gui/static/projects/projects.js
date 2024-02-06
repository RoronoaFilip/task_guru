function setupProject(projectId) {
    document.getElementById(`project-${projectId}`).addEventListener('click', () => {
        window.location.href = `/projects/${projectId}`;
    });
}