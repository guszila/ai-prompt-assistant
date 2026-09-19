"""
Test fixtures containing representative requirements across Thai, English, mixed,
and various technical domains with specific architectural verification targets.
"""

# 1. Thai CRUD User Management
REQ_THAI_CRUD = "สร้างระบบจัดการผู้ใช้ เพิ่ม ลบ แก้ไข ค้นหา"

# 2. Strict Authentication Only (must NOT infer Authorization)
REQ_AUTHN_ONLY = "อยากได้ระบบ login เข้าสู่ระบบด้วย email และ password"

# 3. Explicit Authorization (roles & permissions)
REQ_AUTHZ_EXPLICIT = "กำหนดสิทธิ์ผู้ใช้งาน roles และ permissions ของ admin กับ user"

# 4. Combined Authentication and Authorization
REQ_AUTH_COMBINED = "ระบบเข้าสู่ระบบ login และกำหนดสิทธิ์ roles permissions"

# 5. Dashboard and Analytics
REQ_DASHBOARD = "สร้างหน้า Dashboard แสดงสถิติและกราฟยอดขาย"

# 6. Generic API (must NOT map to RESTful API)
REQ_GENERIC_API = "อยากได้ API สำหรับดึงข้อมูลสินค้า"

# 7. Explicit REST API
REQ_REST_API = "สร้าง RESTful API และ endpoint สำหรับสั่งซื้อสินค้า"

# 8. Ambiguous Functional Requirement (missing functional channel/trigger)
REQ_AMBIGUOUS_NOTIFICATION = "ทำระบบแจ้งเตือน"

# 9. English Concurrency/Task Requirement
REQ_ENGLISH_TASKS = "Build a background task queue with error retry mechanism"

# 10. Mixed Language Export Requirement
REQ_MIXED_EXPORT = "ระบบ Export รายงานเป็น Excel file พร้อมส่ง email"

# 11. Edge Cases
REQ_EMPTY = ""
REQ_WHITESPACE = "   \n\t   "
