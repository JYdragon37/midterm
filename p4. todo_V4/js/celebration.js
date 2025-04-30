export function setupCelebration() {
    // 축하 애니메이션 관련 로직
    const celebrationButton = document.getElementById('celebration-button');
    celebrationButton.addEventListener('click', () => {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        alert(randomMessage); // 팝업 메시지 표시
    });
}