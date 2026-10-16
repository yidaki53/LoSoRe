{ liero::FUN_1ec2_1619 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_1619.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_1619.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_1619(byte param_1,byte param_2)
// 
// {
//   byte bVar1;
//   byte bVar2;
//   undefined1 extraout_AH;
//   undefined1 uVar3;
//   undefined1 extraout_AH_00;
//   undefined2 unaff_SS;
//   undefined1 local_9;
//   undefined1 local_8;
//   undefined1 local_7;
//   undefined1 local_6;
//   undefined1 local_5;
//   undefined1 local_4;
//   byte local_3;
//   
//   FUN_1ec2_152f(&local_6,unaff_SS,&local_5,unaff_SS,&local_4,unaff_SS,&param_1,unaff_SS);
//   bVar1 = param_2;
//   param_1 = param_1 - 1;
//   uVar3 = extraout_AH;
//   bVar2 = param_1;
//   if (param_2 <= param_1) {
//     while( true ) {
//       local_3 = bVar2;
//       FUN_1ec2_152f(&local_9,unaff_SS,&local_8,unaff_SS,&local_7,unaff_SS,&local_3,unaff_SS);
//       uVar3 = (undefined1)(local_3 + 1 >> 8);
//       FUN_2971_65df(0x1ec2,CONCAT11(uVar3,local_9),CONCAT11(uVar3,local_8),CONCAT11(uVar3,local_7),
//                     local_3 + 1);
//       uVar3 = extraout_AH_00;
//       if (local_3 == bVar1) break;
//       bVar2 = local_3 - 1;
//     }
//   }
//   FUN_2971_65df(0x1ec2,CONCAT11(uVar3,local_6),CONCAT11(uVar3,local_5),CONCAT11(uVar3,local_4),
//                 CONCAT11(uVar3,param_2));
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_1619;
begin
  { TODO: translate from asm/FUN_1ec2_1619.s — UNMATCHED until an oracle passes }
end;

