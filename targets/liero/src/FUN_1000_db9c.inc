{ liero::FUN_1000_db9c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_db9c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_db9c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_db9c(void)
// 
// {
//   char cVar1;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar2;
//   undefined2 uVar3;
//   undefined1 local_294 [9];
//   undefined1 local_28b [256];
//   int local_18b;
//   int local_189;
//   int local_187;
//   undefined1 local_183 [80];
//   undefined1 local_133 [49];
//   undefined1 local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x1000;
//   uStack_6 = 0xdba7;
//   FUN_24dd_0530();
//   FUN_24dd_46e9();
//   FUN_24dd_3d68(0x9b,0x669c,unaff_DS,0x1500,unaff_DS);
//   cVar1 = FUN_202c_0843(0xdb82,0x24dd);
//   if (cVar1 == '\0') {
//     FUN_24dd_3eaf(8,0x6664,unaff_DS,0xdb8c,0x202c);
//   }
//   else {
//     FUN_24dd_3639(0xdb82,0x202c,local_28b,unaff_SS);
//     FUN_24dd_36b7(0x24dd,local_28b);
//     FUN_24dd_04f4();
//     puVar2 = local_28b;
//     uVar3 = unaff_SS;
//     FUN_24dd_3988(8,local_294,unaff_SS);
//     FUN_24dd_38f0(puVar2,uVar3);
//     FUN_24dd_04f4();
//     FUN_24dd_3711(local_28b,unaff_SS);
//     FUN_24dd_04f4();
//     if (*(char *)0x6664 == '\0') {
//       FUN_24dd_3eaf(8,0x6664,unaff_DS,0xdb8c,0x24dd);
//     }
//   }
//   FUN_202c_08b2(0x6664,unaff_DS);
//   FUN_24dd_3eaf(0xc,0x65f2,unaff_DS,0x672e,unaff_DS);
//   if (*(char *)0x66ec == '\0') {
//     FUN_1000_a816(0);
//   }
//   if (*(char *)0x6701 == '\0') {
//     FUN_1000_a816(1);
//   }
//   FUN_202c_079e(0x6c00,10,(int)*(undefined4 *)0x6678,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
//                 0xdb92,0x24dd);
//   FUN_202c_079e(0x18e2,0x6e0e,(int)*(undefined4 *)0x667c,(int)((ulong)*(undefined4 *)0x667c >> 0x10)
//                 ,0xdb92,0x202c);
//   FUN_202c_079e(0x1c0,0x86f4,(int)*(undefined4 *)0x6680,(int)((ulong)*(undefined4 *)0x6680 >> 0x10),
//                 0xdb92,0x202c);
//   local_187 = 0;
//   while( true ) {
//     local_189 = 0;
//     while( true ) {
//       for (local_18b = 0;
//           local_102[local_18b * 0x10 + local_189] =
//                *(undefined1 *)
//                 ((int)*(undefined4 *)0x6678 + local_187 * 0x100 + local_189 * 0x10 + local_18b),
//           local_18b != 0xf; local_18b = local_18b + 1) {
//       }
//       if (local_189 == 0xf) break;
//       local_189 = local_189 + 1;
//     }
//     FUN_24dd_3d68(0x100,(int)*(undefined4 *)0x6678 + local_187 * 0x100,
//                   (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_102,unaff_SS);
//     if (local_187 == 0x6b) break;
//     local_187 = local_187 + 1;
//   }
//   local_187 = 0;
//   while( true ) {
//     local_189 = 0;
//     while( true ) {
//       for (local_18b = 0;
//           local_133[local_18b * 7 + local_189] =
//                *(undefined1 *)
//                 ((int)*(undefined4 *)0x667c + local_187 * 0x31 + local_189 * 7 + local_18b),
//           local_18b != 6; local_18b = local_18b + 1) {
//       }
//       if (local_189 == 6) break;
//       local_189 = local_189 + 1;
//     }
//     FUN_24dd_3d68(0x31,(int)*(undefined4 *)0x667c + local_187 * 0x31,
//                   (int)((ulong)*(undefined4 *)0x667c >> 0x10),local_133,unaff_SS);
//     if (local_187 == 0x81) break;
//     local_187 = local_187 + 1;
//   }
//   local_187 = 0;
//   while( true ) {
//     local_189 = 0;
//     while( true ) {
//       for (local_18b = 0;
//           local_183[local_18b * 4 + local_189] =
//                *(undefined1 *)
//                 ((int)*(undefined4 *)0x6680 + local_187 * 0x10 + local_189 * 4 + local_18b),
//           local_18b != 3; local_18b = local_18b + 1) {
//       }
//       if (local_189 == 3) break;
//       local_189 = local_189 + 1;
//     }
//     FUN_24dd_3d68(0x10,(int)*(undefined4 *)0x6680 + local_187 * 0x10,
//                   (int)((ulong)*(undefined4 *)0x6680 >> 0x10),local_183,unaff_SS);
//     if (local_187 == 0x1b) break;
//     local_187 = local_187 + 1;
//   }
//   local_189 = 0;
//   while( true ) {
//     local_18b = 0;
//     while( true ) {
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x4900) = cVar1 + -0x60;
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x4a00) = cVar1 + -0x60;
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x5700) = cVar1 + '\f';
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x5800) = cVar1 + '\f';
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x5200) = cVar1 + '^';
//       cVar1 = FUN_24dd_4654(4);
//       *(char *)((int)*(undefined4 *)0x6678 + local_189 * 0x10 + local_18b + 0x5300) = cVar1 + '^';
//       if (local_18b == 0xf) break;
//       local_18b = local_18b + 1;
//     }
//     if (local_189 == 0xf) break;
//     local_189 = local_189 + 1;
//   }
//   FUN_24dd_46e9();
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_db9c;
begin
  { TODO: translate from asm/FUN_1000_db9c.s — UNMATCHED until an oracle passes }
end;

