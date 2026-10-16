
void __cdecl16near FUN_24dd_46b1(void)

{
  int iVar1;
  long lVar2;
  uint uVar3;
  char cVar4;
  int iVar5;
  undefined2 unaff_DS;
  
  iVar1 = *(int *)0x6414;
  lVar2 = (ulong)*(uint *)0x6412 * (ulong)uRam000246e7;
  uVar3 = (uint)lVar2;
  iVar5 = *(uint *)0x6412 << 3;
  cVar4 = (char)iVar5;
  iVar5 = (int)((ulong)lVar2 >> 0x10) + CONCAT11((char)((uint)iVar5 >> 8) + cVar4,cVar4) + iVar1 * 5
  ;
  *(int *)0x6412 = uVar3 + 1;
  *(int *)0x6414 =
       CONCAT11((char)((uint)iVar5 >> 8) + (char)iVar1 * '\x04' + (char)(iVar1 << 7),(char)iVar5) +
       (uint)(0xfffe < uVar3);
  return;
}

