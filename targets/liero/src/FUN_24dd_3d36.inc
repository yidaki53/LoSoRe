{ liero::FUN_24dd_3d36 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host command-line memory tests).
  Original assembly retained in asm/FUN_24dd_3d36.s.
  The Ghidra decompiler reference is embedded below.
}
// --- reference: Ghidra decompiler C ---
// 
// void __cdecl16near FUN_24dd_3d36(void)
// 
// {
//   undefined2 uVar1;
//   byte *pbVar2;
//   byte *pbVar3;
//   uint uVar4;
//   int in_DX;
//   undefined2 unaff_DS;
//   
//   uVar1 = *(undefined2 *)0x640c;
//   uVar4 = (uint)*(byte *)0x80;
//   pbVar2 = (byte *)0x81;
//   do {
//     for (; (pbVar3 = pbVar2, uVar4 != 0 && (*pbVar2 < 0x21)); pbVar2 = pbVar2 + 1) {
//       uVar4 = uVar4 - 1;
//     }
//     for (; (uVar4 != 0 && (0x20 < *pbVar3)); pbVar3 = pbVar3 + 1) {
//       uVar4 = uVar4 - 1;
//     }
//   } while ((pbVar3 != pbVar2) && (in_DX = in_DX + -1, pbVar2 = pbVar3, in_DX != 0));
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3d36;
var
  commandLineSegment: Word;
  remaining: Word;
  startOffset: Word;
  address: Longint;
  commandLineLength: Byte;
  currentByte: Byte;
  tokenLength: Word;
begin
  commandLineSegment :=
    Word(DosMemory[$640C]) or (Word(DosMemory[$640D]) shl 8);
  RegisterES := commandLineSegment;
  RegisterBX := 0;
  RegisterDI := $80;
  address := ((Longint(commandLineSegment) shl 4) + RegisterDI) and $FFFFF;
  commandLineLength := RealModeMemory[address];
  remaining := commandLineLength;
  Inc(RegisterDI);
  tokenLength := 0;

  while remaining <> 0 do
  begin
    address := ((Longint(commandLineSegment) shl 4) + RegisterDI) and $FFFFF;
    currentByte := RealModeMemory[address];
    while (remaining <> 0) and (currentByte <= $20) do
    begin
      Dec(remaining);
      Inc(RegisterDI);
      if remaining <> 0 then
      begin
        address := ((Longint(commandLineSegment) shl 4) + RegisterDI) and
          $FFFFF;
        currentByte := RealModeMemory[address];
      end;
    end;
    RegisterCX := remaining;
    if remaining = 0 then
      Break;

    startOffset := RegisterDI;
    RegisterSI := startOffset;
    while remaining <> 0 do
    begin
      address := ((Longint(commandLineSegment) shl 4) + RegisterDI) and
        $FFFFF;
      currentByte := RealModeMemory[address];
      if currentByte <= $20 then
        Break;
      Dec(remaining);
      Inc(RegisterDI);
    end;
    tokenLength := Word(RegisterDI - startOffset);
    RegisterAX := tokenLength;
    Inc(RegisterBX);
    Dec(RegisterDX);
    RegisterCX := remaining;
    if RegisterDX = 0 then
      Break;

    if remaining <> 0 then
    begin
      Inc(RegisterDI);
      Dec(remaining);
    end;
  end;
  RegisterCX := remaining;
  RegisterAX := tokenLength;
end;
