import re

with open('index.html', 'r') as f:
    content = f.read()

translations = {
    # Main Header
    r'WATER ROCKET TELEMETRY DASHBOARD': r'BẢNG ĐIỀU KHIỂN ĐO LƯỜNG TÊN LỬA NƯỚC',
    r'PHYSICS & MATH DOCS': r'TÀI LIỆU VẬT LÝ & TOÁN HỌC',
    r'SYSTEM ARCHITECTURE': r'KIẾN TRÚC HỆ THỐNG',
    r'FORCE RECALCULATE': r'BẮT BUỘC TÍNH TOÁN LẠI',

    # Left Pane (Controls)
    r'<legend>Geometry & Mass</legend>': r'<legend>Hình học & Khối lượng</legend>',
    r'Bottle Volume \(L\)': r'Thể tích chai (L)',
    r'Total Length \(mm\)': r'Chiều dài tổng thể (mm)',
    r'Body Diameter \(mm\)': r'Đường kính thân (mm)',
    r'Empty Mass \(kg\)': r'Khối lượng rỗng (kg)',
    r'Nose Ballast \(kg\)': r'Khối lượng tạ mũi (kg)',
    r'Fin Root Chord \(mm\)': r'Chiều dài chân cánh (mm)',
    r'Fin Tip Chord \(mm\)': r'Chiều dài đỉnh cánh (mm)',
    r'Fin Span \(mm\)': r'Sải cánh (mm)',

    r'<legend>Energy & Propellant \(AIR\)</legend>': r'<legend>Năng lượng & Nhiên liệu (AIR)</legend>',
    r'Water Ratio \(%\)': r'Tỷ lệ đổ nước (%)',
    r'Initial Pressure \(PSI\)': r'Áp suất bơm ban đầu (PSI)',
    r'Burst Limit \(PSI\)': r'Áp suất nổ giới hạn (PSI)',

    r'<legend>Chemical Reaction \(CHEM\)</legend>': r'<legend>Phản ứng Hóa học (CHEM)</legend>',
    r'Carbonate Type': r'Loại muối (g/mol)',
    r'Baking Soda \(84 g/mol\)': r'Baking Soda (84 g/mol)',
    r'Washing Soda \(106 g/mol\)': r'Washing Soda (106 g/mol)',
    r'Mass of Salt \(g\)': r'Khối lượng muối (g)',
    r'Volume of Vinegar \(ml\)': r'Thể tích giấm (ml)',
    r'Acid Conc\. \(% m/v\)': r'Nồng độ Acid (% m/v)',
    r'Gas Yield Eff\. \(%\)': r'Hiệu suất sinh khí (%)',
    r'Pop-off Pressure \(PSI\)': r'Áp suất bung nút (PSI)',

    r'<legend>Thrust System</legend>': r'<legend>Hệ thống Lực đẩy</legend>',
    r'Nozzle Diameter \(mm\)': r'Đường kính Vòi phun (mm)',
    r'Launch Tube Length \(m\)': r'Chiều dài ống phóng (m)',
    r'Launch Tube OD \(mm\)': r'Đường kính ngoài ống phóng (mm)',
    r'-> Cork Friction REQD': r'-> Yêu cầu Ma sát Nút bần',

    r'<legend>Trajectory & Environment</legend>': r'<legend>Quỹ đạo & Môi trường</legend>',
    r'Launch Angle \(Deg\)': r'Góc phóng (Độ)',
    r'Drag Coefficient \(Cd\)': r'Hệ số cản không khí (Cd)',
    r'Air Temperature \(C\)': r'Nhiệt độ không khí (C)',
    r'Air Density \(kg/m³\)': r'Mật độ không khí (kg/m³)',
    r'1\.225 \(Sea Level\)': r'1.225 (Ngang mực nước biển)',
    r'1\.056 \(High Altitude\)': r'1.056 (Trên vùng núi cao)',

    r'RUN CMA-ES OPTIMIZER': r'CHẠY TỐI ƯU HÓA CMA-ES',

    # Modes
    r'ENGINE MODE': r'CHẾ ĐỘ ĐỘNG CƠ',
    r'AIR PUMP MODE': r'CHẾ ĐỘ BƠM KHÍ',
    r'CHEMICAL REACTION': r'PHẢN ỨNG HÓA HỌC',

    # Right Pane (Telemetry Stats)
    r'SYSTEM STATUS: NOMINAL': r'TRẠNG THÁI HỆ THỐNG: BÌNH THƯỜNG',
    r'Actual Range': r'Tầm xa Thực tế',
    r'Ideal Range \(Vacuum\)': r'Tầm xa Lý thuyết (Chân không)',
    r'Apogee \(Max Alt\)': r'Đỉnh quỹ đạo (Cao tối đa)',
    r'Max Velocity': r'Vận tốc tối đa',
    r'Flight Time': r'Thời gian bay',
    r'Burn Time': r'Thời gian đốt',

    # Chart Controls
    r'Reset Zoom': r'Đặt lại Zoom',

    # JS System Status
    r'sys_status: "NOMINAL"': r'sys_status: "BÌNH THƯỜNG"',
    r'"SYSTEM STATUS: " \+ msg': r'"TRẠNG THÁI HỆ THỐNG: " + msg',
    r'BOTTLE BURST \(P > LIMIT\)': r'CHAI NỔ (P > GIỚI HẠN)',
    r'FAILED TO LIFT OFF \(P < POPOFF\)': r'KHÔNG THỂ CẤT CÁNH (P < BUNG NÚT)',
    r'SIMULATION ERROR': r'LỖI MÔ PHỎNG',
}

for k, v in translations.items():
    content = re.sub(k, v, content)

with open('index.html', 'w') as f:
    f.write(content)
