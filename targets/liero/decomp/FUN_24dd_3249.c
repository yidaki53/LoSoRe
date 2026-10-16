
/* WARNING: Instruction at (ram,0x00028030) overlaps instruction at (ram,0x0002802f)
    */
/* WARNING: Control flow encountered bad instruction data */

uint __cdecl16far FUN_24dd_3249(void)

{
  code *pcVar1;
  char cVar2;
  undefined1 *puVar3;
  uint uVar4;
  byte bVar5;
  undefined2 in_CX;
  int iVar6;
  uint *in_BX;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 in_CF;
  bool bVar7;
  byte in_AF;
  ulong uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined1 in_stack_00000000;
  undefined4 in_stack_00000001;
  undefined2 uStack_3;
  undefined1 uStack_1;
  
  pcVar1 = (code *)swi(0x35);
  uVar8 = (*pcVar1)();
  puVar3 = &stack0x0005;
code_r0x0002801d:
  iVar6 = (int)(uVar8 >> 0x10);
  if ((POPCOUNT((uint)puVar3 & 0xff) & 1U) == 0) {
    *in_BX = *in_BX >> 0xd;
    in_AF = 9 < ((byte)uVar8 & 0xf) | in_AF;
    in_stack_00000001 = CONCAT22(unaff_DS,(int)in_stack_00000001);
    uVar4 = (CONCAT11((char)(uVar8 >> 8) + in_AF,(byte)uVar8 + in_AF * '\x06') & 0xff0f) + 1;
    bVar7 = (POPCOUNT(uVar4 & 0xff) & 1U) == 0;
    while( true ) {
      if (!bVar7) {
        uVar8 = CONCAT22(iVar6,(uint)(byte)((byte)uVar4 % 0));
        goto code_r0x00027ff2;
      }
      if (POPCOUNT((uint)&stack0x0004 & 0xff) != '\0') break;
      if ((POPCOUNT(uVar4 + 1 & 0xff) & 1U) != 0) {
        pcVar1 = (code *)swi(0x3c);
        (*pcVar1)();
        pcVar1 = (code *)swi(0x3d);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      if ((POPCOUNT(iVar6 + 1U & 0xff) & 1U) != 0) {
        return uVar4 + 1;
      }
      pcVar1 = (code *)swi(0x37);
      uVar9 = (*pcVar1)();
      uVar4 = (int)uVar9 + 1;
      uVar10 = CONCAT22((int)((ulong)uVar9 >> 0x10),uVar4);
      if ((POPCOUNT(uVar4 & 0xff) & 1U) != 0) {
                    /* WARNING: Bad instruction - Truncating control flow here */
        halt_baddata();
      }
      if ((POPCOUNT((int)uVar9 + 0xbf60U & 0xff) & 1U) != 0) {
        pcVar1 = (code *)swi(0x35);
        uVar10 = (*pcVar1)();
        out((int)((ulong)uVar10 >> 0x10),(char)uVar10);
        return (uint)uVar10;
      }
      in_stack_00000001 = CONCAT22(unaff_SS,(int)CONCAT21(unaff_SS,(char)in_stack_00000001));
      while( true ) {
        uVar4 = (int)((ulong)uVar10 >> 0x10) + 1;
        if ((POPCOUNT(uVar4 & 0xff) & 1U) != 0) {
          out(uVar4,(char)uVar10);
          goto LAB_24dd_3243;
        }
        pcVar1 = (code *)swi(0x35);
        uVar8 = (*pcVar1)();
        iVar6 = (int)(uVar8 >> 0x10);
        if ((POPCOUNT((uint)&stack0x0005 & 0xff) & 1U) != 0) {
          in_CF = 0;
          puVar3 = (undefined1 *)((uint)uVar8 ^ 0x443e);
          uVar8 = uVar8 ^ 0x443e;
          goto code_r0x0002801d;
        }
        *in_BX = *in_BX >> 0xd;
        uVar4 = (uint)uVar8 ^ 0xcdfc;
        bVar7 = (POPCOUNT((uint)&stack0x0003 & 0xff) & 1U) == 0;
        if (!bVar7) break;
        pcVar1 = (code *)swi(0x35);
        (*pcVar1)();
        if (POPCOUNT((uint)&stack0x0008 & 0xff) != '\0') {
          return *(uint *)0x7b40;
        }
        *in_BX = *in_BX >> 0xd;
        pcVar1 = (code *)swi(0x3d);
        (*pcVar1)();
        pcVar1 = (code *)swi(0x35);
        uVar10 = (*pcVar1)();
        if ((POPCOUNT((uint)&stack0x0003 & 0xff) & 1U) == 0) {
          pcVar1 = (code *)swi(0x35);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
      }
    }
    pcVar1 = (code *)swi(0x3c);
    (*pcVar1)();
    pcVar1 = (code *)swi(0x3d);
    (*pcVar1)();
    in_BX = (uint *)CONCAT11(in_stack_00000000,uStack_1);
    uVar4 = (uint)((ulong)in_stack_00000001 >> 0x10) & 0x7fff;
    in_CF = uVar4 < 0x3f7e;
    puVar3 = (undefined1 *)(uVar4 + 0xc082);
    uVar8 = CONCAT22((int)in_stack_00000001,puVar3);
    in_CX = uStack_3;
  }
  if ((bool)in_CF || puVar3 == (undefined1 *)0x0) {
    return 0;
  }
  if ((char)(uVar8 >> 8) == '\0') {
code_r0x00027ff2:
    cVar2 = (char)uVar8;
    bVar5 = (byte)((uint)in_CX >> 8);
    bVar7 = (char)in_CX < '\0';
    if ((!CARRY2((uint)(uVar8 >> 0x10),(uint)CARRY2((uint)in_BX,(uint)CARRY1(bVar5,bVar7)))) ||
       (cVar2 = cVar2 + '\x01', cVar2 != '\0')) {
      return CONCAT11(bVar5 + bVar7,cVar2);
    }
  }
LAB_24dd_3243:
  uVar4 = FUN_24dd_010f();
  return uVar4;
}

