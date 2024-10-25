# src/model/generator.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack import Pipeline, Document
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Load thông tin bảo mật từ biến môi trường
CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
API_KEY = os.getenv("ELASTIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Tạo Flask App
app = Flask(__name__)
CORS(app)  # Cho phép tất cả các nguồn được truy cập vào API này

# Bước 1: Kết nối đến Elasticsearch Deployment trên Elastic Cloud
# Khởi tạo ElasticsearchDocumentStore chỉ một lần khi ứng dụng được khởi động
document_store = ElasticsearchDocumentStore(
    cloud_id=CLOUD_ID,
    api_key=API_KEY,
    index="uit_mental_health",
)

# Bước 2: Khởi tạo Text Embedder chỉ một lần khi ứng dụng được khởi động
text_embedder = SentenceTransformersTextEmbedder(model="intfloat/multilingual-e5-small")
text_embedder.warm_up()  # Ensure the model is loaded and ready

# Bước 3: Khởi tạo Elasticsearch Embedding Retriever chỉ một lần khi ứng dụng được khởi động
retriever = ElasticsearchEmbeddingRetriever(
    document_store=document_store,
    top_k=1,
)

# Bước 4: Setup ChatPromptBuilder chỉ một lần khi ứng dụng được khởi động
prompt_builder = ChatPromptBuilder(template=[
    ChatMessage.from_system(
        "Bạn là một trợ lý tư vấn tâm lý thân thiện và hỗ trợ, đặc biệt dành cho học sinh sinh viên Việt Nam, nhất là sinh viên Trường Đại học Công nghệ Thông tin (UIT) Thành phố Hồ Chí Minh. "
        "Nhiệm vụ của bạn là lắng nghe, đồng cảm, và cung cấp lời khuyên về sức khỏe tâm thần một cách nhẹ nhàng, chân thành. "
        "Bạn hãy sử dụng ngôn ngữ gần gũi, dễ hiểu và cố gắng đưa ra những gợi ý hữu ích, toàn diện, giúp sinh viên cảm thấy được thấu hiểu và có định hướng rõ ràng hơn trong việc cải thiện sức khỏe tâm lý của mình. "
        "Luôn nhớ rằng mục tiêu chính của bạn là mang lại sự an ủi và cảm giác an toàn cho sinh viên."
    ),
    ChatMessage.from_user(
        "Dưới đây là một số thông tin tham khảo bao gồm các câu chuyện chữa lành, câu nói truyền động lực, và các tài liệu khác có thể hữu ích: \\n"
        "{{ retriever_documents }} \\n\\n"
        "Tuy nhiên, hãy nhớ rằng các thông tin tham khảo này chỉ là hỗ trợ và không nhất thiết phải áp dụng cho mọi tình huống của sinh viên. "
        "Do đó, điều quan trọng là bạn cần ưu tiên lắng nghe và phản hồi trực tiếp dựa trên câu hỏi cụ thể của sinh viên. "
        "Hãy trả lời một cách rõ ràng, gần gũi, sử dụng các từ ngữ thân thiện, và tập trung vào đưa ra các lời khuyên cụ thể, súc tích nhưng mang tính hỗ trợ sâu sắc. "
        "Luôn đảm bảo rằng câu trả lời của bạn là thân thiện, dễ tiếp cận, súc tích, ngắn gọn, và mang lại cảm giác an toàn cho sinh viên. "
        "Đây là câu hỏi của sinh viên: {{ user_question }}. "
        "\\n\\n "
        "Trả lời: "
    ),
])

# Bước 5: Setup OpenAIChatGenerator chỉ một lần khi ứng dụng được khởi động
chat_generator = OpenAIChatGenerator(
    api_key=Secret.from_env_var("OPENAI_API_KEY"),
    model="gpt-4o"
)

# Bước 6: Tạo và kết nối Pipeline chỉ một lần khi ứng dụng được khởi động
pipeline = Pipeline()
pipeline.add_component("text_embedder", text_embedder)
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", chat_generator)

pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever.documents", "prompt_builder.retriever_documents")
pipeline.connect("prompt_builder.prompt", "llm.messages")

# Bước 7: Tạo Endpoint cho API
@app.route('/generate-response', methods=['POST'])
def generate_response():
    try:
        # Lấy query từ yêu cầu của người dùng
        user_data = request.get_json()
        user_question = user_data.get("query")

        # Chạy Pipeline với câu hỏi của người dùng
        response = pipeline.run({
            "text_embedder": {"text": user_question},
            "prompt_builder": {"user_question": user_question}
        })

        # Trả về phản hồi
        return jsonify({"response": response["llm"]["replies"][0].content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
