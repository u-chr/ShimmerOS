from pathlib import Path
from os import getcwd
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/loplxl/Dynamic-Timer-Resolution/releases/latest/download/dynamic-timer-resolution.exe",(getcwd()[:2] + r"\Shimmer\Software\quickaccess\dynamic-timer-resolution.exe"))