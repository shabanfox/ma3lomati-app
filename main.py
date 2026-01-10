<div id="roi-calc" style="background: #ffffff; padding: 20px; border-radius: 12px; border: 2px solid #3498db; direction: rtl; font-family: sans-serif; margin-top: 20px;">
    <h3 style="color: #2c3e50;">📈 حاسبة العائد على الاستثمار (ROI)</h3>
    <div style="margin-bottom: 15px;">
        <label>إجمالي سعر الشراء (شامل المصاريف):</label>
        <input type="number" id="buyPrice" style="width: 100%; padding: 8px; margin-top: 5px;">
    </div>
    <div style="margin-bottom: 15px;">
        <label>الإيجار الشهري المتوقع:</label>
        <input type="number" id="monthlyRent" style="width: 100%; padding: 8px; margin-top: 5px;">
    </div>
    <button onclick="calculateROI()" style="background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; width: 100%;">احسب العائد السنوي</button>
    
    <div id="res-roi" style="margin-top: 20px; font-weight: bold; color: #2ecc71;"></div>
</div>

<script>
function calculateROI() {
    let price = document.getElementById('buyPrice').value;
    let rent = document.getElementById('monthlyRent').value;
    
    let annualRent = rent * 12;
    let roi = (annualRent / price) * 100;
    
    document.getElementById('res-roi').innerHTML = 
        `العائد السنوي الصافي: ${roi.toFixed(2)}% <br> إجمالي الدخل السنوي: ${annualRent.toLocaleString()} ج.م`;
}
</script>
