"""
ElevenLabs TTS 서비스
텍스트를 음성으로 변환하고 파일로 저장하는 서비스
"""
import requests
from pathlib import Path
from typing import Optional


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
    def generate_tts(cls, text: str, output_path: str) -> Optional[Path]:
        """
        텍스트를 음성으로 변환하고 파일로 저장 (기본 설정 사용)
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str): 저장할 오디오 파일 경로
        
        Returns:
            Path: 저장된 파일 경로 (실패 시 None)
        """
        return cls.generate_tts_with_voice(
            text=text,
            output_path=output_path,
            voice_id=cls.DEFAULT_VOICE_ID,
            model_id=cls.DEFAULT_MODEL_ID
        )
    
    @classmethod
    def generate_tts_with_voice(
        cls, 
        text: str, 
        output_path: str, 
        voice_id: str, 
        model_id: str
    ) -> Optional[Path]:
        """
        텍스트를 음성으로 변환하고 파일로 저장 (voice_id와 model_id 지정)
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str): 저장할 오디오 파일 경로
            voice_id (str): 사용할 음성 ID
            model_id (str): 사용할 모델 ID
        
        Returns:
            Path: 저장된 파일 경로 (실패 시 None)
        """
        try:
            # API 엔드포인트 URL
            url = f"{cls.BASE_URL}/{voice_id}"
            
            # 요청 헤더 설정
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": cls.API_KEY
            }
            
            # 요청 데이터 설정
            data = {
                "text": text,
                "model_id": model_id,
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
    
    @classmethod
    def rachel(cls, text: str, output_path: str) -> Optional[Path]:
        """
        레이첼 음성으로 텍스트를 음성으로 변환하고 파일로 저장
        
        Args:
            text (str): 음성으로 변환할 텍스트
            output_path (str): 저장할 오디오 파일 경로
        
        Returns:
            Path: 저장된 파일 경로 (실패 시 None)
        """
        return cls.generate_tts_with_voice(
            text=text,
            output_path=output_path,
            voice_id=cls.VOICE_RACHEL,
            model_id=cls.DEFAULT_MODEL_ID
        )


# 싱글톤 인스턴스 생성 (편의를 위해)
tts_service = TTSService()

