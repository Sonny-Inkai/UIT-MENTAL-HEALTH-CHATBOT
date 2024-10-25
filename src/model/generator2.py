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
HF_TOKENS = os.getenv("HF_TOKENS")

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
    top_k=5,
)

ranker = TransformersSimilarityRanker(
    model="namdp-ptit/ViRanker",
    token=Secret.from_token(HF_TOKENS),
    score_threshold=0.72,
    top_k=2  # Chọn lọc ra 5 tài liệu phù hợp nhất sau khi rank
)
ranker.warm_up()

# Bước 4: Setup ChatPromptBuilder chỉ một lần khi ứng dụng được khởi động
prompt_builder = ChatPromptBuilder(template=[
    ChatMessage.from_system("Bạn là một trợ lý tư vấn tâm lý thân thiện và hỗ trợ, dành cho học sinh sinh viên Việt Nam, đặc biệt là sinh viên Trường đại học công nghệ thông tin (UIT) Thành phố hồ chí minh. Nhiệm vụ của bạn là lắng nghe và đồng cảm với những chia sẻ của sinh viên, đồng thời cung cấp lời khuyên về sức khỏe tâm thần một cách nhẹ nhàng và chân thành. Hãy trả lời các câu hỏi bằng ngôn ngữ dễ hiểu, gần gũi, và đưa ra những gợi ý hữu ích, toàn diện, giúp sinh viên cảm thấy được thấu hiểu và có định hướng rõ ràng hơn trong việc cải thiện sức khỏe tâm lý của mình. Luôn nhớ rằng mục tiêu của bạn là mang lại sự an ủi và cảm giác an toàn cho sinh viên."),
    ChatMessage.from_user("Các thông tin các câu truyện chữa lành, câu nói truyền động lực bạn có thể tham khảo ở đây:\\n{{ ranker_documents }} \\n\\n Tuy nhiên hãy nhớ rằng không phải lúc nào các thông tin tham khảo này cũng phù hợp với yêu cầu cua sinh viên, do đó bạn cần chú ý trả lời câu hỏi của sinh viên, và thông tin được cung cấp chỉ là hỗ trợ. Đây là câu hỏi của sinh viên: {{ user_question }}. Hãy trả lời dễ hiểu, gần gũi, đưa ra những gợi ý hữu ích, súc tích, và thân thiện nhất. \\n\\n Trả lời: "),
])

# Bước 5: Setup OpenAIChatGenerator chỉ một lần khi ứng dụng được khởi động
chat_generator = OpenAIChatGenerator(
    api_key=Secret.from_env_var("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

# Bước 6: Tạo và kết nối Pipeline chỉ một lần khi ứng dụng được khởi động
pipeline = Pipeline()
pipeline.add_component("text_embedder", text_embedder)
pipeline.add_component("retriever", retriever)
pipeline.add_component("ranker", ranker)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", chat_generator)

pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever.documents", "ranker.documents")
pipeline.connect("ranker.documents", "prompt_builder.ranker_documents")
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
            "ranker":{"query": user_question},
            "prompt_builder": {"user_question": user_question}
        })

        # Trả về phản hồi
        return jsonify({"response": response["llm"]["replies"][0].content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
