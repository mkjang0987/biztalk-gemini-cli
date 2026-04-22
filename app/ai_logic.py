import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage

# .env 파일에서 환경 변수 로드
load_dotenv()

# Upstage Solar-Pro2 모델 설정
# 모델명은 실제 API 가이드에 따라 'solar-pro' 등으로 설정될 수 있습니다.
llm = ChatUpstage(model="solar-pro")

# 수신 대상별 시스템 프롬프트 정의
PROMPT_TEMPLATES = {
    "boss": "귀하는 상사나 임원에게 보고하는 상황입니다. 격식 있고 공손한 경어체를 사용하며, 전달하고자 하는 핵심 내용을 논리적이고 명확하게 보고하는 말투로 변환해 주세요. 불필요한 사족은 줄이되 정중함을 잃지 마십시오.",
    "colleague": "귀하는 타 부서 동료에게 업무 협조를 요청하거나 의견을 나누는 상황입니다. 정중하면서도 협조적인 어조를 사용하며, 상대방의 상황을 배려하면서도 필요한 업무 사항이 명확하게 전달되도록 변환해 주세요.",
    "client": "귀하는 고객이나 외부 업체 담당자에게 안내하는 상황입니다. 매우 친절하고 신뢰감을 주는 서비스 어조를 사용하며, 고객을 존중하고 배려하는 마음이 느껴지도록 부드럽고 전문적인 문장으로 변환해 주세요.",
    "team": "귀하는 같은 팀 내 동료와 편하게 소통하는 상황입니다. 격식보다는 실무적인 효율성과 명확성을 중시하며, 간결하고 이해하기 쉬운 어조로 변환해 주세요. 너무 딱딱하지 않으면서도 업무의 핵심이 잘 드러나야 합니다."
}

def convert_tone(text: str, target: str) -> str:
    """
    사용자가 입력한 텍스트를 대상(target)에 맞는 말투로 변환합니다.
    """
    system_prompt = PROMPT_TEMPLATES.get(target, PROMPT_TEMPLATES["team"])
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"다음 내용을 해당 말투로 변환해 주세요: {text}")
    ]
    
    response = llm.invoke(messages)
    return response.content
