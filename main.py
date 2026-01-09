import sys
from pathlib import Path
import asyncio

# добавляем src в sys.path
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from infrastructure.entrypoints.telegram.bot import main

if __name__ == "__main__":
    asyncio.run(main())
