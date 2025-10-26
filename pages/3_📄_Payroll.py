# pages/3_📄_Payroll.py
import streamlit as st
import base64
from datetime import datetime
from common import get_text, show_security_warnings, show_announcement, main_layout

# 페이지 제목 설정
st.set_page_config(
    page_title="給与 - Otsuka Bank",
    page_icon="📄",
    layout="wide"
)

# 급여 계산 함수들
def calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction):
    total_income = basic_salary + overtime_pay
    total_deductions = income_tax + residence_tax + health_insurance + pension + employment_insurance + other_deduction
    net_salary = total_income - total_deductions
    
    return {
        'total_income': total_income,
        'total_deductions': total_deductions,
        'net_salary': net_salary,
        'income_breakdown': {
            'basic_salary': {'jp': '基本給', 'en': 'Basic Salary', 'amount': basic_salary},
            'overtime_pay': {'jp': '残業代', 'en': 'Overtime Pay', 'amount': overtime_pay}
        },
        'deduction_breakdown': {
            'income_tax': {'jp': '所得税', 'en': 'Income Tax', 'amount': income_tax},
            'residence_tax': {'jp': '住民税', 'en': 'Residence Tax', 'amount': residence_tax},
            'health_insurance': {'jp': '健康保険', 'en': 'Health Insurance', 'amount': health_insurance},
            'pension': {'jp': '厚生年金', 'en': 'Pension', 'amount': pension},
            'employment_insurance': {'jp': '雇用保険', 'en': 'Employment Insurance', 'amount': employment_insurance},
            'other_deduction': {'jp': '控除額', 'en': 'Other Deduction', 'amount': other_deduction}
        }
    }

def create_payslip_html(salary_data, payslip_date, user_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>給与明細 - {payslip_date}</title>
        <style>
            body {{ font-family: 'Hiragino Sans', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .payslip-container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 20px rgba(0,0,0,0.1); border-radius: 8px; }}
            .header {{ text-align: center; border-bottom: 3px solid #2c5282; padding-bottom: 20px; margin-bottom: 30px; }}
            .company-name {{ font-size: 24px; font-weight: bold; color: #2c5282; margin-bottom: 10px; }}
            .info-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
            .amount-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
            .income-box {{ background: #f0fff4; padding: 20px; border-radius: 8px; border: 2px solid #38a169; }}
            .deduction-box {{ background: #fff5f5; padding: 20px; border-radius: 8px; border: 2px solid #e53e3e; }}
            .total-section {{ background: #2c5282; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 20px; }}
            .detail-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; }}
        </style>
    </head>
    <body>
        <div class="payslip-container">
            <div class="header">
                <div class="company-name">大塚銀行 / Otsuka Bank</div>
                <div style="font-size: 20px; color: #333; margin-bottom: 20px;">給与明細書 / Payslip</div>
                <div>支給日 / Pay Date: {payslip_date}</div>
            </div>
            
            <div class="info-section">
                <div style="background: #f8f9fa; padding: 15px; border-radius: 6px;">
                    <strong>氏名 / Name</strong><br>{user_data['name']}<br>
                    <strong>社員番号 / Employee Number</strong><br>{user_data['emp_num']}
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 6px;">
                    <strong>所属部署 / Department</strong><br>{user_data['department']}<br>
                    <strong>口座番号 / Account Number</strong><br>{user_data['account']}
                </div>
            </div>
            
            <div class="amount-section">
                <div class="income-box">
                    <h3 style="color: #38a169;">支給内訳 / Income Breakdown</h3>
                    <div class="detail-row">
                        <span>基本給 / Basic Salary</span>
                        <span>¥{salary_data['income_breakdown']['basic_salary']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>残業代 / Overtime Pay</span>
                        <span>¥{salary_data['income_breakdown']['overtime_pay']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 2px solid #38a169; padding-top: 10px;">
                        <div class="detail-row">
                            <strong>総支給額 / Total Income</strong>
                            <strong>¥{salary_data['total_income']:,.0f}</strong>
                        </div>
                    </div>
                </div>
                
                <div class="deduction-box">
                    <h3 style="color: #e53e3e;">控除内訳 / Deduction Breakdown</h3>
                    <div class="detail-row">
                        <span>所得税 / Income Tax</span>
                        <span>¥{salary_data['deduction_breakdown']['income_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>住民税 / Residence Tax</span>
                        <span>¥{salary_data['deduction_breakdown']['residence_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>健康保険 / Health Insurance</span>
                        <span>¥{salary_data['deduction_breakdown']['health_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>厚生年金 / Pension</span>
                        <span>¥{salary_data['deduction_breakdown']['pension']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>雇用保険 / Employment Insurance</span>
                        <span>¥{salary_data['deduction_breakdown']['employment_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>控除額 / Other Deduction</span>
                        <span>¥{salary_data['deduction_breakdown']['other_deduction']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 2px solid #e53e3e; padding-top: 10px;">
                        <div class="detail-row">
                            <strong>総控除額 / Total Deductions</strong>
                            <strong>¥{salary_data['total_deductions']:,.0f}</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="total-section">
                <div>差引支給額 / Net Salary</div>
                <div style="font-size: 28px; font-weight: bold; margin: 10px 0;">¥{salary_data['net_salary']:,.0f}</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def main():
    main_layout()
    show_security_warnings()
    show_announcement()
    
    st.markdown(f"## 📄 {get_text('payroll_management')}")
    
    with st.form("payroll_form"):
        st.subheader("給与情報 / Payroll Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {get_text('income_breakdown')}")
            basic_salary = st.number_input(get_text('basic_salary'), value=300000, step=10000)
            overtime_pay = st.number_input(get_text('overtime_pay'), value=50000, step=5000)
        
        with col2:
            st.markdown(f"#### {get_text('deduction_breakdown')}")
            income_tax = st.number_input(get_text('income_tax'), value=25000, step=1000)
            residence_tax = st.number_input(get_text('residence_tax'), value=15000, step=1000)
            health_insurance = st.number_input(get_text('health_insurance'), value=20000, step=1000)
            pension = st.number_input(get_text('pension'), value=30000, step=1000)
            employment_insurance = st.number_input(get_text('employment_insurance'), value=5000, step=1000)
            other_deduction = st.number_input(get_text('other_deduction'), value=10000, step=1000)
            payslip_date = st.date_input(get_text('pay_date'), datetime.now().date())
        
        submitted = st.form_submit_button(f"📄 {get_text('payslip_creation')}", use_container_width=True, type="primary")
        
        if submitted:
            salary_data = calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction)
            
            new_payslip = {
                'id': len(st.session_state.payroll_list) + 1,
                'date': payslip_date.strftime('%Y/%m/%d'),
                'salary_data': salary_data,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.payroll_list.append(new_payslip)
            
            st.success("🎉 給与明細が作成されました！ / Payslip created successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('total_income'), f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric(get_text('total_deductions'), f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric(get_text('net_salary'), f"¥{salary_data['net_salary']:,.0f}")
            
            # HTML 다운로드
            html_content = create_payslip_html(salary_data, payslip_date.strftime('%Y年%m月%d日 / %Y/%m/%d'), st.session_state.user_data)
            b64 = base64.b64encode(html_content.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="給与明細_{payslip_date.strftime("%Y%m%d")}.html">'
            st.markdown(
                f'{href}'
                f'<button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin-top: 1rem; width: 100%;">'
                f'📥 {get_text("download_payslip")}'
                f'</button>'
                f'</a>',
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()