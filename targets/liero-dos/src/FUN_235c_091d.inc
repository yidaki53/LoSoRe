{ liero-dos::FUN_235c_091d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_091d.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_091d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void FUN_235c_091d(uint8_t param_1);
// 
// void FUN_235c_091d(uint8_t param_1) {
//     uint16_t iVar1;
//     uint8_t *ptr1 = (uint8_t *)(param_1 + 0x67fc);
//     uint16_t *ptr2 = (uint16_t *)((uint16_t)param_1 * 10 + 0x6804);
// 
//     *ptr1 = 0;
//     iVar1 = (uint16_t)param_1 * 10;
//     *ptr2 = 0;
//     *(ptr2 + 1) = 0;
//     *(uint8_t *)(iVar1 + 0x6808) = 0;
//     *(uint16_t *)(iVar1 + 0x6809) = 0;
//     *(uint16_t *)(iVar1 + 0x680b) = 0;
//     *(uint8_t *)(iVar1 + 0x680d) = 0;
// }
// --- end reference ---
procedure FUN_235c_091d(param_1: Byte);
var
    iVar1: Word;
    ptr1: ^Byte;
    ptr2: ^Word;
begin
    ptr1 := Pointer(Byte(param_1) + $67fc);
    ptr1^ := 0;
    iVar1 := Word(param_1) * 10;
    ptr2 := Pointer(iVar1 + $6804);
    ptr2^ := 0;
    Inc(ptr2);
    ptr2^ := 0;
    ptr1 := Pointer(iVar1 + $6808);
    ptr1^ := 0;
    ptr2 := Pointer(iVar1 + $6809);
    ptr2^ := 0;
    Inc(ptr2);
    ptr2^ := 0;
    ptr1 := Pointer(iVar1 + $680b);
    ptr1^ := 0;
    ptr1 := Pointer(iVar1 + $680d);
    ptr1^ := 0;
end;
