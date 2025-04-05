# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import gradio as gr
from service.langraph_service import run_langraph_pipeline
from service.vectordb_upload_service import update_vectordb
def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

if __name__ == '__main__':

    load_dotenv()
    # app = FastAPI(
    #     title="KBank PoC",
    #     version="0.1.0",
    #     description="Kbank Proof-of-Concept API"
    # )

    def sample1(input):
        return 123


    with gr.Blocks() as demo:
        gr.Markdown("### LangGraph 기반 질의응답 & vectorDB 파일 업로드")

        with gr.Tab("💬 질의응답"):
            question = gr.Textbox(label="질문")
            answer = gr.Textbox(label="응답")
            ask_btn = gr.Button("질문하기")
            ask_btn.click(fn=run_langraph_pipeline, inputs=question, outputs=answer)

        with gr.Tab("📁 파일 업로드"):
            file_input = gr.File(label="업로드할 파일", file_types=[".pdf", ".ppt", ".pptx", ".csv", ".xlsx", ".xls"])
            output = gr.Textbox(label="결과")
            upload_button = gr.Button("📌 VectorDB에 저장")
            upload_button.click(fn=update_vectordb, inputs=[file_input], outputs=[output])

    demo.launch()