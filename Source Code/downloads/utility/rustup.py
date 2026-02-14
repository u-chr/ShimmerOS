from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://win.rustup.rs/x86_64",(Path.home() / "Downloads" / "rustup-init.exe"))