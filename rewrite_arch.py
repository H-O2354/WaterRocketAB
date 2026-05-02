import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = "<!-- ARCHITECTURE MODAL -->"
end_str = "<!-- SCRIPT SECTION -->"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

arch_modal_html = """<!-- ARCHITECTURE MODAL -->
    <div id="arch-modal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="document.getElementById('arch-modal').style.display='none'">&times;</span>
            <div class="doc-container" style="padding:0; box-shadow:none; border:none; background:transparent;">
            <h2>Kiến Trúc Hệ Thống (System Architecture)</h2>
            <p>Sơ đồ Luồng xử lý tính toán Vật lý</p>
            <ul class="tree">
                <li class="tree-head">compute_derivatives(t, Y, params)</li>
                <li>
                    <span class="tree-title">1. GIẢI NÉN VECTOR TRẠNG THÁI & THAM SỐ</span>
                    <ul>
                        <li>Trích xuất biến thiên (Y): x, y, vx, vy, m_w, P</li>
                        <li>Trích xuất hằng số (params): C_d, A_c, A_e, rho_w, rho_air, P_atm, g, V_0 ...</li>
                    </ul>
                </li>
                <li>
                    <span class="tree-title">2. KHÍ ĐỘNG HỌC & LỰC CẢN (Fd)</span>
                    <ul>
                        <li>Xác định hướng và độ lớn vận tốc</li>
                        <li>Tính độ ổn định Static Margin</li>
                        <li>Hệ số cản hiệu dụng (WOBBLE_FACTOR)</li>
                        <li>Tính lực cản F_d</li>
                    </ul>
                </li>
                <li>
                    <span class="tree-title">3. BIẾN DẠNG VỎ CHAI (PET Elasticity)</span>
                    <ul>
                        <li>Tính gia tốc dọc trục</li>
                        <li>Độ phình Hooke</li>
                    </ul>
                </li>
                <li>
                    <span class="tree-title">4. BỘ ĐỊNH TUYẾN LỰC ĐẨY (MAIN PHASE TREE)</span>
                    <ul>
                        <li>
                            <span class="tree-title">[PHA A]: CÒN NƯỚC (if m_w > 0)</span>
                            <ul>
                                <li><strong>A1: Trong ống phóng</strong> (Lực ma sát O-ring, tụt áp)</li>
                                <li><strong>A2: Đã rời ống phóng</strong> (Áp suất đáy, lưu lượng khối lượng nước, lực đẩy nước)</li>
                                <li><strong>Nhiệt Động Học Pha A</strong> (Khí nén đẩy nước, trao đổi nhiệt)</li>
                            </ul>
                        </li>
                        <li>
                            <span class="tree-title">[PHA B]: HẾT NƯỚC, CÒN KHÍ (else if P > P_atm)</span>
                            <ul>
                                <li><strong>B1: Dùng Hóa Học</strong> (Tốc độ phản ứng sinh khí)</li>
                                <li><strong>B2: Dùng Khí Nén Xả Trực Tiếp</strong> (Nghẹt/Choked Flow hoặc Dưới âm/Subsonic flow)</li>
                                <li><strong>Nhiệt Động Học Pha B</strong> (Khí tự xả làm lạnh buồng đốt)</li>
                            </ul>
                        </li>
                        <li>
                            <span class="tree-title">[PHA C]: BAY TỰ DO / COASTING (else)</span>
                            <ul>
                                <li>Lực đẩy = 0, áp suất cân bằng với môi trường</li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li>
                    <span class="tree-title">5. TỔNG HỢP GIA TỐC BƯỚC NHẢY (NEWTON 2)</span>
                    <ul>
                        <li>Khối lượng tổng: m_total = m_empty + m_w + m_air</li>
                        <li>Ràng buộc mặt đất (chống lún)</li>
                        <li>Bay tự do (Thrust, F_d, Gravity)</li>
                    </ul>
                </li>
            </ul>
            <p><strong>OUTPUT:</strong> Trả về các đạo hàm [vx, vy, ax, ay, dm_w/dt, dP/dt]</p>
            </div>
        </div>
    </div>

    """

html = html[:start_idx] + arch_modal_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
