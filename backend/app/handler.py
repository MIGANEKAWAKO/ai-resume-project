import asyncio
from mangum import Mangum
from app.main import app
from app.core.database import init_db

# 在冷启动时初始化数据库（替代 FastAPI lifespan 事件）
loop = asyncio.new_event_loop()
loop.run_until_complete(init_db())
loop.close()

# mangum 将 FastAPI/ASGI 适配为 FC 标准 Python 运行时的 handler
handler = Mangum(app, lifespan="off")
