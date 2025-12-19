"""
ElevenLabs TTS 서비스
텍스트를 음성으로 변환하고 파일로 저장하는 서비스
"""
import requests
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class TTSRequest:
    """
    TTS 요청 구조체
    텍스트, 출력 경로, 음성 ID, 모델 ID를 포함
    output_path가 없으면 자동으로 tts_outputs 폴더에 저장됨
    """
    text: str
    voice_id: str
    model_id: str
    output_path: Optional[str] = None  # None이면 자동으로 tts_outputs에 저장
    
    @classmethod
    def rachel(cls, text: str, output_path: Optional[str] = None) -> 'TTSRequest':
        """
        레이첼 음성 프리셋으로 TTSRequest 생성
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str, optional): 저장할 오디오 파일 경로 (None이면 자동 생성)
        
        Returns:
            TTSRequest: 레이첼 음성 설정이 포함된 요청 객체
        """
        return cls(
            text=text,
            output_path=output_path,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # 레이첼 (영어)
            model_id="eleven_multilingual_v2"
        )
    
    @classmethod
    def default(cls, text: str, output_path: Optional[str] = None) -> 'TTSRequest':
        """
        기본 음성 프리셋으로 TTSRequest 생성
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str, optional): 저장할 오디오 파일 경로 (None이면 자동 생성)
        
        Returns:
            TTSRequest: 기본 음성 설정이 포함된 요청 객체
        """
        return cls(
            text=text,
            output_path=output_path,
            voice_id="8jHHF8rMqMlg8if2mOUe",  # 기본 음성
            model_id="eleven_multilingual_v2"
        )
    
    @classmethod
    def han(cls, text: str, output_path: Optional[str] = None) -> 'TTSRequest':
        """
        한(han) 음성 프리셋으로 TTSRequest 생성
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str, optional): 저장할 오디오 파일 경로 (None이면 자동 생성)
        
        Returns:
            TTSRequest: 한(han) 음성 설정이 포함된 요청 객체
        """
        return cls(
            text=text,
            output_path=output_path,
            voice_id="8jHHF8rMqMlg8if2mOUe",  # 한(han) 음성
            model_id="eleven_multilingual_v2"
        )


class TTSService:
    """ElevenLabs TTS 서비스 클래스"""
    
    # API 키 하드코딩 (인자로 받지 않음)
    API_KEY = "sk_92c9abfb8d79f63d8ad337bc05d711c20fdfe8c140beaec7"
    
    # 기본 설정 하드코딩
    DEFAULT_VOICE_ID = "8jHHF8rMqMlg8if2mOUe"
    DEFAULT_MODEL_ID = "eleven_multilingual_v2"
    
    # 음성 ID 상수 정의
    VOICE_RACHEL = "21m00Tcm4TlvDq8ikWAM"  # 레이첼 (영어)
    VOICE_DEFAULT = "8jHHF8rMqMlg8if2mOUe"  # 기본 음성
    
    # API 엔드포인트
    BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
    
    @classmethod
    def generate(cls, request: TTSRequest) -> Optional[Path]:
        """
        TTSRequest 구조체를 받아서 텍스트를 음성으로 변환하고 파일로 저장
        
        Args:
            request (TTSRequest): TTS 요청 구조체 (text, output_path, voice_id, model_id 포함)
        
        Returns:
            Path: 저장된 파일 경로 (실패 시 None)
        """
        try:
            # output_path가 없으면 자동으로 tts_outputs 폴더에 저장
            if request.output_path is None:
                import hashlib
                import time
                # 텍스트 기반으로 고유한 파일명 생성
                text_hash = hashlib.md5(request.text.encode()).hexdigest()[:8]
                timestamp = int(time.time())
                output_path = f"tts_outputs/tts_{timestamp}_{text_hash}.mp3"
            else:
                output_path = request.output_path
            
            # API 엔드포인트 URL
            url = f"{cls.BASE_URL}/{request.voice_id}"
            
            # 요청 헤더 설정
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": cls.API_KEY
            }
            
            # 요청 데이터 설정
            data = {
                "text": request.text,
                "model_id": request.model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            # API 요청 보내기
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            # 응답 확인
            if response.status_code == 200:
                # 오디오 데이터를 파일로 저장
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                return output_file
            else:
                # 에러 응답 처리
                error_msg = response.text
                print(f"❌ TTS API 요청 실패 (상태 코드: {response.status_code})")
                print(f"   오류 메시지: {error_msg}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ 오류: TTS API 요청 시간 초과")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 오류: TTS API 요청 중 문제 발생: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ 오류: TTS 생성 중 예상치 못한 문제 발생: {str(e)}")
            return None


# 싱글톤 인스턴스 생성 (편의를 위해)
tts_service = TTSService()

