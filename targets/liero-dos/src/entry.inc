{ liero-dos::entry — game Pascal draft (oracle: none).
  Drafted from asm/entry.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/entry.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Stack frame is not setup normally: Input value of stackpointer is not used */
// /* WARNING: This function may have set the stack pointer */
// 
// char __cdecl16near entry(void)
// 
// {
//   char cVar1;
//   char in_CL;
//   int in_BX;
//   undefined1 *puVar2;
//   undefined2 unaff_BP;
//   int unaff_SI;
//   undefined2 uVar3;
//   undefined2 unaff_DS;
//   undefined4 uVar4;
//   
//   DAT_4000_125e = 0x1000;
//   DAT_4000_125c = 0xe4ac;
//   FUN_24dd_0000();
//   DAT_4000_125e = 0x24dd;
//   puVar2 = (undefined1 *)0xffec;
//   DAT_4000_125c = 0xe4b1;
//   FUN_24dd_0548();
//   *(undefined2 *)(puVar2 + -2) = 0x24dd;
//   *(undefined2 *)(puVar2 + -4) = 0xe4b6;
//   FUN_235c_135f();
//   *(undefined2 *)(puVar2 + -2) = 0x235c;
//   *(undefined2 *)(puVar2 + -4) = 0xe4bb;
//   FUN_1ea2_01f0();
//   *(undefined2 *)(puVar2 + -2) = unaff_BP;
//   *(undefined2 *)(puVar2 + -4) = 0x1ea2;
//   *(undefined2 *)(puVar2 + -6) = 0xe4c6;
//   FUN_24dd_0530();
//   *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x26) = 0xe4ce;
//   FUN_249c_0159();
//   *(undefined1 *)0x65e0 = 0;
//   while( true ) {
//     *(undefined2 *)(puVar2 + -0x24) = 0xb800;
//     *(undefined1 *)((uint)*(byte *)0x65e0 * 2 + 1) = 0x40;
//     if (*(char *)0x65e0 == 'O') break;
//     *(char *)0x65e0 = *(char *)0x65e0 + '\x01';
//   }
//   *(undefined2 *)(puVar2 + -0x24) = 0;
//   *(undefined2 *)(puVar2 + -0x26) = 0;
//   *(undefined2 *)(puVar2 + -0x28) = 0x249c;
//   *(undefined2 *)(puVar2 + -0x2a) = 0xe3f0;
//   *(undefined2 *)(puVar2 + -0x2c) = 0x249c;
//   *(undefined2 *)(puVar2 + -0x2e) = 0xe501;
//   FUN_249c_0037();
//   *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//   *(undefined2 *)(puVar2 + -0x26) = 0x6528;
//   *(undefined2 *)(puVar2 + -0x28) = 0x249c;
//   *(undefined2 *)(puVar2 + -0x2a) = 0xe50b;
//   FUN_24dd_02b9();
//   *(undefined2 *)(puVar2 + -0x24) = 64000;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe513;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6684 = (int)uVar4;
//   *(undefined2 *)0x6686 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0xc940;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe522;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x65d7 = (int)uVar4;
//   *(undefined2 *)0x65d9 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x56a;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe531;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6698 = (int)uVar4;
//   *(undefined2 *)0x669a = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x2ef4;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe540;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6688 = (int)uVar4;
//   *(undefined2 *)0x668a = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x132b;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe54f;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x668c = (int)uVar4;
//   *(undefined2 *)0x668e = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x2ef4;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe55e;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6694 = (int)uVar4;
//   *(undefined2 *)0x6696 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x2e8d;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe56d;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6690 = (int)uVar4;
//   *(undefined2 *)0x6692 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x6c00;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe57c;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6678 = (int)uVar4;
//   *(undefined2 *)0x667a = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x18e2;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe58b;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x667c = (int)uVar4;
//   *(undefined2 *)0x667e = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x1c0;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe59a;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6680 = (int)uVar4;
//   *(undefined2 *)0x6682 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = 0x1fe;
//   *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x28) = 0xe5a9;
//   uVar4 = FUN_24dd_028a();
//   *(undefined2 *)0x6670 = (int)uVar4;
//   *(undefined2 *)0x6672 = (int)((ulong)uVar4 >> 0x10);
//   *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//   *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//   *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x2a) = 0xe5ba;
//   FUN_24dd_3930();
//   *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x26) = 0xe5bf;
//   FUN_24dd_04f4();
//   *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//   *(undefined2 *)(puVar2 + -0x26) = 0x6674;
//   *(undefined2 *)(puVar2 + -0x28) = 0x1f8;
//   *(undefined2 *)(puVar2 + -0x2a) = 0x15e;
//   *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x2e) = 0xe5cf;
//   cVar1 = FUN_1ea2_0000();
//   if (cVar1 == '\0') {
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//     *(undefined2 *)(puVar2 + -0x28) = 0x1ea2;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe44c;
//     *(undefined2 *)(puVar2 + -0x2c) = 0;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x1ea2;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe78a;
//     FUN_24dd_39c3();
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe78f;
//     FUN_24dd_3930();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe794;
//     FUN_24dd_04f4();
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x6528;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe79e;
//     FUN_24dd_02cb();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     uVar3 = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe7a5;
//     FUN_24dd_0116();
//   }
//   else {
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//     *(undefined2 *)(puVar2 + -0x28) = 0x1ea2;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe422;
//     *(undefined2 *)(puVar2 + -0x2c) = 0;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x1ea2;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe5e7;
//     FUN_24dd_39c3();
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe5ec;
//     FUN_24dd_3951();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe5f1;
//     FUN_24dd_04f4();
//     *(undefined2 *)(puVar2 + -0x24) = 0xe5f4;
//     FUN_1000_db9c();
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe438;
//     *(undefined2 *)(puVar2 + -0x2c) = 0;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe605;
//     FUN_24dd_39c3();
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe60a;
//     FUN_24dd_3930();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe60f;
//     FUN_24dd_04f4();
//     *(undefined2 *)(puVar2 + -0x24) = 0xe612;
//     FUN_1000_df98();
//     *(undefined2 *)(puVar2 + -0x24) = 0xe615;
//     FUN_1000_01a1();
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe61f;
//     FUN_24dd_3930();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe624;
//     FUN_24dd_04f4();
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x79f0;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe43b;
//     *(undefined2 *)(puVar2 + -0x2c) = 0;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe635;
//     FUN_24dd_39c3();
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe63a;
//     FUN_24dd_3930();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe63f;
//     FUN_24dd_04f4();
//     *(undefined2 *)(puVar2 + -0x24) = 0x3127;
//     *(undefined1 **)(puVar2 + -0x26) = puVar2 + -0x22;
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1460;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe650;
//     FUN_24dd_40ac();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1480;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2e) = 0xe65a;
//     FUN_24dd_4181();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x14a0;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2e) = 0xe664;
//     FUN_24dd_4181();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x6604;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe670;
//     FUN_24dd_4141();
//     *(undefined2 *)(puVar2 + -0x24) = 0x3127;
//     *(undefined1 **)(puVar2 + -0x26) = puVar2 + -0x22;
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1460;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe681;
//     FUN_24dd_40ac();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1480;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2e) = 0xe68b;
//     FUN_24dd_4181();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x6624;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe697;
//     FUN_24dd_4141();
//     *(undefined2 *)(puVar2 + -0x24) = 0x3127;
//     *(undefined1 **)(puVar2 + -0x26) = puVar2 + -0x22;
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1460;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe6a8;
//     FUN_24dd_40ac();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1480;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2e) = 0xe6b2;
//     FUN_24dd_4181();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x14c0;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2e) = 0xe6bc;
//     FUN_24dd_4181();
//     *(undefined2 *)(puVar2 + -0x28) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x6644;
//     *(undefined2 *)(puVar2 + -0x2c) = 0x20;
//     *(undefined2 *)(puVar2 + -0x2e) = 0x24dd;
//     uVar3 = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x30) = 0xe6c8;
//     FUN_24dd_4141();
//     while( true ) {
//       *(undefined2 *)(puVar2 + -0x24) = uVar3;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe6cd;
//       cVar1 = FUN_249c_0180();
//       if (cVar1 == '\0') break;
//       *(undefined2 *)(puVar2 + -0x24) = 0x249c;
//       uVar3 = 0x249c;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe6d6;
//       FUN_249c_019d();
//     }
//     *(undefined2 *)(puVar2 + -0x24) = 0x249c;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe6dd;
//     FUN_24ba_0090();
//     do {
//       *(undefined2 *)(puVar2 + -0x24) = 0x24ba;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe6e2;
//       cVar1 = FUN_24ba_00d8();
//     } while (cVar1 == '\0');
//     *(undefined2 *)(puVar2 + -0x24) = 0x300;
//     *(undefined2 *)(puVar2 + -0x26) = 0x24ba;
//     *(undefined2 *)(puVar2 + -0x28) = 0xe6f0;
//     uVar4 = FUN_24dd_028a();
//     *(undefined2 *)0x65dc = (int)uVar4;
//     *(undefined2 *)0x65de = (int)((ulong)uVar4 >> 0x10);
//     uVar4 = *(undefined4 *)0x65dc;
//     *(int *)(puVar2 + -0x24) = (int)((ulong)uVar4 >> 0x10);
//     *(int *)(puVar2 + -0x26) = (int)uVar4;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe702;
//     FUN_1ec2_15bb();
//     *(undefined1 *)0x65e0 = 0x20;
//     while( true ) {
//       *(undefined2 *)(puVar2 + -0x24) = 0x1ec2;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe712;
//       FUN_1ec2_13c5();
//       uVar4 = *(undefined4 *)0x65dc;
//       *(int *)(puVar2 + -0x24) = (int)((ulong)uVar4 >> 0x10);
//       *(int *)(puVar2 + -0x26) = (int)uVar4;
//       *(uint *)(puVar2 + -0x28) = (uint)*(byte *)0x65e0;
//       *(undefined2 *)(puVar2 + -0x2a) = 0x1ec2;
//       *(undefined2 *)(puVar2 + -0x2c) = 0xe723;
//       FUN_1ec2_10ea();
//       if (*(char *)0x65e0 == '\0') break;
//       *(char *)0x65e0 = *(char *)0x65e0 + -1;
//     }
//     *(undefined2 *)(puVar2 + -0x24) = *(undefined2 *)0x65de;
//     *(undefined2 *)(puVar2 + -0x26) = *(undefined2 *)0x65dc;
//     *(undefined2 *)(puVar2 + -0x28) = 0x300;
//     *(undefined2 *)(puVar2 + -0x2a) = 0x1ec2;
//     *(undefined2 *)(puVar2 + -0x2c) = 0xe73a;
//     FUN_24dd_029f();
//     *(undefined2 *)(puVar2 + -0x24) = 0x13;
//     *(undefined2 *)(puVar2 + -0x26) = 0x24dd;
//     *(undefined2 *)(puVar2 + -0x28) = 0xe741;
//     FUN_1ec2_13a4();
//     *(undefined2 *)(puVar2 + -0x24) = 0xe744;
//     FUN_1000_d7b5();
//     *(undefined2 *)(puVar2 + -0x24) = 3;
//     *(undefined2 *)(puVar2 + -0x26) = 0x1ec2;
//     *(undefined2 *)(puVar2 + -0x28) = 0xe74b;
//     FUN_1ec2_13a4();
//     *(undefined2 *)(puVar2 + -0x24) = 0x1ec2;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe750;
//     FUN_24ba_00c4();
//     *(undefined2 *)(puVar2 + -0x24) = 0x24ba;
//     *(undefined2 *)(puVar2 + -0x26) = 0xe3f1;
//     *(undefined2 *)(puVar2 + -0x28) = 0x24ba;
//     uVar3 = 0x202c;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe75a;
//     FUN_202c_093b();
//     while( true ) {
//       *(undefined2 *)(puVar2 + -0x24) = uVar3;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe75f;
//       cVar1 = FUN_249c_0180();
//       if (cVar1 == '\0') break;
//       *(undefined2 *)(puVar2 + -0x24) = 0x249c;
//       uVar3 = 0x249c;
//       *(undefined2 *)(puVar2 + -0x26) = 0xe768;
//       FUN_249c_019d();
//     }
//     *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//     *(undefined2 *)(puVar2 + -0x26) = 0x6674;
//     *(undefined2 *)(puVar2 + -0x28) = 0x249c;
//     uVar3 = 0x1ea2;
//     *(undefined2 *)(puVar2 + -0x2a) = 0xe774;
//     FUN_1ea2_0104();
//     *(undefined2 *)(puVar2 + -0x24) = 0xe777;
//     FUN_1000_05a4();
//   }
//   *(undefined2 *)(puVar2 + -0x24) = unaff_DS;
//   *(undefined2 *)(puVar2 + -0x26) = 0x6528;
//   *(undefined2 *)(puVar2 + -0x28) = uVar3;
//   *(undefined2 *)(puVar2 + -0x2a) = 0xe7af;
//   FUN_24dd_02cb();
//   *(undefined2 *)(puVar2 + -0x24) = 0;
//   *(undefined2 *)(puVar2 + -0x26) = 0;
//   *(undefined2 *)(puVar2 + -0x28) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x2a) = 0xe471;
//   *(undefined2 *)(puVar2 + -0x2c) = 0x24dd;
//   *(undefined2 *)(puVar2 + -0x2e) = 0xe7bd;
//   FUN_249c_0037();
//   *(undefined2 *)(puVar2 + -2) = 0x249c;
//   *(undefined2 *)(puVar2 + -4) = 0xe7c5;
//   cVar1 = FUN_24dd_0116();
//   *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar1;
//   *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar1;
//   *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar1;
//   *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar1;
//   *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar1;
//   *(char *)(unaff_SI + -0x712d) = *(char *)(unaff_SI + -0x712d) + in_CL;
//   return cVar1 + in_CL + '\x02';
// }
// 
// --- end reference ---
function entry: Char;
var
  ch: Byte;
  nil_ptr: Pointer;
  { Local model of DOS absolute memory (Mem[]/MemW[]).
    Real mode addresses map to flat indices here. }
  Mem: array[0..65535] of Byte;
  MemW: array[0..65535] of Word;
begin
  nil_ptr := nil;
  { === Phase 1: RTL / segment initialization === }
  FUN_24dd_0000;
  FUN_24dd_0548;
  FUN_249c_0159;
  FUN_1000_db9c;

  { === Phase 2: stack / heap setup === }
  { MOV AX,0x20; CALLF 0x2000:5300 — heap/stack init }
  { SUB SP,0x20 — 32 bytes of local stack space }
  FUN_1000_df98;

  { === Phase 3: video memory fill — display '@' (0x40) at B800:0 === }
  { Counter at 0x65E0: increment from 0 to 'O' (0x4F),
    writing attribute byte 0x40 at B800:(counter*2+1) }
  Mem[$65E0] := 0;
  repeat
    Mem[$65E0] := Mem[$65E0] + 1;
    { B800 segment: flat base = $B8000. Attribute byte at odd offset. }
    MemW[$B8000 + Word(Mem[$65E0]) * 2 + 1] := $40;
  until Mem[$65E0] = $4F;

  { === Phase 4: disk / sound initialization === }
  FUN_249c_0037(nil_ptr, 0, 0);
  FUN_24dd_02b9(nil_ptr);

  { === Phase 5: timer channel configuration === }
  { FUN_24dd_028a is declared as a procedure (no return value) in
    _forward.inc. The original asm stores DX:AX pairs at globals;
    here we zero the globals as placeholders. }
  FUN_24dd_028a;
  MemW[$6684] := 0;
  MemW[$6686] := 0;

  FUN_24dd_028a;
  MemW[$65D7] := 0;
  MemW[$65D9] := 0;

  FUN_24dd_028a;
  MemW[$6698] := 0;
  MemW[$669A] := 0;

  FUN_24dd_028a;
  MemW[$6688] := 0;
  MemW[$668A] := 0;

  FUN_24dd_028a;
  MemW[$668C] := 0;
  MemW[$668E] := 0;

  FUN_24dd_028a;
  MemW[$6694] := 0;
  MemW[$6696] := 0;

  FUN_24dd_028a;
  MemW[$6690] := 0;
  MemW[$6692] := 0;

  FUN_24dd_028a;
  MemW[$6678] := 0;
  MemW[$667A] := 0;

  FUN_24dd_028a;
  MemW[$667C] := 0;
  MemW[$667E] := 0;

  FUN_24dd_028a;
  MemW[$6680] := 0;
  MemW[$6682] := 0;

  FUN_24dd_028a;
  MemW[$6670] := 0;
  MemW[$6672] := 0;

  { === Phase 6: display / keyboard init === }
  FUN_1ea2_0000(0, 0, nil_ptr);
  FUN_24dd_02cb(nil_ptr);

  { === Phase 7: load level/data === }
  FUN_249c_0037(nil_ptr, 0, 0);
  FUN_24dd_0116;
  ch := 0;

  { === Phase 8: main game loop === }
  { Loop calls FUN_249c_0180 each frame; exits when it returns 0. }
  repeat
    if FUN_249c_0180 = 0 then
      break;
  until False;

  { === Phase 9: cleanup and exit === }
  FUN_1000_d7b5;
  FUN_1000_05a4;
  { Program termination — the original never returns from this point. }
end;

