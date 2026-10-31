{ liero-dos::FUN_24dd_028a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_028a.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_028a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_24dd_0353(void);
// void FUN_24dd_010f(void);
// 
// void __stdcall16far FUN_24dd_028a(void) {
//     uint8_t cf;
// 
//     FUN_24dd_0353();
//     __asm__ volatile ("pushf; pop %%ax; setc %%al" : "=a" (cf));
//     if (cf == 0) {
//         return;
//     }
//     FUN_24dd_010f();
//     return;
// }
// --- end reference ---
procedure FUN_24dd_028a;
var
  cf: Byte;
begin
  FUN_24dd_0353;
  asm
    pushf;
    pop ax;
    setc al;
  end;
  if cf = 0 then
    Exit;
  FUN_24dd_010f;
end;
