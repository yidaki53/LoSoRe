
int __stdcall16far FUN_24dd_4654(uint param_1)

{
  long lVar1;
  ulong uVar2;
  
  uVar2 = FUN_24dd_46b1();
  lVar1 = (uVar2 >> 0x10) * (ulong)param_1;
  return (int)((ulong)lVar1 >> 0x10) +
         (uint)CARRY2((uint)lVar1,(uint)((uVar2 & 0xffff) * (ulong)param_1 >> 0x10));
}

