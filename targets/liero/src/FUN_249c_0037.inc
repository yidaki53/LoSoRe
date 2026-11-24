{ Oracle: complete original0037 execution, supported textmode3/device37b3 path.
  Host source pointer resolves original far input; logical segmented stack/video
  state and checked output bindings are explicit, not native TP7 ABI.
  Nonzero04f4 uses the checked text-code return binding; arbitrary BIOS effects,
  descriptor/callback chains and normal startup remain unresolved.
  Original assembly retained; no whole-source or training promotion. }
procedure FUN_249c_0037(param_1: Pointer; param_2, param_3: Byte);
var
  savedBP, entrySP, frame, screenOffset, index, length: Word;
  state, value: Byte;
  stackBase, frameAddress, sourceAddress: LongInt;
begin
  if (param_1 = nil) or (BIOSVideoMode <> 3) or
     (RegisterDS <> LieroTextDataSegment) or (RegisterSP < $200) or
     (RegisterSP > $FFF0) or
     (LieroBufferObjectOffset <> $79F0) or
     (LieroBufferObjectSegment <> RegisterDS) then RunError(211);
  sourceAddress := LongInt(RegisterDS) * 16;
  if (RegisterSS <> RegisterDS) or (LieroBufferCodeSegment <> RegisterDS) or
     (RegisterSP < $DB00) or (RegisterSP > $DFF0) or
     (sourceAddress + $E000 > $A0000) or
     (param_1 <> @RealModeMemory[sourceAddress + $8200]) or
     (LieroBufferObject <> @RealModeMemory[sourceAddress + $79F0]) then
    RunError(211);
  length := PByte(param_1)^;
  if (param_2 >= 25) or (LongInt(param_3) + length >= 80) then RunError(211);
  entrySP := RegisterSP;
  savedBP := RegisterBP;
  frame := entrySP - 2;
  stackBase := LongInt(RegisterSS) * 16;
  frameAddress := stackBase + frame;
  sourceAddress := LongInt(RegisterDS) * 16 + $79F0;
  if (frameAddress + 16 > $100000) or
     ((sourceAddress < frameAddress + 16) and
      (sourceAddress + 256 > frameAddress - $10A)) or
     ((LongInt(LieroBufferSourceSegment) * 16 + LieroBufferSourceOffset <
       frameAddress + 16) and
      (LongInt(LieroBufferSourceSegment) * 16 + LieroBufferSourceOffset + 128 >
       frameAddress - $10A)) then RunError(211);
  RegisterBP := frame;
  RegisterSP := frame - $10A;
  Move(param_1^, RealModeMemory[frameAddress - 256], length + 1);
  RealModeMemory[frameAddress - 260] := 7;
  RealModeMemory[frameAddress - 261] := 0;
  RegisterSP := RegisterSP - 4;
  FUN_249c_0013(Integer(frame));
  screenOffset := (Word(param_2) * 80 + param_3) * 2;
  RegisterSP := RegisterSP - 8;
  FUN_249c_0000(param_3, param_2);
  state := 0;
  for index := 1 to length do begin
    value := RealModeMemory[frameAddress - 256 + index];
    case state of
      0: if value = 0 then state := 1 else begin
        RealModeMemory[$B8000 + screenOffset] := value;
        RealModeMemory[$B8000 + screenOffset + 1] :=
          RealModeMemory[frameAddress - 259];
        Inc(screenOffset, 2);
      end;
      1: begin
        state := 2;
        RealModeMemory[frameAddress - 260] := value;
        RegisterSP := RegisterSP - 4;
        FUN_249c_0013(Integer(frame));
      end;
      2: begin
        state := 0;
        RealModeMemory[frameAddress - 261] := value;
        RegisterSP := RegisterSP - 4;
        FUN_249c_0013(Integer(frame));
      end;
    end;
  end;
  RegisterSP := RegisterSP - 8;
  FUN_249c_0000(Word(param_3) + length, param_2);
  RegisterSP := RegisterSP - 8;
  FUN_24dd_3930((LongInt(RegisterDS) shl 16) or $79F0);
  RegisterSP := RegisterSP - 4;
  if GlobalWord6410 <> 0 then begin
    if (LieroTextCodeSegment = 0) or
       (LieroErrorDataSegment <> RegisterDS) or
       (LieroErrorCodeSegment <> LieroBufferCodeSegment) then RunError(211);
    WriteWordLE(@RealModeMemory[stackBase], RegisterSP, $0155);
    WriteWordLE(@RealModeMemory[stackBase], RegisterSP + 2, LieroTextCodeSegment);
  end;
  FUN_24dd_04f4;
  RegisterBP := savedBP;
  RegisterSP := entrySP + 12;
end;
