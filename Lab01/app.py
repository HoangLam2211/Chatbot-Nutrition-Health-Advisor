from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Predefined answers for the Chatbot
predefined_answers = {
    "Làm thế nào để xây dựng một chế độ ăn uống cân bằng?": (
        "Chế độ ăn uống cân bằng bao gồm đầy đủ các nhóm thực phẩm: protein, carbohydrate, "
        "chất béo lành mạnh, vitamin, và khoáng chất. Hãy đảm bảo cung cấp đủ lượng rau, "
        "trái cây, ngũ cốc nguyên hạt, và thực phẩm giàu protein từ nguồn động vật và thực vật."
    ),
    
    "Những thực phẩm nào nên ăn để tăng cường hệ miễn dịch?": (
        "Các thực phẩm giàu vitamin C (cam, chanh, bưởi), vitamin E (hạt, quả hạch), kẽm "
        "(thịt, hải sản), và các chất chống oxy hóa (rau xanh, cà rốt) là những lựa chọn tốt "
        "để tăng cường hệ miễn dịch."
    ),
    
    "Làm thế nào để giảm cân một cách an toàn và hiệu quả?": (
        "Để giảm cân an toàn, hãy tập trung vào chế độ ăn uống giàu dinh dưỡng, kiểm soát "
        "khẩu phần ăn, kết hợp tập thể dục thường xuyên và tránh các chế độ ăn kiêng cực đoan. "
        "Giảm cân nên diễn ra từ từ với mục tiêu khoảng 0.5-1kg mỗi tuần."
    ),
    
    "Chế độ ăn uống nào phù hợp cho người mắc bệnh tiểu đường?": (
        "Người mắc bệnh tiểu đường nên ăn các loại carbohydrate phức hợp như ngũ cốc nguyên hạt, "
        "đậu, và rau xanh. Hạn chế đường đơn và thực phẩm chế biến sẵn, chia nhỏ bữa ăn và "
        "kiểm soát lượng carbohydrate hấp thụ mỗi ngày."
    ),
    
    "Có nên bổ sung vitamin và khoáng chất từ thực phẩm chức năng không?": (
        "Bổ sung vitamin và khoáng chất nên dựa trên sự tư vấn của bác sĩ hoặc chuyên gia dinh dưỡng. "
        "Hầu hết các chất dinh dưỡng cần thiết có thể được cung cấp qua chế độ ăn uống đa dạng và lành mạnh."
    ),
    
    "Làm thế nào để duy trì một lối sống lành mạnh?": (
        "Duy trì lối sống lành mạnh bằng cách ăn uống cân bằng, tập thể dục thường xuyên, ngủ đủ giấc, "
        "quản lý căng thẳng, và duy trì các mối quan hệ xã hội tích cực. Tránh các thói quen không lành mạnh "
        "như hút thuốc và tiêu thụ rượu bia quá mức."
    ),

    "Nên ăn bao nhiêu bữa một ngày để duy trì sức khỏe tốt?": (
        "Thông thường, ăn 3 bữa chính và 1-2 bữa phụ sẽ giúp duy trì năng lượng và sức khỏe tốt. "
        "Quan trọng là cân bằng lượng calo trong ngày và chọn thực phẩm giàu dinh dưỡng."
    ),
    
    "Chất béo nào là tốt cho sức khỏe?": (
        "Chất béo không bão hòa có lợi cho sức khỏe, bao gồm chất béo từ dầu ô liu, quả bơ, hạt, "
        "và các loại cá giàu omega-3 như cá hồi. Hạn chế chất béo bão hòa và trans từ thực phẩm chế biến sẵn."
    ),
    
    "Làm thế nào để tăng cân lành mạnh?": (
        "Để tăng cân lành mạnh, hãy ăn nhiều bữa trong ngày, bổ sung các thực phẩm giàu protein "
        "như thịt nạc, trứng, đậu, và thực phẩm giàu calo lành mạnh như các loại hạt, dầu thực vật, và bơ."
    ),
    
    "Nên uống bao nhiêu nước mỗi ngày?": (
        "Lượng nước cần thiết phụ thuộc vào cơ thể mỗi người, nhưng một khuyến nghị phổ biến là 8 ly nước "
        "(khoảng 2 lít) mỗi ngày. Hãy uống nhiều hơn khi hoạt động thể chất hoặc trong thời tiết nóng."
    ),
    
    "Nên tránh những thực phẩm nào để kiểm soát huyết áp?": (
        "Để kiểm soát huyết áp, bạn nên hạn chế muối, thực phẩm chế biến sẵn, đồ ăn nhanh và đồ uống có cồn. "
        "Tăng cường các thực phẩm giàu kali như chuối, khoai tây và rau xanh để giúp cân bằng huyết áp."
    ),
    
    "Thực phẩm nào giúp cải thiện tiêu hóa?": (
        "Thực phẩm giàu chất xơ như rau xanh, hoa quả, ngũ cốc nguyên hạt, và đậu sẽ giúp cải thiện tiêu hóa. "
        "Cũng nên uống nhiều nước và ăn sữa chua để hỗ trợ hệ vi sinh đường ruột."
    ),
    
    "Người ăn chay nên bổ sung những dưỡng chất nào?": (
        "Người ăn chay cần chú ý bổ sung protein từ các nguồn như đậu, hạt, và đậu nành. "
        "Cần bổ sung thêm vitamin B12, sắt, canxi, và omega-3 từ thực phẩm hoặc thực phẩm chức năng."
    ),
    
    "Làm thế nào để hạn chế ăn đồ ngọt?": (
        "Để hạn chế đồ ngọt, hãy thay thế đồ ngọt bằng trái cây, giảm dần lượng đường trong chế độ ăn, "
        "và chọn các loại thực phẩm ít đường. Kiểm soát cảm giác thèm ăn bằng cách ăn bữa đầy đủ dưỡng chất."
    ),
    
    "Thực phẩm nào giúp tăng cường trí nhớ và tập trung?": (
        "Các thực phẩm giàu omega-3 như cá hồi, quả óc chó, và hạt lanh có thể giúp cải thiện trí nhớ "
        "và tập trung. Ngoài ra, các loại quả mọng, rau xanh và trà xanh cũng có lợi cho não bộ."
    ),
    
    "Nên ăn gì trước và sau khi tập thể dục?": (
        "Trước khi tập thể dục, hãy ăn thực phẩm giàu carbohydrate như chuối hoặc bánh mì nguyên cám "
        "để cung cấp năng lượng. Sau khi tập, ăn các món giàu protein như ức gà hoặc sữa chua để phục hồi cơ bắp."
    ),
    
    "Thực phẩm nào giàu protein ngoài thịt?": (
        "Ngoài thịt, bạn có thể bổ sung protein từ đậu, đậu phụ, hạt quinoa, hạt chia, sữa và trứng. "
        "Các loại hạt và sản phẩm từ đậu nành cũng là nguồn protein thực vật tốt."
    ),
    
    "Có nên uống cà phê mỗi ngày không?": (
        "Uống cà phê mỗi ngày ở mức vừa phải (khoảng 1-2 cốc) có thể mang lại lợi ích cho sức khỏe "
        "như tăng cường năng lượng và tập trung. Tuy nhiên, hãy hạn chế đường và kem trong cà phê, "
        "và tránh uống quá nhiều để tránh ảnh hưởng đến giấc ngủ."
    ),
    
    "Chế độ ăn kiêng keto là gì?": (
        "Chế độ ăn kiêng keto là chế độ ăn ít carbohydrate và nhiều chất béo, giúp cơ thể chuyển sang "
        "đốt cháy chất béo thay vì carbohydrate. Tuy nhiên, không phải ai cũng phù hợp với chế độ này, "
        "hãy tham khảo ý kiến chuyên gia trước khi thực hiện."
    ),
    
    "Làm thế nào để quản lý cơn thèm ăn vặt?": (
        "Để quản lý cơn thèm ăn vặt, hãy ăn đủ bữa và đảm bảo chế độ ăn giàu dinh dưỡng. "
        "Chọn đồ ăn vặt lành mạnh như trái cây, hạt, và yogurt thay vì đồ ăn nhiều đường và calo."
    ),
    
    "Thực phẩm nào giúp cải thiện chất lượng giấc ngủ?": (
        "Các thực phẩm giàu tryptophan như sữa, chuối, và hạt giúp cải thiện giấc ngủ. "
        "Ngoài ra, uống trà hoa cúc hoặc tránh caffeine trước khi ngủ cũng hỗ trợ giấc ngủ tốt hơn."
    ),
    
    "Ai là người đẹp trai nhất?": (
        "Một câu hỏi tuyệt vời, tất nhiên là anh Hoàng Lâm rồi!"
    ),
    
    "Làm thế nào để giảm cân an toàn?": (
        "Giảm cân an toàn cần duy trì chế độ ăn uống hợp lý và kết hợp tập thể dục thường xuyên."
    ),
    
    "Tôi nên ăn gì để tăng cường hệ miễn dịch?": (
        "Bạn nên ăn các thực phẩm giàu vitamin C và kẽm như cam, chanh, hạt bí."
    ),
    
    "Làm sao để có một chế độ dinh dưỡng cân bằng?": (
        "Chế độ ăn cân bằng bao gồm đủ chất đạm, chất xơ, vitamin và khoáng chất."
    ),
    
    "Tôi có thể dùng loại thực phẩm bổ sung nào?": (
        "Bạn nên tham khảo ý kiến bác sĩ trước khi sử dụng bất kỳ loại thực phẩm bổ sung nào."
    ),

    "Chào bạn": (
        "Chào bạn, tôi có thể giúp gì?"
    )
}


# Store chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

# Handle messages from client
@socketio.on('message')
def handle_message(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response = predefined_answers.get(msg, "Xin lỗi, tôi không hiểu câu hỏi của bạn. Vui lòng hỏi lại!")
    
    # Store chat history
    chat_history.append({'user': msg, 'bot': response, 'time': timestamp})
    
    # Send response with time to user
    send({'msg': response, 'time': timestamp}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
