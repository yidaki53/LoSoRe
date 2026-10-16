{ liero::FUN_1000_df98 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_df98.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_df98.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_df98(void)
// 
// {
//   int *piVar1;
//   undefined2 uVar2;
//   undefined1 extraout_AH;
//   undefined2 uVar3;
//   undefined1 extraout_AH_00;
//   uint uVar4;
//   undefined2 uVar5;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 uVar6;
//   undefined1 uVar7;
//   undefined1 *puVar8;
//   undefined1 *puVar9;
//   undefined1 local_50a [256];
//   undefined1 local_40a [2];
//   undefined1 local_408 [254];
//   uint local_30a;
//   undefined1 local_308 [256];
//   undefined1 local_208 [256];
//   int local_108;
//   byte local_106 [256];
//   uint local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0xdfa3;
//   FUN_24dd_0530();
//   local_108 = FUN_24dd_3d2f();
//   uVar6 = local_108 == 1;
//   if (local_108 < 1) {
//     return;
//   }
//   local_4 = 1;
//   do {
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ce0(local_4);
//     FUN_24dd_3eaf(0xff,local_106,unaff_SS,puVar9,uVar2);
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf56,0x24dd,puVar9,uVar2);
//     if ((bool)uVar6) {
// LAB_1000_e022:
//       puVar9 = local_408;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(local_106[0] - 2,3,local_106,unaff_SS);
//       uVar5 = 0x202c;
//       uVar2 = FUN_202c_0706(puVar9,uVar2);
//       *(undefined2 *)0x66aa = uVar2;
//       if (0xc < *(int *)0x66aa % 0x19) {
//         *(int *)0x66aa = *(int *)0x66aa + 0x19;
//       }
//       piVar1 = (int *)0x66aa;
//       *piVar1 = *piVar1 - *(int *)0x66aa % 0x19;
//       uVar7 = *piVar1 == 0;
//     }
//     else {
//       puVar9 = local_308;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//       uVar5 = 0x24dd;
//       FUN_24dd_3f86(0xdf59,0x24dd,puVar9,uVar2);
//       uVar7 = false;
//       if ((bool)uVar6) goto LAB_1000_e022;
//     }
//     FUN_24dd_3f86(0xdf5c,uVar5,local_106,unaff_SS);
//     if ((bool)uVar7) {
//       *(undefined1 *)0x66a5 = 0;
//     }
//     FUN_24dd_3f86(0xdf5e,0x24dd,local_106,unaff_SS);
//     if (((bool)uVar7) || (FUN_24dd_3f86(0xdf62,0x24dd,local_106,unaff_SS), (bool)uVar7)) {
//       *(undefined1 *)0x66a7 = 1;
//     }
//     FUN_24dd_3f86(0xdf66,0x24dd,local_106,unaff_SS);
//     if (((bool)uVar7) || (FUN_24dd_3f86(0xdf6a,0x24dd,local_106,unaff_SS), (bool)uVar7)) {
//       *(undefined1 *)0x66a8 = 1;
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf6e,0x24dd,puVar9,uVar2);
//     uVar6 = 0;
//     if ((bool)uVar7) {
//       puVar9 = local_308;
//       uVar6 = local_106[0] - 2 == 0;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(local_106[0] - 2,3,local_106,unaff_SS);
//       FUN_24dd_3eaf(0x14,0x66ec,unaff_DS,puVar9,uVar2);
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf71,0x24dd,puVar9,uVar2);
//     uVar7 = 0;
//     if ((bool)uVar6) {
//       puVar9 = local_308;
//       uVar7 = local_106[0] - 2 == 0;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(local_106[0] - 2,3,local_106,unaff_SS);
//       FUN_24dd_3eaf(0x14,0x6701,unaff_DS,puVar9,uVar2);
//     }
//     FUN_24dd_3f86(0xdf74,0x24dd,local_106,unaff_SS);
//     if (((bool)uVar7) || (FUN_24dd_3f86(0xdf77,0x24dd,local_106,unaff_SS), (bool)uVar7)) {
//       *(undefined1 *)0x66a6 = 0;
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf7a,0x24dd,puVar9,uVar2);
//     if ((bool)uVar7) {
// LAB_1000_e1ce:
//       *(undefined1 *)0x672e = 0;
//       local_30a = (uint)local_106[0];
//       uVar6 = local_30a == 3;
//       if (2 < local_30a) {
//         local_6 = 3;
//         while( true ) {
//           puVar9 = local_50a;
//           uVar5 = unaff_SS;
//           FUN_24dd_3e95(0x672e,unaff_DS);
//           puVar8 = local_40a;
//           uVar2 = unaff_SS;
//           uVar3 = FUN_24dd_4919(CONCAT11(extraout_AH,local_106[local_6]));
//           FUN_24dd_3fb1(uVar3);
//           FUN_24dd_3f14(puVar8,uVar2);
//           FUN_24dd_3eaf(8,0x672e,unaff_DS,puVar9,uVar5);
//           uVar6 = true;
//           if (local_6 == local_30a) break;
//           local_6 = local_6 + 1;
//         }
//       }
//       *(undefined1 *)0x66a9 = 0;
//     }
//     else {
//       puVar9 = local_308;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//       FUN_24dd_3f86(0xdf7d,0x24dd,puVar9,uVar2);
//       uVar6 = false;
//       if ((bool)uVar7) goto LAB_1000_e1ce;
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf80,0x24dd,puVar9,uVar2);
//     if ((bool)uVar6) {
// LAB_1000_e278:
//       *(undefined1 *)0x6664 = 0;
//       local_30a = (uint)local_106[0];
//       uVar7 = local_30a == 3;
//       if (2 < local_30a) {
//         local_6 = 3;
//         while( true ) {
//           puVar9 = local_50a;
//           uVar5 = unaff_SS;
//           FUN_24dd_3e95(0x6664,unaff_DS);
//           puVar8 = local_40a;
//           uVar2 = unaff_SS;
//           uVar3 = FUN_24dd_4919(CONCAT11(extraout_AH_00,local_106[local_6]));
//           FUN_24dd_3fb1(uVar3);
//           FUN_24dd_3f14(puVar8,uVar2);
//           FUN_24dd_3eaf(8,0x6664,unaff_DS,puVar9,uVar5);
//           uVar7 = true;
//           if (local_6 == local_30a) break;
//           local_6 = local_6 + 1;
//         }
//       }
//     }
//     else {
//       puVar9 = local_308;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//       FUN_24dd_3f86(0xdf83,0x24dd,puVar9,uVar2);
//       uVar7 = false;
//       if ((bool)uVar6) goto LAB_1000_e278;
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf86,0x24dd,puVar9,uVar2);
//     if ((bool)uVar7) {
// LAB_1000_e31d:
//       puVar9 = local_408;
//       uVar6 = local_106[0] - 2 == 0;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(local_106[0] - 2,3,local_106,unaff_SS);
//       uVar5 = 0x202c;
//       uVar2 = FUN_202c_0706(puVar9,uVar2);
//       *(undefined2 *)0x669d = uVar2;
//     }
//     else {
//       puVar9 = local_308;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//       uVar5 = 0x24dd;
//       FUN_24dd_3f86(0xdf89,0x24dd,puVar9,uVar2);
//       uVar6 = 0;
//       if ((bool)uVar7) goto LAB_1000_e31d;
//     }
//     FUN_24dd_3f86(0xdf8c,uVar5,local_106,unaff_SS);
//     if (((bool)uVar6) || (FUN_24dd_3f86(0xdf8f,0x24dd,local_106,unaff_SS), (bool)uVar6)) {
//       *(undefined1 *)0x4b8 = 0;
//     }
//     puVar9 = local_208;
//     uVar2 = unaff_SS;
//     FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//     FUN_24dd_3f86(0xdf92,0x24dd,puVar9,uVar2);
//     if ((bool)uVar6) {
// LAB_1000_e3ac:
//       puVar9 = local_408;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(local_106[0] - 2,3,local_106,unaff_SS);
//       uVar2 = FUN_202c_0706(puVar9,uVar2);
//       *(undefined2 *)0x2 = uVar2;
//     }
//     else {
//       puVar9 = local_308;
//       uVar2 = unaff_SS;
//       FUN_24dd_3ed3(2,1,local_106,unaff_SS);
//       FUN_24dd_3f86(0xdf95,0x24dd,puVar9,uVar2);
//       if ((bool)uVar6) goto LAB_1000_e3ac;
//     }
//     uVar4 = (int)*(uint *)0x2 >> 0xf;
//     *(int *)0x2 = (int)((*(uint *)0x2 ^ uVar4) - uVar4) % 6;
//     if (local_4 == local_108) {
//       return;
//     }
//     local_4 = local_4 + 1;
//     uVar6 = local_4 == 0;
//   } while( true );
// }
// 
// --- end reference ---
procedure FUN_1000_df98;
begin
  { TODO: translate from asm/FUN_1000_df98.s — UNMATCHED until an oracle passes }
end;

