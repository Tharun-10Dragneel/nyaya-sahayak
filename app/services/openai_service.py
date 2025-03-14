from tenacity import retry, stop_after_attempt, wait_exponential
import openai
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for interacting with Azure OpenAI to process legal queries"""
    
    def __init__(self):
        # Configure Azure OpenAI client
        openai.api_type = "azure"
        openai.api_key = settings.AZURE_OPENAI_API_KEY
        openai.api_base = settings.AZURE_OPENAI_ENDPOINT
        openai.api_version = "2023-05-15"
        
        # Set deployment name (model name in Azure)
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def get_legal_response(self, query, language="english"):
        """Get legal information response from Azure OpenAI"""
        try:
            system_message = """
            You are Nyaya Sahayak, a legal assistant helping people in India understand legal procedures and rights.
            Provide helpful, accurate, and easy-to-understand information about Indian laws and legal processes.
            Keep responses concise and focused on practical steps.
            If you don't know something, acknowledge it and suggest contacting a legal professional.
            For emergency situations, recommend appropriate helplines (Women: 181, Child: 1098, Police: 112).
            """
            
            user_message = f"Query in {language}: {query}"
            
            logger.info(f"Sending query to Azure OpenAI: {query[:50]}...")
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message["content"].strip()
            logger.info(f"Received response from Azure OpenAI: {content[:50]}...")
            return content
            
        except Exception as e:
            logger.error(f"Error with Azure OpenAI: {e}")
            raise
