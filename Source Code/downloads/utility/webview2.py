
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/ebea1897-413e-4de3-9cdf-8591f9efed8f/MicrosoftEdgeWebView2RuntimeInstallerX64.exe",(Path.home() / "Downloads" / "MicrosoftEdgeWebView2RuntimeInstallerX64.exe"))
