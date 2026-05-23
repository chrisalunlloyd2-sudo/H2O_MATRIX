import os
import asyncio
import sys

# Dynamic path injection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from genetic_flow.memory_pipeline.rag_interceptor import RAGInterceptor
from genetic_flow.memory_pipeline.audio_engine import AudioManifestationEngine
from genetic_flow.core_brain.router import LocalAgentRouter

class HeadlessOrchestrator:
    def __init__(self):
        self.rag = RAGInterceptor()
        self.tts = AudioManifestationEngine()
        self.router = LocalAgentRouter()

    async def handle_input(self, user_input):
        # 1. RAG Pre-Flight
        context = self.rag.pre_flight_query(user_input)
        
        # 2. LLM Generation
        response = self.router.run_generation(user_input, str(context))
        
        # 3. Memory Persistence
        self.rag.log_event("cli_interaction", f"Q: {user_input} | A: {response}")
        
        # 4. Async Headless Audio Feedback
        await self.tts.run_audio_feedback(response)

if __name__ == "__main__":
    orchestrator = HeadlessOrchestrator()
    asyncio.run(orchestrator.handle_input("System memory initialized."))
