from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.ai_logic import convert_tone
import os

# FastAPI 애플리케이션 인스턴스화
app = FastAPI(title="Business Tone Converter")

# 요청 데이터 모델 정의
class ConvertRequest(BaseModel):
    text: str
    target: str

# 말투 변환 API 엔드포인트
@app.post("/api/convert")
async def convert(request: ConvertRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="변환할 내용을 입력해 주세요.")
    
    try:
        converted_text = convert_tone(request.text, request.target)
        return {
            "converted_text": converted_text,
            "target": request.target,
            "original_text": request.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 정적 파일 서빙 (static 폴더의 파일들을 루트 경로에서 접근 가능하게 설정)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # uvicorn 실행 (로컬 테스트용)
    uvicorn.run(app, host="0.0.0.0", port=8000)
