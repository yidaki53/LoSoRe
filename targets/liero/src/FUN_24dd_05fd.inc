{ liero::FUN_24dd_05fd — reviewed Pascal reconstruction (oracle: host-test).
  Host behavior passed; original-binary parity remains unverified.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C ---
// 
// void __cdecl16near FUN_24dd_05fd(void)
// 
// {
//   undefined2 in_AX;
//   byte in_CL;
//   undefined2 *unaff_DI;
//   undefined2 unaff_ES;
//   
//   *unaff_DI = 0;
//   unaff_DI[1] = 0;
//   unaff_DI[2] = 0;
//   unaff_DI[3] = 0;
//   unaff_DI[4] = in_AX;
//   unaff_DI[5] = (uint)in_CL;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_05fd;
var
  originalAX: Word;
  destinationOffset: Word;
  destinationAddress: Longint;
  wordIndex: Integer;
begin
  originalAX := RegisterAX;
  destinationOffset := RegisterDI;
  for wordIndex := 0 to 3 do
  begin
    destinationAddress := ((Longint(RegisterES) * 16) +
      destinationOffset) and $FFFFF;
    RealModeMemory[destinationAddress] := 0;
    RealModeMemory[(destinationAddress + 1) and $FFFFF] := 0;
    Inc(destinationOffset, 2);
  end;
  destinationAddress := ((Longint(RegisterES) * 16) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := originalAX and $00FF;
  RealModeMemory[(destinationAddress + 1) and $FFFFF] := originalAX shr 8;
  Inc(destinationOffset, 2);
  destinationAddress := ((Longint(RegisterES) * 16) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := RegisterCX and $00FF;
  RealModeMemory[(destinationAddress + 1) and $FFFFF] := 0;
  RegisterAX := RegisterCX and $00FF;
end;
