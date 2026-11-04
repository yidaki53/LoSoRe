{ liero::FUN_1ec2_09bd — signed-word result ($FFFF, 0, or 1).
  Oracle: complete original-byte source review and exhaustive signed-word
  return differential at this entry. unusedWord is not read by the original.
  Valid SS frame/arguments required; host ABI and caller reachability differ. }
function FUN_1ec2_09bd(unusedWord: Word; value: Integer): Word;
begin
  FUN_1ec2_09bd := SignWord(value);
end;
