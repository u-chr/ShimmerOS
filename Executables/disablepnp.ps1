$devices = @(
    "High precision event timer",
    "Intel(R) Platform Monitoring Technology Device",
    "Microsoft GS Wavetable Synth",
    "Microsoft Hyper-V Virtualization Infrastructure Driver",
    "Microsoft Hypervisor Service",
    "Microsoft Kernel Debug Network Adapter",
    "NDIS Virtual Network Adapter Enumerator",
    "Remote Desktop Device Redirector Bus",
    "Root Print Queue",
    "System speaker",
    "UMBus Root Bus Enumerator",
	"Composite Bus Enumerator"
)
Get-PnpDevice -FriendlyName $devices -ErrorAction Ignore | Disable-PnpDevice -Confirm:$false -ErrorAction Ignore