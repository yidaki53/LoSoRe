{ liero::FUN_1000_b3fe — partial assembly-reviewed Pascal reconstruction
  (oracle: raw assembly review; host tests not run; keyboard ISR not modeled).
  Source: asm/FUN_1000_b3fe.s; Ghidra reference is embedded below.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 FUN_1000_b3fe(void)
// 
// {
//   undefined1 uVar1;
//   int iVar2;
//   char extraout_AL;
//   undefined1 extraout_AH;
//   undefined2 unaff_DS;
//   undefined4 uStack_6;
//   
//   FUN_24dd_0530();
//   uStack_6 = 0x10000109;
//   while (*(undefined1 *)(uStack_6._1_2_ + 0x783b) = 0, uStack_6._1_2_ != 0xab) {
//     uStack_6 = (ulong)CONCAT12(uStack_6._3_1_,uStack_6._1_2_ + 1) << 8;
//   }
//   do {
//     FUN_24ba_00d8();
//   } while (extraout_AL == '\0');
//   uStack_6 = CONCAT13(uStack_6._3_1_,0x100);
//   while( true ) {
//     iVar2 = uStack_6._1_2_;
//     if (*(char *)(uStack_6._1_2_ + 0x783b) != '\0') {
//       uVar1 = uStack_6._1_1_;
//       uStack_6 = CONCAT13(uVar1,(undefined3)uStack_6);
//       *(undefined1 *)(iVar2 + 0x783b) = 0;
//     }
//     if (uStack_6._1_2_ == 0xab) break;
//     uStack_6 = (ulong)CONCAT12(uStack_6._3_1_,uStack_6._1_2_ + 1) << 8;
//   }
//   return CONCAT11(extraout_AH,uStack_6._3_1_);
// }
// 
// --- end reference ---
function FUN_1000_b3fe: Word;
var
  keyIndex: Word;
  pending: Boolean;
  resultAssigned: Boolean;
  resultValue: Byte;
begin
  { TODO: the original input interrupt which populates this queue is outside
    the host model; this routine blocks until that external state arrives. }
  keyIndex := 1;
  repeat
    DosMemory[Word($783B + keyIndex)] := 0;
    if keyIndex = $00AB then
      Break;
    keyIndex := Word(keyIndex + 1);
  until False;

  { The called polling helper scans these interrupt-populated flags from AB
    down to 1 and returns one as soon as any key flag is set. }
  repeat
    pending := False;
    keyIndex := $00AB;
    while keyIndex <> 0 do
    begin
      if DosMemory[Word($783B + keyIndex)] <> 0 then
      begin
        pending := True;
        Break;
      end;
      keyIndex := Word(keyIndex - 1);
    end;
  until pending;
  RegisterAX := (RegisterAX and $FF00) or 1;

  resultAssigned := False;
  keyIndex := 1;
  repeat
    if DosMemory[Word($783B + keyIndex)] <> 0 then
    begin
      resultValue := Byte(keyIndex);
      resultAssigned := True;
      DosMemory[Word($783B + keyIndex)] := 0;
    end;
    if keyIndex = $00AB then
      Break;
    keyIndex := Word(keyIndex + 1);
  until False;

  if resultAssigned then
  begin
    RegisterAX := (RegisterAX and $FF00) or resultValue;
    FUN_1000_b3fe := RegisterAX;
  end
  else
    { A concurrent interrupt could clear the flag after the polling call and
      before the sweep; in that race the assembly returns an uninitialized
      local byte. Do not synthesize a default result. }
    Exit;
end;
