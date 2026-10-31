
void __stdcall16far FUN_42b5_1ade(int param_1,undefined1 *param_2,byte param_3)

{
  char *pcVar1;
  code *pcVar2;
  char cVar3;
  int iVar4;
  char *pcVar5;
  undefined2 unaff_SS;
  bool bVar6;
  char local_82 [128];
  
  if (param_3 == 0) {
    pcVar2 = (code *)swi(0x21);
    cVar3 = (*pcVar2)();
    param_3 = cVar3 + 1;
  }
  bVar6 = 0xbf < param_3;
  local_82[0] = param_3 + 0x40;
  local_82[1] = ':';
  local_82[2] = '\\';
  pcVar2 = (code *)swi(0x21);
  (*pcVar2)();
  if (bVar6) {
    local_82[3] = 0;
  }
  pcVar5 = local_82;
  iVar4 = 0;
  do {
    pcVar1 = pcVar5;
    pcVar5 = pcVar5 + 1;
    if (*pcVar1 == '\0') break;
    iVar4 = iVar4 + 1;
    ((undefined1 *)param_2)[iVar4] = *pcVar1;
    param_1 = param_1 + -1;
  } while (param_1 != 0);
  *param_2 = (char)iVar4;
  return;
}

