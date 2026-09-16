powercfg -import "C:\Shimmer\Temp\Shimmer.pow" 67676767-6767-6767-6767-676767676767
powercfg -import "C:\Shimmer\Temp\ShimmerHetero.pow" 69696969-6969-6969-6969-696969696969

Add-Type @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class C {
    [DllImport("kernel32.dll")]
    static extern bool GetLogicalProcessorInformationEx(int r, IntPtr b, ref int l);
    public static bool HasECores() {
        int len = 0;
        GetLogicalProcessorInformationEx(0, IntPtr.Zero, ref len);
        IntPtr ptr = Marshal.AllocHGlobal(len);
        GetLogicalProcessorInformationEx(0, ptr, ref len);
        HashSet<byte> classes = new HashSet<byte>();
        int offset = 0;
        while (offset < len) {
            int size = Marshal.ReadInt32(ptr, offset + 4);
            byte eff = Marshal.ReadByte(ptr, offset + 9);
            classes.Add(eff);
            offset += size;
        }
        Marshal.FreeHGlobal(ptr);
        return classes.Count > 1;
    }
}
"@

if ([C]::HasECores()) {
	Write-Output "Hybrid CPU"
    powercfg -setactive 69696969-6969-6969-6969-696969696969
} else {
	Write-Output "Non-hybrid CPU"
    powercfg -setactive 67676767-6767-6767-6767-676767676767
}