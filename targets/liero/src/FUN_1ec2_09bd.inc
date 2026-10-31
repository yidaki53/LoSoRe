{ liero::FUN_1ec2_09bd — signed comparison result (-1, 0, or 1).
  Oracle: none; not compared with the DOS executable. }
function FUN_1ec2_09bd(param_1: Word; param_2: Integer): Word;
begin
  FUN_1ec2_09bd := SignWord(param_2);
end;
