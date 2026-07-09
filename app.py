import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Cấu hình API Key cho Gemini
# Bạn có thể dán trực tiếp Key vào đây, hoặc hệ thống sẽ tự đọc từ môi trường khi đưa lên mạng
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    problem_text = ""
    
    if request.method == "POST":
        problem_text = request.form.get("problem")
        
        try:
            # Sử dụng mô hình Gemini 1.5 Flash để xử lý nhanh và chính xác
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Tạo câu lệnh định hướng cho AI trả lời như một giáo viên
            prompt = f"Bạn là một giáo viên toán giỏi. Hãy giải bài toán sau đây một cách chi tiết, rõ ràng từng bước và dễ hiểu nhất: {problem_text}"
            
            result = model.generate_content(prompt)
            response_text = result.text
        except Exception as e:
            response_text = f"❌ Đã xảy ra lỗi: {str(e)}"

    return render_template("index.html", problem=problem_text, response=response_text)

if __name__ == "__main__":
    # Lấy cổng port tự động từ server khi đưa lên mạng, mặc định chạy local là 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)