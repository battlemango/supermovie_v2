import os
import requests
import re
from pathlib import Path
from typing import Optional, List

# ElevenLabs TTS API를 사용하여 텍스트를 음성으로 변환하고 파일로 저장하는 함수
def generate_tts_with_elevenlabs(
    text: str,
    output_path: str = "output.mp3",
    api_key: Optional[str] = "sk_92c9abfb8d79f63d8ad337bc05d711c20fdfe8c140beaec7",
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # 기본 음성 ID (Rachel - 영어)
    model_id: str = "eleven_multilingual_v2"  # 다국어 모델 사용
) -> bool:
    """
    ElevenLabs TTS API를 사용하여 텍스트를 음성으로 변환하고 파일로 저장합니다.
    
    Args:
        text (str): 음성으로 변환할 텍스트
        output_path (str): 저장할 오디오 파일 경로 (기본값: "output.mp3")
        api_key (str, optional): ElevenLabs API 키 (없으면 환경변수에서 가져옴)
        voice_id (str): 사용할 음성 ID (기본값: Rachel)
        model_id (str): 사용할 모델 ID (기본값: eleven_multilingual_v2)
    
    Returns:
        bool: 성공 여부
    """
    # API 키 가져오기 (환경변수 또는 직접 입력)
    if api_key is None:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("❌ 오류: ElevenLabs API 키가 필요합니다.")
            print("   환경변수 ELEVENLABS_API_KEY를 설정하거나 api_key 파라미터를 전달하세요.")
            return False
    
    # API 엔드포인트 URL
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    # 요청 헤더 설정
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    # 요청 데이터 설정
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,      # 안정성 (0.0 ~ 1.0)
            "similarity_boost": 0.75,  # 유사도 부스트 (0.0 ~ 1.0)
            "style": 0.0,          # 스타일 (0.0 ~ 1.0)
            "use_speaker_boost": True  # 화자 부스트 사용 여부
        }
    }
    
    try:
        print(f"🔄 텍스트를 음성으로 변환 중...")
        print(f"   텍스트: {text[:50]}..." if len(text) > 50 else f"   텍스트: {text}")
        
        # API 요청 보내기
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        # 응답 확인
        if response.status_code == 200:
            # 오디오 데이터를 파일로 저장
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)  # 디렉토리 생성
            
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = output_file.stat().st_size / 1024  # KB 단위
            print(f"✅ 음성 파일 저장 완료!")
            print(f"   경로: {output_path}")
            print(f"   크기: {file_size:.2f} KB")
            return True
        else:
            # 에러 응답 처리
            error_msg = response.text
            print(f"❌ API 요청 실패 (상태 코드: {response.status_code})")
            print(f"   오류 메시지: {error_msg}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 오류: API 요청 시간 초과")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 오류: API 요청 중 문제 발생")
        print(f"   상세: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 오류: 예상치 못한 문제 발생")
        print(f"   상세: {str(e)}")
        return False


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    파일명으로 사용할 수 있도록 텍스트를 정리합니다.
    특수문자를 제거하고 길이를 제한합니다.
    
    Args:
        text (str): 정리할 텍스트
        max_length (int): 최대 파일명 길이 (기본값: 50)
    
    Returns:
        str: 정리된 파일명
    """
    # 특수문자 제거 (한글, 영문, 숫자, 공백만 허용)
    cleaned = re.sub(r'[^\w\s가-힣]', '', text)
    # 공백을 언더스코어로 변경
    cleaned = re.sub(r'\s+', '_', cleaned)
    # 길이 제한
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    # 빈 문자열이면 기본값 사용
    if not cleaned:
        cleaned = "text"
    return cleaned


def generate_multiple_tts(
    sentences: List[str],
    output_dir: str = "tts_outputs",
    api_key: Optional[str] = None,
    voice_id: str = "8jHHF8rMqMlg8if2mOUe",
    model_id: str = "eleven_multilingual_v2"
) -> dict:
    """
    여러 문장을 순차적으로 TTS로 변환하고 각각 파일로 저장합니다.
    
    Args:
        sentences (List[str]): 변환할 문장 리스트
        output_dir (str): 출력 디렉토리 경로 (기본값: "tts_outputs")
        api_key (str, optional): ElevenLabs API 키
        voice_id (str): 사용할 음성 ID
        model_id (str): 사용할 모델 ID
    
    Returns:
        dict: 결과 딕셔너리 {"success": 성공 개수, "failed": 실패 개수, "files": 파일 경로 리스트}
    """
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 결과 저장용 변수
    success_count = 0
    failed_count = 0
    saved_files = []
    
    # 전체 문장 개수
    total = len(sentences)
    
    print(f"📝 총 {total}개의 문장을 TTS로 변환합니다.\n")
    print("=" * 60)
    
    # 각 문장을 순차적으로 처리
    for index, sentence in enumerate(sentences, 1):
        print(f"\n[{index}/{total}] 처리 중...")
        print(f"   문장: {sentence[:80]}..." if len(sentence) > 80 else f"   문장: {sentence}")
        
        # 파일명 생성 (문장 내용 기반)
        safe_filename = sanitize_filename(sentence)
        output_file = output_path / f"{safe_filename}.mp3"
        
        # TTS 생성 및 저장
        success = generate_tts_with_elevenlabs(
            text=sentence,
            output_path=str(output_file),
            api_key=api_key,
            voice_id=voice_id,
            model_id=model_id
        )
        
        if success:
            success_count += 1
            saved_files.append(str(output_file))
            print(f"   ✅ 완료: {output_file.name}")
        else:
            failed_count += 1
            print(f"   ❌ 실패: {sentence[:50]}...")
        
        # 구분선 출력
        if index < total:
            print("-" * 60)
    
    # 최종 결과 출력
    print("\n" + "=" * 60)
    print(f"\n📊 변환 완료!")
    print(f"   ✅ 성공: {success_count}개")
    print(f"   ❌ 실패: {failed_count}개")
    print(f"   📁 저장 위치: {output_dir}/")
    
    return {
        "success": success_count,
        "failed": failed_count,
        "files": saved_files
    }


# 사용 예시
if __name__ == "__main__":
    # 변환할 문장 리스트 (여기에 원하는 문장들을 입력하세요)
    sentences = [
        "크리스마스 하면 떠오르는 것은?",
        "크리스마스 트리",
        "산타 할아버지",
        "크리스마스에 더 하고 싶은 알바",
        "루돌프 대타 뛰기 (단 산타랑 썰매 엄청 무거움)",
        "산타 대타 뛰기 (단 무단 침입으로 오해 받을 수 있음)",
        "붕어빵 취향은?",
        "슈붕",
        "팥붕",
    ]
    
    # API 키 설정 (기본값 사용)
    api_key = "sk_92c9abfb8d79f63d8ad337bc05d711c20fdfe8c140beaec7"
    
    # 여러 문장을 순차적으로 TTS로 변환
    result = generate_multiple_tts(
        sentences=sentences,
        output_dir="tts_outputs",  # 출력 디렉토리
        api_key=api_key,
        voice_id="8jHHF8rMqMlg8if2mOUe",
        model_id="eleven_multilingual_v2"
    )
    
    print(f"\n🎉 모든 작업이 완료되었습니다!")