document.addEventListener('DOMContentLoaded', () => {
    const convertBtn = document.getElementById('convertBtn');
    const copyBtn = document.getElementById('copyBtn');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const outputArea = document.getElementById('outputArea');
    const loading = document.getElementById('loading');

    // 변환 버튼 클릭 이벤트
    convertBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        const target = document.querySelector('input[name="target"]:checked').value;

        if (!text) {
            alert('변환할 내용을 입력해 주세요.');
            return;
        }

        // 로딩 표시
        loading.style.display = 'flex';
        outputArea.style.display = 'none';

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '변환 중 오류가 발생했습니다.');
            }

            const data = await response.json();
            
            // 결과 출력
            outputText.textContent = data.converted_text;
            outputArea.style.display = 'block';
            
            // 결과 영역으로 스크롤
            outputArea.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            alert(`오류: ${error.message}`);
        } finally {
            // 로딩 숨김
            loading.style.display = 'none';
        }
    });

    // 복사하기 버튼 클릭 이벤트
    copyBtn.addEventListener('click', () => {
        const textToCopy = outputText.textContent;
        
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '✅ 복사 완료!';
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
            }, 2000);
        }).catch(err => {
            console.error('복사 실패:', err);
            alert('복사에 실패했습니다.');
        });
    });
});
