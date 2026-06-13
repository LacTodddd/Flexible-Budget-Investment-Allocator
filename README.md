# Flexible Budget & Investment Allocator

(English / [ภาษาไทย](#ภาษาไทย))

## English

A command-line personal finance tool that helps users track income, manage expenses, build emergency funds, and allocate investments.

### Features
- **Income & Expense Tracking:** Track monthly income along with essential and lifestyle expenses.
- **Emergency Fund Management:** Calculate your emergency fund target (based on months of coverage) and allocate monthly contributions from your surplus.
- **Investment Allocation:** Automatically split any remaining investable amount across a balanced starter portfolio (Index Funds, Bonds, International Markets, REITs, Individual Stocks, and Crypto).
- **Comprehensive Reporting:** Generate a plain-text budget report summarizing your financial health, savings rate, and progress.
- **Data Export:** Export your financial report to both `.txt` and `.csv` formats in the `reports/` directory.

### Requirements
- Python 3.x
- Standard Python libraries (`csv`, `os`, `datetime`)

### Usage
Run the script using Python from your terminal:
```bash
python3 budget_allocator.py
```
Follow the interactive prompts to input your financial data. The tool will calculate your budget, give you insights on your savings rate, and ask if you'd like to export your report.

---

## ภาษาไทย

เครื่องมือจัดการการเงินส่วนบุคคลผ่านระบบ Command-line ที่จะช่วยคุณติดตามรายรับ จัดการรายจ่าย สร้างเงินสำรองฉุกเฉิน และจัดสรรเงินลงทุนอย่างเป็นระบบ

### ฟีเจอร์หลัก
- **ติดตามรายรับและรายจ่าย:** จัดการรายรับต่อเดือน รวมถึงแยกแยะรายจ่ายที่จำเป็น (Essential) และรายจ่ายไลฟ์สไตล์ (Lifestyle)
- **จัดการเงินสำรองฉุกเฉิน:** คำนวณเป้าหมายเงินสำรองฉุกเฉิน (ตามจำนวนเดือนที่ต้องการให้ครอบคลุมรายจ่าย) และจัดสรรเงินเข้ากองทุนจากเงินคงเหลือในแต่ละเดือน
- **จัดสรรการลงทุน:** แบ่งเงินลงทุนที่เหลือโดยอัตโนมัติไปยังพอร์ตการลงทุนที่สมดุล (เช่น Index Funds, Bonds, กองทุนต่างประเทศ, REITs, หุ้นรายตัว, และ Crypto)
- **สรุปรายงานการเงิน:** สร้างรายงานสรุปสุขภาพการเงิน อัตราการออม และความคืบหน้าในการออมเงินของคุณ
- **ส่งออกข้อมูล:** สามารถส่งออกรายงานของคุณในรูปแบบไฟล์ `.txt` และ `.csv` โดยจะถูกบันทึกไว้ในโฟลเดอร์ `reports/`

### ความต้องการของระบบ
- Python 3.x
- ไลบรารีมาตรฐานของ Python (`csv`, `os`, `datetime`)

### วิธีการใช้งาน
รันสคริปต์ด้วย Python ผ่านเทอร์มินัล (Terminal):
```bash
python3 budget_allocator.py
```
จากนั้นทำตามคำแนะนำบนหน้าจอเพื่อป้อนข้อมูลทางการเงินของคุณ ระบบจะทำการคำนวณงบประมาณ สรุปอัตราการออม และมีตัวเลือกให้คุณส่งออกรายงานเมื่อทำรายการเสร็จสิ้น
