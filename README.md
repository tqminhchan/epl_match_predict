
Scripts
1. clean_data.py
Bao gồm các hàm trợ giúp cần thiết để xử lý dữ liệu gốc
2. current_status.py
Thu thập và thêm thông tin chi tiết hơn vào dữ liệu gốc đã xử lý
Bảng xếp hạng hiện tại/qua khứ, số bàn thắng/gỡ/bị thủng lưới, v.v.
3. match_history.py
Thu thập kết quả trận đấu mới nhất
4. rankings.py
Tính điểm và tạo bảng xếp hạng
5. sofifa_scraper.py
Cào dữ liệu thống kê tổng quát về đội bóng từ FIFA
6. predict.py
Sử dụng dữ liệu đã xử lý, huấn luyện một mô hình ML để dự đoán kết quả trong tương lai
7. model.py
Tệp I/O trong đó các chức năng từ các tệp trên thực sự được thực thi
 
 

Data
1. data/raw/OVAs (thư mục)
Dữ liệu thống kê tổng quát về đội bóng được cào
2. data/cleaned/standings (thư mục)
Kết quả xếp hạng lịch sử được tính toán trong rankings.py
3. data/raw/results (thư mục)
Dữ liệu lịch sử về kết quả trận đấu được thu thập thủ công
Kết quả trận đấu mới nhất của mùa giải hiện tại
4. data/cleaned/results (thư mục)
Dữ liệu được trích xuất từ data/raw/results
5. data/train_data/results (thư mục)
Dữ liệu được xử lý từ data/cleaned/results
6. data/statistics (thư mục)
data/statistics/round_rankings (thư mục)
Bảng xếp hạng được tính toán dựa trên kết quả dự đoán của trận đấu
Mỗi tệp trong thư mục có chứa một ngày trong tên của nó. Nó cung cấp kết quả xếp hạng dự đoán vào ngày được chỉ định
data/statistics/prediction_ranking.csv
Xếp hạng dự đoán vào cuối mùa giải
data/statistics/prediction_result.csv
Dự đoán kết quả trận đấu cá nhân
data/statistics/round_rankings_summary.csv
Tóm tắt kết quả xếp hạng dự đoán trong suốt mùa giải
7. data/statistics/best_clf.joblib
Bộ nhớ đệm đĩa của bộ phân loại đạt độ chính xác tốt nhất trong dự đoán
8. data/database.db
Cơ sở dữ liệu SQL lưu trữ kết quả trận đấu trước đó, kết quả dự đoán trận đấu và kết quả xếp hạng dự đoán
9. data/train_data/final.csv
Tệp csv được sử dụng để huấn luyện mô hình và thực hiện dự đoán
10. data/statistics/model_confidence.csv
Danh sách các bộ phân loại được tìm kiếm trên lưới và điểm tin cậy của chúng