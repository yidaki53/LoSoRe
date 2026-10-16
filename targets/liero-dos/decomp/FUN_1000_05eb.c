
void FUN_1000_05eb(byte param_1)

{
  undefined2 unaff_DS;
  undefined2 local_4;
  
  FUN_24dd_0530();
  FUN_24dd_48e1(3,(uint)*(byte *)(param_1 + 0x68) * 3 + 0x5826,unaff_DS,(uint)param_1 * 3 + 0x66d8,
                unaff_DS);
  FUN_1ec2_0810(*(undefined1 *)(param_1 + 0x68),0x5826,unaff_DS);
  local_4 = -2;
  while( true ) {
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5826) =
         (char)((uint)*(byte *)((uint)param_1 * 3 + 0x66d8) * (uint)*(byte *)(local_4 + 0x1a4) >> 6)
    ;
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5827) =
         (char)((uint)*(byte *)((uint)param_1 * 3 + 0x66d9) * (uint)*(byte *)(local_4 + 0x1a4) >> 6)
    ;
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5828) =
         (char)((uint)*(byte *)((uint)param_1 * 3 + 0x66da) * (uint)*(byte *)(local_4 + 0x1a4) >> 6)
    ;
    FUN_1ec2_0810((uint)*(byte *)(param_1 + 0x68) + local_4,0x5826,unaff_DS);
    if (local_4 == -1) break;
    local_4 = local_4 + 1;
  }
  local_4 = 1;
  while( true ) {
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5826) =
         (char)((uint)*(byte *)(local_4 + 0x1a3) * 0x3f +
                (uint)*(byte *)((uint)param_1 * 3 + 0x66d8) *
                (0x3f - (uint)*(byte *)(local_4 + 0x1a3)) >> 6);
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5827) =
         (char)((uint)*(byte *)(local_4 + 0x1a3) * 0x3f +
                (uint)*(byte *)((uint)param_1 * 3 + 0x66d9) *
                (0x3f - (uint)*(byte *)(local_4 + 0x1a3)) >> 6);
    *(undefined1 *)(((uint)*(byte *)(param_1 + 0x68) + local_4) * 3 + 0x5828) =
         (char)((uint)*(byte *)(local_4 + 0x1a3) * 0x3f +
                (uint)*(byte *)((uint)param_1 * 3 + 0x66da) *
                (0x3f - (uint)*(byte *)(local_4 + 0x1a3)) >> 6);
    FUN_1ec2_0810((uint)*(byte *)(param_1 + 0x68) + local_4,0x5826,unaff_DS);
    if (local_4 == 2) break;
    local_4 = local_4 + 1;
  }
  local_4 = 0;
  while( true ) {
    FUN_24dd_3d68(3,((uint)*(byte *)(param_1 + 0x1a6) + local_4) * 3 + 0x5826,unaff_DS,
                  ((uint)*(byte *)(param_1 + 0x68) + local_4 % 3 + -1) * 3 + 0x5826,unaff_DS);
    FUN_1ec2_0810((uint)*(byte *)(param_1 + 0x1a6) + local_4,0x5826,unaff_DS);
    if (local_4 == 5) break;
    local_4 = local_4 + 1;
  }
  local_4 = 0;
  while( true ) {
    FUN_24dd_3d68(3,((uint)*(byte *)(param_1 + 0x1a8) + local_4) * 3 + 0x5826,unaff_DS,
                  ((uint)*(byte *)(param_1 + 0x68) + (uint)*(byte *)(local_4 + 0x1aa)) * 3 + 0x5826,
                  unaff_DS);
    FUN_1ec2_0810((uint)*(byte *)(param_1 + 0x1a8) + local_4,0x5826,unaff_DS);
    if (local_4 == 3) break;
    local_4 = local_4 + 1;
  }
  return;
}

